# 実装・パラメータ・対象版の対応

このページは、pangeo-fish `main` の `af4fe17` のソースと、同じコミットの Complete デモ（`notebooks/pangeo-fish-complete-demo.ipynb`）を読んで整理したものである（ノートブックを実行して確かめたものではない）。**関数の既定値とNotebookで明示的に与えた値を別々に記す。** ワークショップの環境はこのコミットをビルドしたイメージ `ghcr.io/pangeo-fish/pangeo-fish-notebook:2026.10.21-af4fe17` で、デモの HEALPix レベルは10である。

単位は入力の物理量を踏まえた記述であり、すべての関数がPintによる単位検査を行うという意味ではない。下記にないNotebook変数名や引数の完全なsignatureは、組み込み時にコードで再確認する。

## 1. どこで何を設定するか

| 目的 | 主な入口 | 関連する項目 | 変えると何が変わるか |
|---|---|---|---|
| タグとモデルの温度差 | `compute_diff` → `diff_z` | 深度、time bounds、`min_water_depth` | 比較するサンプル・モデル深度と有効セル |
| 水温の観測確率（emission probability） | `compute_emission_pdf` → `pdf.normal` | `differences_std` | 温度差をどの程度許すか |
| 放流・終点 | `compute_emission_pdf` → `normal_at` | `initial_std`, `recapture_std` | 既知位置を格子上でどれだけ広げるか |
| 音響 | `compute_acoustic_pdf` → `emission_probability` | `receiver_buffer`, `nondetections` | 受信範囲・未検出の意味 |
| 海底地形 | `compute_healpix_histogram_region_bin_size`、`batch_compute_pdf_bathy` | `depth_bin_size`等 | セル内の深度分布の表現と深さの整合 |
| 潮汐の区間検出 | `detect_tide` → `tide_behav_extr` | `tideFL`・`tideLV`・`behavFL`・`behavLV`（窓長、RMSE・$R^2$・振幅の閾値） | どの区間に潮汐情報があるとみなすか |
| legacy潮汐 | `tide_pdf`、`tide_to_healpix` | `sigma_tid`（`tide_pdf` 内で2.0に固定）、時間集約 | 絶対水柱深度を含む重み |
| HEALPix潮汐 | `still_tag_tide_likelihood`（デモが呼ぶ。`predict_tide` は別の公開関数でデモは呼ばない） | `sigma`, `n_eff`, `water_column`等 | 波形残差、オフセット、有効情報量 |
| 観測を組み合わせる | `normalize_pdf` → `combine_emission_pdf` | `excluded_pdf` | 積に含める観測項 |
| 移動を推定する | `optimize_pdf` | `conv_method`, `maximum_speed`, `truncate`, `tolerance` | 遷移の計算、σの探索範囲、数値精度 |
| 2種類の移動幅 | `stamp_parameter_indices_from_mask`と最適化 | `predictor_index`、行動フラグ | 各遷移で使うσ |
| 結果を要約する | `decode_trajectories`（`track_modes`：`mean`・`mode`・`viterbi_healpix`） | 入力分布、遷移（Viterbi の `truncate`、`ellipsoid` は `decode_trajectories` 経由では既定値） | 平均・最頻・連続する最尤状態列 |

## 2. 水温・初期位置・音響

| 引数・設定 | 関数の既定値／要件 | デモの値・呼出し | 科学的・数値的意味 |
|---|---|---|---|
| `differences_std` | `compute_emission_pdf`で必須 | 0.75 °C | 平均した符号付き温度差（モデルの温度の単位）に対する正規分布の標準偏差。センサー精度そのものではない |
| `initial_std` | 同関数で必須 | $10^{-4}$ rad | 放流位置まわりの正規分布の幅（セル中心間の角距離に対する値） |
| `recapture_std` | 同関数で必須 | $10^{-4}$ rad | 終点イベントがある場合の広がり。ソースは `fish_death` イベントを参照する |
| `min_water_depth`（`compute_diff`） | `"auto"` | デモは指定しない（コメントに選択肢のみ） | 干出するセル（仮）の扱い。数値ならm、`None` は保持する指定。`"auto"` では `H0 + XE <= 0` のセルがあるときだけ除外され、実際に起こるのは North-West Shelf の1時間値の場合に限る（`docs/dry-cells.md`） |
| `relative_depth_threshold` | `compute_diff` で必須だが、`main` では使われず、非ゼロだと `FutureWarning` | 0 | 配布デモの設定コメントは旧動作（浅いセルの除外）を説明したままだが、**有効な浅海除外のスイッチとして教えない** |
| `receiver_buffer` | ラッパーでPint量を要求 | 2,000 m | 受信可能域を近似する半径 |
| `nondetections`（下位関数 `emission_probability` の引数） | `"ignore"` | ラッパー `compute_acoustic_pdf` は `"mask"` を固定して渡す | ラッパーに同名の切替引数があるとは説明しない |
| `chunk_time` | ラッパー（`compute_diff`・`compute_emission_pdf`・`compute_acoustic_pdf`）で24 | **1**（研究設定で上書き） | 時間の処理チャンク（デモでは1時間ステップ分）であり、24時間の生物学的仮定ではない |

半径6,371 kmを用いる単純な角度換算では、$10^{-4}$ radは約0.637 km、0.0003 radは約1.911 kmである。後者は日本語Baseの手動σ（`sigma=[0.0003]`）の例である。格子レベル10の代表長約6.4 kmより狭い幅も設定されているため、この数値をそのまま達成された位置精度と呼ばない。

音響ラッパーと下位関数で既定動作が違う点は、研究用の直接呼出しに移るときに特に確認する。[helpers.py](https://github.com/pangeo-fish/pangeo-fish/blob/af4fe17/pangeo_fish/helpers.py)／[acoustic.py](https://github.com/pangeo-fish/pangeo-fish/blob/af4fe17/pangeo_fish/acoustic.py)

## 3. 海底地形

| 引数・処理 | 関数の既定値 | Completeの設定 | 留意点 |
|---|---|---|---|
| `depth_bin_size` | 1（m） | 16 m | ヒストグラムの深度刻み |
| `max_depth_m` | `None`（`nb_depth_bins` とどちらかが必須） | 1,000 m | `ceil(max_depth_m / depth_bin_size)`（デモでは63）ビンを作る |
| `depth_offset` | 0 | 指定なし | `(-elevation - depth_offset)/depth_bin_size` で水深を求める際に引く値 |
| `chunk_size` | 500 | 指定なし | 一度に読む緯度の行数 |
| `ellipsoid` | `"sphere"` | 研究設定の `ellipsoid`（配布デモでは `"sphere"`） | セルIDの計算に渡される。出力のセル座標は球面で作られる（[楕円体HEALPix](09_ellipsoidal_healpix.md)第7節） |
| `batch_compute_pdf_bathy` の `batch_size` | 50,000（セル） | 10,000（セル） | 一度に計算するセル数 |
| 深度検索の `+10` | ヒストグラム側は10**ビン**、引く側は10**m** | そのまま適用 | `depth_bin_size = 1` では一致するが、デモの16 mでは一致しない（[海底地形](06_bathymetry.md)第3節）。校正済み誤差幅や基準面補正ではない |
| ヒストグラムの `stdev` 利用 | 平滑化カーネルの幅として**ビン単位**でそのまま使う（`depth_bin_size` で割らない）。入力にないとき1.0、最小0.5 | データに `stdev` があるかは未確認 | 物理的な幅はビン幅に依存する。単位の整合を要確認 |

最後の二行はユーザーが調整できる公開パラメータの説明ではなく、**科学的意味を説明する前に確認すべき実装事項**である。[bathy.py](https://github.com/pangeo-fish/pangeo-fish/blob/af4fe17/pangeo_fish/bathy.py)

## 4. 潮汐

### 区間を選ぶ処理

`detect_tide`の実効設定（`TIDE_PARAMS`）は、潮汐検出が窓10 h・RMSE 0.42 m未満・$R^2$ 0.85超・振幅0.6 m超、行動フラグが窓16 h・RMSE 0.42 m未満・$R^2$ 0.70超・振幅0.2 m超。等号は含まない。下位関数 `tide_behav_extr` の直接既定値（窓10 h／16 h、閾値は両方とも `[0.5, 0.7, 0.5]`）とは異なる。

ターゲットは10分間隔で、細かい記録は各10分間の最初のサンプルを取る再サンプリング、粗い記録は `NotImplementedError` になる。フィットは固定周期12.42 hの正弦・余弦と切片を用いる。これらはタグの深度パターンの判定であり、独立な着底観測ではない。[tide.py](https://github.com/pangeo-fish/pangeo-fish/blob/af4fe17/pangeo_fish/tide.py)

### HEALPix潮汐の観測重み

| 引数 | `still_tag_tide_likelihood`の既定値 | デモで与える値 | 意味 |
|---|---|---|---|
| `sigma` | 必須（キーワード引数） | 2 m（`tide_sigma_m`） | モデル誤差（潮汐モデル・高潮・センサー）の尺度。1時間内の変動ではない |
| `freq` | `"1h"` | 既定 | 観測と予測を同じサンプルで集約する時間単位 |
| `time_step` | `"1D"` | 既定 | 位置の重みを作る時間区間 |
| `min_samples` | 12 | 6（`tide_min_samples`） | 窓内の有効な集約サンプルの最低数。足りない窓は一様な重み |
| `n_eff` | `None`（窓内のサンプル数） | 既定 | 尤度の鋭さを左右する情報量。自動で自己相関を推定する指定ではない |
| `water_column` | `None` | 指定なし | 与えなければ各セル・窓で平均水深を推定。与えるときは平均海面基準の水深（m） |
| `valid` | `None` | `tide_found > 0` | 使用する観測のフラグ |
| `min_tidal_signal` | 0.05 m | 既定（効かない） | `detection_ratio` を指定したときだけ使われる最小信号 |
| `detection_ratio` | `None` | 指定なし（`None`） | `None` ならモデルに基づく窓の判定をしない |
| `tide_method`（デモの設定） | — | `"legacy"`（既定）／`"healpix"` | `"healpix"` は `pangeo-fish[tide]`（PyFES）が必要 |
| `tide_model`（デモの設定） | — | `"tpxo9"`（既定）／`"fes2022b"` | FES2022b は `tide_method="healpix"` と `ellipsoid="WGS84"` が必須 |

legacyの`sigma_tid=2.0`は、どの時間にも一律に2 mを使うという意味ではない。ソースでは、尺度はその時間枠のタグ水深のサンプル標準偏差で、時間枠のサンプル行列の幅が1のとき、または標準偏差が $10^{-6}$ 未満のときだけ`sigma_tid`（2.0）に置き換わる。[HEALPix方式](https://github.com/pangeo-fish/pangeo-fish/blob/af4fe17/pangeo_fish/tide_healpix.py)／[legacy方式](https://github.com/pangeo-fish/pangeo-fish/blob/af4fe17/pangeo_fish/tide.py)

## 5. 移動と最適化

| 引数・設定 | 関数等の既定値 | デモの値 | 解釈 |
|---|---|---|---|
| `conv_method` | `"FFTConv"` | `"FFTConv"` | 遷移を適用する数値方法 |
| `maximum_speed` | 必須（Pint量） | 60 km/day | σの探索上限を作る尺度。実現する移動距離の上限ではない |
| `adjustment_factor` | 必須 | 1 | 探索上限の倍率 |
| `truncate` | 必須（`None` 可。`HealpixConv` では `None` 不可） | 5 | カーネルの打ち切り幅（σの倍数） |
| `tolerance` | 必須 | $10^{-6}$ | 探索の許容差（`scipy.optimize.fminbound` の `xtol`） |
| `single_behav` | `True` | 1つのσのとき `True`、2つのσの例でも `True` | 多σのときに、行動の値ごとに1つのσを推定する（`False` は連続区間ごと） |
| `multivariate` | `False` | 二つのσの例で `True` | 全σを同時に最適化する |
| `final` | `False` | 指定なし | `True` で、最終状態が観測した最終位置と合うようにσを最適化する。多σ（`predictor_index`）とは併用不可 |
| `earth_radius` | `None` | 既定 | `None` なら格子の `ellipsoid` から求める（球なら半径、楕円体なら長半径） |
| `ellipsoid` | `None`（格子の属性から推定） | 既定 | 畳み込みの作用素に渡される |
| `projection` | `"conservative"` | 既定 | `FFTConv` のみ |
| `normalization`、`land_barrier` | `"full_disc"`、`False` | 既定 | `HealpixAnalyseConv` のみ |
| 探索の範囲 | — | — | 下限 $10^{-4}$ rad、上限は `maximum_speed × Δt × adjustment_factor / 地球半径`（rad）。単独σは `fminbound`（有界の Brent 法） |
| joint optimizer（`fit_multivariate_parameter`） | `Powell`、`maxfev=20` | 二つのσの例 | 目的関数の評価回数の上限と識別性を確認する |
| Viterbiの打ち切り | `truncate=4.0`（`viterbi_healpix`） | `decode_trajectories` は渡さない | fitの`truncate=5`と自動で一致しない |

`final=False`という引数だけを見て、終点情報を使っていないと判断しない。`combine_emission_pdf`が最後の観測スライスに終点因子（`final`）を掛ける経路もあるため、計算全体で何回条件付けされるかを確認する。

Completeの二つのσの例では、日別の`behav_found > 0`から`predictor_index`を作り（`stamp_parameter_indices_from_mask`）、グループごとに60／30 km/dayの速度尺度（`maximum_speed`と`maximum_speed / 2`）をσの探索上限とする。潜在的な行動状態の遷移確率を同時推定するモデルとは区別する。[最適化](https://github.com/pangeo-fish/pangeo-fish/blob/af4fe17/pangeo_fish/hmm/optimize/scipy.py)

## 6. 対象版・格子設定・依存パッケージ

### 6.1 ワークショップの設定

| 項目 | 内容 | 出典 |
|---|---|---|
| pangeo-fish | `main` のコミット `af4fe17`（`af4fe1734ab88a1ab63abf3f52e516a0da4456d0`） | 本書の起動ガイド（`pangeo-eosc.md`） |
| 環境イメージ | `ghcr.io/pangeo-fish/pangeo-fish-notebook:2026.10.21-af4fe17` | 同上 |
| 格子 | 球面（`ellipsoid = "sphere"`）、レベル10 | Complete／Baseデモと日本語Notebook |
| 海マスク閾値 | `mask_threshold = 0.25`（`regrid_dataset_hpresample` の既定値は0.5） | 同上 |
| 移動 | `FFTConv` | 同上 |
| 軌跡 | `track_modes = ["viterbi_healpix", "mode", "mean"]` | 同上 |
| 潮汐 | `tide_method = "legacy"`、`tide_model = "tpxo9"` | Completeデモ |

WGS84 を選ぶ設定は配布デモにあるが、既定は球面である。楕円体に関する `main` の挙動は[楕円体HEALPix](09_ellipsoidal_healpix.md)第7節にまとめた。

### 6.2 依存パッケージの版

ソースツリーで読み取れる版の情報は次のとおりで、いずれも**最低限の制約**または CI の固定値であり、実際に環境へ入った版ではない。

| パッケージ | 読み取れる情報 | 出典 |
|---|---|---|
| pangeo-fish | 版番号は読み取れない（`setuptools_scm` が動的に決め、フォールバックは `999`）。コミット `af4fe17` で特定する | `pyproject.toml` |
| healpix-geo | `>=0.5`。デモ用 CI の固定値は `0.5.0` | `pyproject.toml`、`ci/requirements/demo-constraints.txt` |
| healpix-resample | `>=2026.11.2,<2027`。同固定値は `2026.11.2` | 同上 |
| healpix-analyse | `>=2026.11.1`。同固定値は `2026.11.1` | 同上 |
| xdggs | `==0.6.0` | `pyproject.toml` |
| PyFES | 任意の依存 `tide` として `pyfes>=2026.10`。CI の固定値はない | `pyproject.toml` |
| xarray／zarr | `>=2025.7.1,<2027`／`>=3.1.2,<4` | `pyproject.toml` |

イメージに実際に入った版は、Complete デモ末尾の付録「Information for bug reports」のセルが表示する（pangeo-fish、xarray、dask、numpy、xdggs、healpix-geo、copernicusmarine）。解析結果の属性にも、pangeo-fish・healpix-convolution・xarray・xhealpixify の版が記録される（`helpers._get_package_versions`）。PyFES の実際の版は、潮汐に `"healpix"` を使うときに別途記録する。
