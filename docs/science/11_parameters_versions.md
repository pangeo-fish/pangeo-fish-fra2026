# 実装・パラメータ・対象版の対応

このページは、pangeo-fish `main` の `361e9b7` の関数と、同じコミットの Complete デモ（`notebooks/pangeo-fish-complete-demo.ipynb`）のパラメータをまとめたものです。**関数の既定値とNotebookで明示的に与えた値を別々に記します。** ワークショップの環境はこのコミットをビルドしたイメージ `ghcr.io/pangeo-fish/pangeo-fish-notebook:2026.11.2` で、デモの HEALPix レベルは10です。

単位は入力の物理量を踏まえた記述であり、すべての関数がPintによる単位検査を行うという意味ではありません。下記にないNotebook変数名や引数の完全なsignatureは、組み込み時にコードで再確認します。

## 1. どこで何を設定するか

| 目的 | 主な入口 | 関連する項目 | 変えると何が変わるか |
|---|---|---|---|
| タグとモデルの温度差 | `compute_diff` → `diff_z` | 深度、time bounds、`min_water_depth` | 比較するサンプル・モデル深度と有効セル |
| 水温の観測確率（emission probability） | `compute_emission_pdf` → `pdf.normal` | `differences_std` | 温度差をどの程度許すか |
| 放流・終点 | `compute_emission_pdf` → `normal_at` | `initial_std`, `recapture_std` | 既知位置を格子上でどれだけ広げるか |
| 音響 | `compute_acoustic_pdf` → `emission_probability` | `receiver_buffer`, `nondetections` | 受信範囲・未検出の意味 |
| 海底地形 | `compute_healpix_histogram_region_bin_size`、`batch_compute_pdf_bathy` | `depth_bin_size`等 | セル内の深度分布の表現と深さの整合 |
| 潮汐の区間検出 | `detect_tide` → `tide_behav_extr` | `tideFL`・`tideLV`・`behavFL`・`behavLV`（窓長、RMSE・$R^2$・振幅の閾値） | どの区間に潮汐情報があるとみなすか |
| 潮汐（`healpix`、既定） | `still_tag_tide_likelihood`（デモが呼ぶ。`predict_tide` は別の公開関数でデモは呼ばない） | `sigma`, `n_eff`, `water_column`等 | 波形残差、オフセット、有効情報量 |
| 潮汐（`pedersen`） | `pedersen_tide_likelihood`、`cell_bathymetry`（セルの平均水深） | `window_hours`、共分散のパラメータ（`white_noise_sd`・`depth_offset_sd`等） | 時間相関のある共分散での水深の比較。誤差パラメータは未較正 |
| 潮汐を総合 PDF に結合 | `write_tide_pdf_healpix` → `merge_tide_with_total` | なし | セル・日の対応、欠けた分の中立な因子 |
| 観測を組み合わせる | `normalize_pdf` → `combine_emission_pdf` | `excluded_pdf` | 積に含める観測項 |
| 移動を推定する | `optimize_pdf` | `conv_method`, `maximum_speed`, `truncate`, `tolerance` | 遷移の計算、σの探索範囲、数値精度 |
| 2種類の移動幅 | `stamp_parameter_indices_from_mask`と最適化 | `predictor_index`、行動フラグ | 各遷移で使うσ |
| 結果を要約する | `decode_trajectories`（`track_modes`：`mean`・`mode`・`viterbi_healpix`） | 入力分布、遷移（Viterbi の `truncate` は渡されず4.0。`ellipsoid` は予測器のものが引き継がれ、`decode_trajectories` 経由では格子の楕円体） | 平均・最頻・連続する最尤状態列 |

## 2. 水温・初期位置・音響

| 引数・設定 | 関数の既定値／要件 | デモの値・呼出し | 科学的・数値的意味 |
|---|---|---|---|
| `differences_std` | `compute_emission_pdf`で必須 | 0.75 °C | 平均した符号付き温度差（モデルの温度の単位）に対する正規分布の標準偏差。センサー精度そのものではない |
| `initial_std` | 同関数で必須 | $10^{-4}$ rad | 放流位置まわりの正規分布の幅（セル中心間の角距離に対する値） |
| `recapture_std` | 同関数で必須 | $10^{-4}$ rad | 終点イベントがある場合の広がり。`fish_death` イベントを参照する |
| `min_water_depth`（`compute_diff`） | `"auto"` | デモは指定しない（コメントに選択肢のみ） | 干出するセル（仮）の扱い。数値ならm、`None` は保持する指定。`"auto"` では `H0 + XE <= 0` のセルがあるときだけ除外され、実際に起こるのは North-West Shelf の1時間値の場合に限る（`docs/dry-cells.md`） |
| `relative_depth_threshold` | `compute_diff` で必須だが、`main` では使われず、非ゼロだと `FutureWarning` | 0 | 配布デモの設定コメントは旧動作（浅いセルの除外）を説明したままだが、**有効な浅海除外のスイッチとして教えない** |
| `receiver_buffer` | ラッパーでPint量を要求 | 2,000 m | 受信可能域を近似する半径 |
| `nondetections`（下位関数 `emission_probability` の引数） | `"ignore"` | ラッパー `compute_acoustic_pdf` は `"mask"` を固定して渡す | ラッパーに同名の切替引数があるとは説明しない |
| `chunk_time` | ラッパー（`compute_diff`・`compute_emission_pdf`・`compute_acoustic_pdf`）で24 | **1**（研究設定で上書き） | 時間の処理チャンク（デモでは1時間ステップ分）であり、24時間の生物学的仮定ではない |

WGS84 の長半径6,378 kmを用いる単純な角度換算では、$10^{-4}$ radは約0.64 km、0.0003 radは約1.91 kmです。後者は日本語Baseの手動σ（`sigma=[0.0003]`）の例です。格子レベル10の代表長約6.4 kmより狭い幅も設定されているため、この数値をそのまま達成された位置精度と呼びません。

音響ラッパーと下位関数で既定動作が違う点は、研究用の直接呼出しに移るときに特に確認します。[helpers.py](https://github.com/pangeo-fish/pangeo-fish/blob/361e9b7/pangeo_fish/helpers.py)／[acoustic.py](https://github.com/pangeo-fish/pangeo-fish/blob/361e9b7/pangeo_fish/acoustic.py)

## 3. 海底地形

| 引数・処理 | 関数の既定値 | Completeの設定 | 留意点 |
|---|---|---|---|
| `depth_bin_size` | 1（m） | 2 m | 深度ビンの幅（m）。尤度（likelihood）はビン内で線形補間されるので、幅を広げると海底の位置が最大1ビンぶんぼやける |
| `max_depth_m` | `None`（`nb_depth_bins` とどちらかが必須） | 1,000 m | 最後のビン境界がちょうど `max_depth_m` になる（最後の区間は短くなりうる）。デモでは `ceil(1000 / 2)` = 500 区間で、これより深い魚には「`max_depth_m` より深い海底の割合」が使われる |
| `depth_offset` | 0 | 指定なし | 魚と海底の間の余裕（m）。水深を `-elevation - depth_offset` として求める。負の値なら、その分だけ海底より下を許す |
| `default_stdev_m` | 1（m） | 指定なし | `stdev` がない、または有限でない点の GEBCO 水深の鉛直不確かさ（m） |
| `chunk_size` | 500 | 指定なし | 一度に読む緯度の行数 |
| `ellipsoid` | `"WGS84"` | 研究設定の `ellipsoid`（配布デモでは `"WGS84"`） | セルIDとセル中心の計算に渡され、出力の `cell_ids` 属性にも保存される（[楕円体HEALPix](09_ellipsoidal_healpix.md)第7節） |
| `batch_compute_pdf_bathy` の `batch_size` | 50,000（セル） | 10,000（セル） | 一度に計算するセル数 |
| `depth_bins`（出力の水深軸） | 海面より上の10ビンぶん（`-10 × depth_bin_size`）から最後の境界まで、単位は m | そのまま適用 | 水深を引く側も同じ m の軸で読むので、ビン幅を変えても一致する。校正済み誤差幅や基準面補正ではない |
| ヒストグラムの `stdev` 利用 | 各 GEBCO 点の水深を、平均が水深、標準偏差が `stdev`（**m**）の正規分布として広げる。入力にないとき `default_stdev_m`（1 m）、最小は0.001 m | データに `stdev` があるかは未確認 | ビン幅とは独立に m で与える。値は誤差の仮定であり、推奨される測深誤差ではない |

最後の二行はユーザーが調整できる公開パラメータの説明ではなく、**科学的意味を説明する前に確認すべき実装事項**です。この節の海底地形の記述は `361e9b7` に対応しています。[bathy.py](https://github.com/pangeo-fish/pangeo-fish/blob/361e9b7/pangeo_fish/bathy.py)

## 4. 潮汐

### 区間を選ぶ処理

`detect_tide`の実効設定（`TIDE_PARAMS`）は、潮汐検出が窓25 h・RMSE 0.42 m未満・$R^2$ 0.85超・振幅0.6 m超（かつ上限 `ampli_max` = 5 m 未満）、行動フラグが窓25 h・RMSE 0.42 m未満・$R^2$ 0.70超・振幅0.2 m超（同じく5 m未満）です。等号は含みません。下位関数 `tide_behav_extr` の直接既定値（窓は同じく25 h、閾値は両方とも `[0.5, 0.7, 0.5]`）とは閾値が異なります。窓長の下限は M2 の周期 12.42 h で、これより短いと `ValueError` です。フラグは窓の中心に記録され、有効サンプルが80%（`min_coverage`）未満の窓はフラグ0です。

ターゲットは10分間隔で、細かい記録は各10分間の最初のサンプルを取る再サンプリング、粗い記録は `NotImplementedError` になります。各窓で、1次の線形トレンドと固定周期12.42 hの正弦・余弦を最小二乗で当てはめます。これらはタグの深度パターンの判定であり、独立な着底観測ではありません。[tide.py](https://github.com/pangeo-fish/pangeo-fish/blob/361e9b7/pangeo_fish/tide.py#L685-L792)

### Complete デモの潮汐の設定（セル 7、8）

| 設定 | Complete デモの既定値 | 選択肢・意味 |
|---|---|---|
| `tide_method` | `"healpix"` | `"healpix"` または `"pedersen"`。それ以外は `ValueError`（セル 8）。どちらも `pyfes` が必要 |
| `tide_model` | `"tpxo9"` | `"tpxo9"`（Ifremer のデモ用データ）または `"fes2022b"`。FES2022b は `ellipsoid = "WGS84"` が必須 |
| `tide_model_source` | `None` | `None` なら公開の TPXO9 ファイル。ネイティブの FES2022b では、ローカルの `.nc` のパス（存在しないと `ValueError`） |
| `tide_constants_store` | `None` | FES2022b の事前計算 Zarr（`s3://` またはローカル）。`tide_model = "fes2022b"` かつ `tide_model_source` なしの場合のみ |
| `tide_s3_endpoint` | `None` | S3 互換のエンドポイント。`None` なら環境の S3 設定 |
| `tide_constituents` | `None` | `None` なら保存された分潮すべて。リストは FES2022b のみ、空リストは不可 |
| `tide_sigma_m` | 2.0 | `"healpix"` のみが読むモデル誤差（m）。`"pedersen"` で2.0以外にすると `check_tide_sigma` が警告する |
| `tide_min_samples` | 6 | `"healpix"` のみ。1日に必要な有効な1時間平均の最低数 |

### `healpix` 方式の観測重み

| 引数 | `still_tag_tide_likelihood`の既定値 | デモで与える値 | 意味 |
|---|---|---|---|
| `sigma` | 必須（キーワード引数） | 2 m（`tide_sigma_m`） | モデル誤差（潮汐モデル・高潮・センサー）の尺度。1時間内の変動ではない |
| `freq` | `"1h"` | 既定 | 観測と予測を同じサンプルで集約する時間単位 |
| `time_step` | `"1D"` | 既定 | 位置の重みを作る時間区間。ラベル $T$ は $(T-12\,\mathrm{h},\,T+12\,\mathrm{h}]$ |
| `min_samples` | 12 | 6（`tide_min_samples`） | 窓内の有効な集約サンプルの最低数。足りない窓は一様な重み |
| `n_eff` | `None`（窓内のサンプル数） | 既定 | 尤度（likelihood）の鋭さを左右する情報量。自動で自己相関を推定する指定ではない |
| `water_column` | `None` | 指定なし | 与えなければ各セル・窓で平均水深を推定。与えるときは平均海面基準の水深（m） |
| `valid` | `None` | `tide_found > 0` | 使用する観測のフラグ（窓の中心のサンプルだけが残る） |
| `min_tidal_signal` | 0.05 m | 既定（効かない） | `detection_ratio` を指定したときだけ使われる最小信号 |
| `detection_ratio` | `None` | 指定なし（`None`） | `None` ならモデルに基づく窓の判定をしない |

### `pedersen` 方式の観測重み

| 引数 | `pedersen_tide_likelihood`の既定値 | デモで与える値 | 意味 |
|---|---|---|---|
| `water_column` | 必須 | `cell_bathymetry` が GEBCO から作るセルの平均水深 | 平均海面基準の水深（m、正） |
| `tide_found`、`rmse` | 必須／`None` | `detect_tide` の `tide_found`、`rmse_tide` | 窓の中心のフラグと、当てはめの RMSE（共分散の時間相関の項の標準偏差） |
| `window_hours` | 25 | `tag_test.attrs["tideFL"]` | 1つのフラグの窓長 |
| `freq` | `None` | 既定 | `None` ならサンプルをそのまま使う |
| `white_noise_sd` | 0.2 m | 既定 | センサーの白色ノイズ |
| `ar_decay_hours`、`ar_level` | 6.67 h（40×10分）、0.05 | 既定 | 時間相関が 0.05 まで下がるまでの時間 |
| `epsilon` | 0.4 m | 既定（RMSE が取れない窓のみ） | 時間相関の項の標準偏差の代替値 |
| `depth_offset_sd` | 10 m | 既定 | 平均水深に対する一定の標準偏差 |
| `bathy_variance` | 20 m² | `cell_bathymetry` の分散 | `non_tidal="bathymetry"` のときだけ効く |
| `non_tidal` | `"uniform"` | 既定 | 窓のない日の PDF（一様）。`"bathymetry"` は MATLAB の海底地形のみの尤度（likelihood） |
| `min_fraction`、`max_overlap_hours` | 0.8、1 h | 既定 | 候補の窓に必要なサンプルの割合、異なる日の窓が共有できる時間 |

これらの誤差パラメータは MATLAB のコードのもので、このパッケージ向けには較正されていません。[tide_healpix.py](https://github.com/pangeo-fish/pangeo-fish/blob/361e9b7/pangeo_fish/tide_healpix.py#L488-L1249)／[Complete デモ](https://github.com/pangeo-fish/pangeo-fish/blob/361e9b7/notebooks/pangeo-fish-complete-demo.ipynb)（セル 7、8、79）

窓のない日の潮汐 PDF は、どちらの方式でも一様です。総合 PDF との結合（`merge_tide_with_total`）では、欠けたセルや日に一定の中立な因子が入ります。詳細は[潮汐](07_tides.md)3.4 節と[再格子化](09b_regridding_alignment.md)を参照します。

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
| `earth_radius` | `None` | 既定 | `None` なら格子の `ellipsoid` から求める（WGS84 では長半径 6378.137 km） |
| `ellipsoid` | `None`（格子の属性から推定。属性のない古い保存データは `"sphere"` とみなされる） | 既定（WGS84 の格子から取得） | 畳み込みの作用素に渡される |
| `projection` | `"conservative"` | 既定 | `FFTConv` のみ |
| `normalization`、`land_barrier` | `"full_disc"`、`False` | 既定 | `HealpixAnalyseConv` のみ |
| 探索の範囲 | — | — | 下限 $10^{-4}$ rad、上限は `maximum_speed × Δt × adjustment_factor / 地球半径`（rad）。単独σは `fminbound`（有界の Brent 法） |
| joint optimizer（`fit_multivariate_parameter`） | `Powell`、`maxfev=20` | 二つのσの例 | 目的関数の評価回数の上限と識別性を確認する |
| Viterbiの打ち切り | `truncate=4.0`（`viterbi_healpix`） | `decode_trajectories` は渡さない | fitの`truncate=5`と自動で一致しない |
| Viterbiの楕円体 | `viterbi_healpix` の `ellipsoid=None` は、格子に記録された楕円体（記録がなければ `"sphere"`）を使う。`EagerEstimator.decode` は予測器の楕円体を渡す | `decode_trajectories` 経由では格子の楕円体（WGS84） | 作用素は異なる（FFT は接平面、Viterbi はセル中心間の角距離）が、位置は同じ楕円体で計算される |
| Viterbiのσの割り当て | 遷移 $k-1\to k$ に `predictor_index[k-1]` を使う（フィルタと同じ） | 二つのσの例も同じ | 最後の時刻の添字は使われないが、範囲検査は全時刻に行われる。使われない遷移のσは遷移表を作らない |

`final=False`という引数だけを見て、終点情報を使っていないと判断しません。`combine_emission_pdf`が最後の観測スライスに終点因子（`final`）を掛ける経路もあるため、計算全体で何回条件付けされるかを確認します。

Completeの二つのσの例では、日別の`behav_found > 0`から`predictor_index`を作り（`stamp_parameter_indices_from_mask`）、グループごとに60／30 km/dayの速度尺度（`maximum_speed`と`maximum_speed / 2`）をσの探索上限とします。潜在的な行動状態の遷移確率を同時推定するモデルとは区別します。[最適化](https://github.com/pangeo-fish/pangeo-fish/blob/361e9b7/pangeo_fish/hmm/optimize/scipy.py)

## 6. 対象版・格子設定・依存パッケージ

### 6.1 ワークショップの設定

| 項目 | 内容 | 出典 |
|---|---|---|
| pangeo-fish | `main` のコミット `361e9b7`（`361e9b7639b09115c281e13c7fe78da22b2c1711`） | 本書の起動ガイド（`pangeo-eosc.md`） |
| 環境イメージ | `ghcr.io/pangeo-fish/pangeo-fish-notebook:2026.11.2` | 同上 |
| 格子 | WGS84 楕円体上の HEALPix（`ellipsoid = "WGS84"`）、レベル10 | Complete／Baseデモと日本語Notebook |
| 海マスク閾値 | `mask_threshold = 0.25`（`regrid_dataset_hpresample` の既定値は0.5） | 同上 |
| 移動 | `FFTConv` | 同上 |
| 軌跡 | `track_modes = ["viterbi_healpix", "mode", "mean"]` | 同上 |
| 潮汐 | `tide_method = "healpix"`、`tide_model = "tpxo9"` | Completeデモ（セル 7） |

格子は WGS84 のみを使います（Notebook の設定セルで `ellipsoid = "WGS84"`）。楕円体に関する `main` の挙動は[楕円体HEALPix](09_ellipsoidal_healpix.md)第7節にまとめました。

### 6.2 依存パッケージの版

pangeo-fish のリポジトリに記載されている版の情報は次のとおりで、いずれも**最低限の制約**または CI の固定値であり、実際に環境へ入った版ではありません。

| パッケージ | 読み取れる情報 | 出典 |
|---|---|---|
| pangeo-fish | 版番号は読み取れない（`setuptools_scm` が動的に決め、フォールバックは `999`）。コミット `361e9b7` で特定する | `pyproject.toml` |
| healpix-geo | `>=0.5`。デモ用 CI の固定値は `0.5.0` | `pyproject.toml`、`ci/requirements/demo-constraints.txt` |
| healpix-resample | `>=2026.11.2,<2027`。同固定値は `2026.11.2` | 同上 |
| healpix-analyse | `>=2026.11.1`。同固定値は `2026.11.1` | 同上 |
| xdggs | `==0.6.0` | `pyproject.toml` |
| PyFES | 任意の依存 `tide` として `pyfes>=2026.10`（コメントは Complete デモに必要で、PyPI に wheel がなく conda-forge を勧めると書く）。デモ用 CI は conda-forge の `pyfes==2026.10.0` を入れる | `pyproject.toml`、`ci/run_demo_notebook.sh` |
| xarray／zarr | `>=2025.7.1,<2027`／`>=3.1.2,<4` | `pyproject.toml` |

イメージに実際に入った版は、Complete デモ末尾の付録「Information for bug reports」のセルが表示します（pangeo-fish、xarray、dask、numpy、xdggs、healpix-geo、copernicusmarine）。解析結果の属性にも、pangeo-fish・healpix-convolution・xarray・xhealpixify の版が記録されます（`helpers._get_package_versions`）。PyFES の実際の版は、潮汐の予測に使った環境で別途記録します（どちらの方式でも必要です）。
