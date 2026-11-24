# 実装・パラメータ・対象版の対応

このページは、ワークショップで使う pangeo-fish（`361e9b7`）の Complete デモ（`notebooks/pangeo-fish-complete-demo.ipynb`）で、利用者が設定する項目をまとめたものです。**関数の既定値とノートブックで明示的に与えた値を別々に記します。** ワークショップの環境はイメージ `ghcr.io/pangeo-fish/pangeo-fish-notebook:2026.11.2` で、デモの HEALPix レベルは10です。

## 1. どこで何を設定するか

| 目的 | 主な関数 | 設定する項目 | 変えると何が変わるか |
|---|---|---|---|
| タグとモデルの温度差 | `compute_diff` | 深度、time bounds、`min_water_depth` | 比較するサンプル・モデル深度と有効セル |
| 水温の観測確率（emission probability） | `compute_emission_pdf` | `differences_std` | 温度差をどの程度許すか |
| 放流・終点 | `compute_emission_pdf` | `initial_std`, `recapture_std` | 既知位置を格子上でどれだけ広げるか |
| 音響 | `compute_acoustic_pdf` | `receiver_buffer` | 受信範囲 |
| 海底地形 | `compute_healpix_histogram_region_bin_size`、`batch_compute_pdf_bathy` | `depth_bin_size`等 | セル内の深度分布の表現と深さの整合 |
| 潮汐の区間検出 | `detect_tide` | `tideFL`・`tideLV`・`behavFL`・`behavLV`（窓長、RMSE・$R^2$・振幅の閾値） | どの区間に潮汐情報があるとみなすか |
| 潮汐（`healpix`、既定） | `still_tag_tide_likelihood` | `sigma`, `n_eff`, `water_column`等 | 波形のずれ、オフセット、観測の情報量 |
| 潮汐（`pedersen`） | `pedersen_tide_likelihood`、`cell_bathymetry`（セルの平均水深） | `window_hours`、誤差のパラメータ（`white_noise_sd`・`depth_offset_sd`等） | 時間相関のある誤差を考えた水深の比較。誤差パラメータは較正していません |
| 潮汐を総合 PDF に結合 | `write_tide_pdf_healpix` → `merge_tide_with_total` | なし | セル・日の対応、欠けた分の中立な因子 |
| 観測を組み合わせる | `normalize_pdf` → `combine_emission_pdf` | `excluded_pdf` | 掛け合わせる観測の種類 |
| 移動を推定する | `optimize_pdf` | `conv_method`, `maximum_speed`, `truncate`, `tolerance` | 移動の計算方法、σの探索範囲、数値精度 |
| 2種類の移動幅 | `stamp_parameter_indices_from_mask` と最適化 | `predictor_index`、行動フラグ | 各ステップで使うσ |
| 結果を要約する | `decode_trajectories` | `track_modes`（`mean`・`mode`・`viterbi_healpix`） | 平均・最頻・連続する最も尤もらしい経路 |

## 2. 水温・初期位置・音響

| 引数・設定 | 関数の既定値／要件 | デモの値 | 科学的・数値的意味 |
|---|---|---|---|
| `differences_std` | 必須 | 0.75 °C | 平均した符号付き温度差（モデルの温度の単位）に対する正規分布の標準偏差。センサー精度そのものではない |
| `initial_std` | 必須 | $10^{-4}$ rad | 放流位置まわりの正規分布の幅（rad は角度の単位ラジアン。地球の半径を掛けると距離になる） |
| `recapture_std` | 必須 | $10^{-4}$ rad | 終点イベントがある場合の広がり。`fish_death` イベントを参照する |
| `min_water_depth`（`compute_diff`） | `"auto"` | 指定しない | 干出するセルの扱い。数値ならm、`None` は保持する指定。`"auto"` では干出するセルがあるときだけ除外され、実際に起こるのは North-West Shelf の1時間値の場合に限る |
| `relative_depth_threshold` | 必須 | 0 | 現在は使われません。0 のままにしてください |
| `receiver_buffer` | 必須（長さの単位つき） | 2,000 m | 受信可能域を近似する半径 |
| `chunk_time` | 24 | **1**（デモで上書き） | 時間の処理チャンク（デモでは1時間ステップ分）であり、24時間の生物学的仮定ではない |

音響では、未検出（受信機の近くにいなかったという情報）はマスクとして使われます。

WGS84 の長半径6,378 kmを用いる単純な角度換算では、$10^{-4}$ radは約0.64 km、0.0003 radは約1.91 kmです。後者は日本語Baseの手動σ（`sigma=[0.0003]`）の例です。格子レベル10の代表長約6.4 kmより狭い幅も設定されているため、この数値をそのまま達成された位置精度と呼ぶことはできません。

## 3. 海底地形

| 引数・処理 | 関数の既定値 | Completeの設定 | 留意点 |
|---|---|---|---|
| `depth_bin_size` | 1（m） | 2 m | 深度ビンの幅（m）。尤度（likelihood）はビン内で線形補間されるので、幅を広げると海底の位置が最大1ビンぶんぼやける |
| `max_depth_m` | `None`（`nb_depth_bins` とどちらかが必須） | 1,000 m | 最後のビン境界がちょうど `max_depth_m` になる。デモでは500区間で、これより深い魚には「`max_depth_m` より深い海底の割合」が使われる |
| `depth_offset` | 0 | 指定なし | 魚と海底の間の余裕（m）。負の値なら、その分だけ海底より下を許す |
| `default_stdev_m` | 1（m） | 指定なし | 水深データに不確かさの値がない点に使う、水深の不確かさ（m） |
| `chunk_size` | 500 | 指定なし | 一度に読む緯度の行数 |
| `ellipsoid` | `"WGS84"` | `"WGS84"` | 地球の形。セルIDとセル中心の計算に渡される（[楕円体HEALPix](09_ellipsoidal_healpix.md)第7節） |
| `batch_compute_pdf_bathy` の `batch_size` | 50,000（セル） | 10,000（セル） | 一度に計算するセル数 |

水深の不確かさは誤差の仮定であり、推奨される測深誤差ではありません。ビン幅とは独立に m で与えます。

## 4. 潮汐

### 区間を選ぶ処理

`detect_tide`は、タグの深度記録に潮汐の波形が見える区間を自動で探します。既定の設定は、潮汐検出が窓25 h・RMSE 0.42 m未満・$R^2$ 0.85超・振幅0.6 m超（上限5 m未満）、行動フラグが窓25 h・RMSE 0.42 m未満・$R^2$ 0.70超・振幅0.2 m超（上限5 m未満）です。窓の長さは、主要な潮汐 M2 の周期 12.42 h 以上にします。フラグは窓の中心に記録され、有効なサンプルが80%未満の窓はフラグ0です。

各窓では、1次の傾きと周期12.42 hの波を当てはめます。これはタグの深度パターンの判定であり、独立な着底の観測ではありません。

### Complete デモの潮汐の設定

| 設定 | Complete デモの既定値 | 選択肢・意味 |
|---|---|---|
| `tide_method` | `"healpix"` | `"healpix"` または `"pedersen"`。どちらも `pyfes` が必要 |
| `tide_model` | `"tpxo9"` | `"tpxo9"`（Ifremer のデモ用データ）または `"fes2022b"`。FES2022b は `ellipsoid = "WGS84"` が必須 |
| `tide_model_source` | `None` | `None` なら公開の TPXO9 ファイル。FES2022b では、ローカルの `.nc` ファイルのパス |
| `tide_constants_store` | `None` | FES2022b の事前計算データ（`s3://` またはローカル）。`tide_model = "fes2022b"` かつ `tide_model_source` なしの場合のみ |
| `tide_s3_endpoint` | `None` | S3 互換のエンドポイント。`None` なら環境の S3 設定 |
| `tide_constituents` | `None` | `None` なら保存された分潮すべて。リストは FES2022b のみ、空リストは不可 |
| `tide_sigma_m` | 2.0 | `"healpix"` のみが使うモデル誤差（m）。`"pedersen"` で2.0以外にすると警告が出る |
| `tide_min_samples` | 6 | `"healpix"` のみ。1日に必要な有効な1時間平均の最低数 |

### `healpix` 方式の観測重み

| 引数 | `still_tag_tide_likelihood`の既定値 | デモで与える値 | 意味 |
|---|---|---|---|
| `sigma` | 必須 | 2 m（`tide_sigma_m`） | モデル誤差（潮汐モデル・高潮・センサー）の尺度。1時間内の変動ではない |
| `freq` | `"1h"` | 既定 | 観測と予測を同じサンプルで集約する時間単位 |
| `time_step` | `"1D"` | 既定 | 位置の重みを作る時間区間。ラベル $T$ は $(T-12\,\mathrm{h},\,T+12\,\mathrm{h}]$ |
| `min_samples` | 12 | 6（`tide_min_samples`） | 窓内の有効な集約サンプルの最低数。足りない窓は一様な重み |
| `n_eff` | `None`（窓内のサンプル数） | 既定 | 尤度（likelihood）の鋭さを左右する情報量 |
| `water_column` | `None` | 指定なし | 与えなければ各セル・窓で平均水深を推定。与えるときは平均海面基準の水深（m） |
| `valid` | `None` | `tide_found > 0` | 使用する観測のフラグ |
| `min_tidal_signal` | 0.05 m | 既定（効かない） | `detection_ratio` を指定したときだけ使われる最小信号 |
| `detection_ratio` | `None` | 指定なし | `None` ならモデルに基づく窓の判定をしない |

### `pedersen` 方式の観測重み

| 引数 | `pedersen_tide_likelihood`の既定値 | デモで与える値 | 意味 |
|---|---|---|---|
| `water_column` | 必須 | `cell_bathymetry` が GEBCO から作るセルの平均水深 | 平均海面基準の水深（m、正） |
| `tide_found`、`rmse` | 必須／`None` | `detect_tide` の `tide_found`、`rmse_tide` | 窓の中心のフラグと、当てはめの RMSE（当てはめの残りのずれの大きさ） |
| `window_hours` | 25 | `tag_test.attrs["tideFL"]` | 1つのフラグの窓長 |
| `freq` | `None` | 既定 | `None` ならサンプルをそのまま使う |
| `white_noise_sd` | 0.2 m | 既定 | センサーの白色ノイズ |
| `ar_decay_hours`、`ar_level` | 6.67 h、0.05 | 既定 | 時間相関が 0.05 まで下がるまでの時間 |
| `epsilon` | 0.4 m | 既定（RMSE が取れない窓のみ） | 時間相関の項の標準偏差の代わりの値 |
| `depth_offset_sd` | 10 m | 既定 | 平均水深に対する一定の標準偏差 |
| `bathy_variance` | 20 m² | `cell_bathymetry` の分散 | `non_tidal="bathymetry"` のときだけ効く |
| `non_tidal` | `"uniform"` | 既定 | 窓のない日の PDF（一様）。`"bathymetry"` は海底地形のみの尤度（likelihood） |
| `min_fraction`、`max_overlap_hours` | 0.8、1 h | 既定 | 候補の窓に必要なサンプルの割合、異なる日の窓が共有できる時間 |

これらの誤差パラメータは Pedersen らの MATLAB のコードの値で、このパッケージ向けには較正していません。

窓のない日の潮汐 PDF は、どちらの方式でも一様です。総合 PDF との結合（`merge_tide_with_total`）では、欠けたセルや日に一定の中立な因子が入ります。詳細は[潮汐](07_tides.md)3.4 節と[再格子化](09b_regridding_alignment.md)を参照します。

## 5. 移動と最適化

| 引数・設定 | 既定値 | デモの値 | 解釈 |
|---|---|---|---|
| `conv_method` | `"FFTConv"` | `"FFTConv"` | 移動の確率の計算方法（[計算](10_computing.md)第5節） |
| `maximum_speed` | 必須（速度の単位つき） | 60 km/day | σの探索上限を作る尺度。実現する移動距離の上限ではない |
| `adjustment_factor` | 必須 | 1 | 探索上限の倍率 |
| `truncate` | 必須（`None` 可。`HealpixConv` では `None` 不可） | 5 | 近傍を打ち切る幅（σの倍数） |
| `tolerance` | 必須 | $10^{-6}$ | σの探索を止める許容差 |
| `single_behav` | `True` | 1つのσのとき `True`、2つのσの例でも `True` | 複数のσのとき、行動の値ごとに1つのσを推定する（`False` は連続区間ごと） |
| `multivariate` | `False` | 二つのσの例で `True` | 全σを同時に最適化する |
| `final` | `False` | 指定なし | `True` で、最終状態が観測した最終位置と合うようにσを最適化する。2つのσ（`predictor_index`）とは併用不可 |
| `projection` | `"conservative"` | 既定 | `FFTConv` のみ |
| `normalization`、`land_barrier` | `"full_disc"`、`False` | 既定 | `HealpixAnalyseConv` のみ |

σの探索範囲は、下限が $10^{-4}$ rad、上限が `maximum_speed × Δt × adjustment_factor` を地球の半径で割った角度です。

`final=False`という引数だけを見て、終点情報を使っていないと判断しないでください。`combine_emission_pdf`が最後の観測に終点の情報を掛ける場合もあるため、計算全体で何回条件付けされるかを確認します。

Completeの二つのσの例では、日別の`behav_found > 0`から`predictor_index`を作り（`stamp_parameter_indices_from_mask`）、グループごとに60／30 km/dayの速度尺度（`maximum_speed`と`maximum_speed / 2`）をσの探索上限とします。行動の状態が切り替わる確率まで同時に推定するモデルとは別のものです。

## 6. 対象版・格子設定

| 項目 | 内容 |
|---|---|
| pangeo-fish | `main` のコミット `361e9b7`（`361e9b7639b09115c281e13c7fe78da22b2c1711`）、リリース 2026.11.2 |
| 環境イメージ | `ghcr.io/pangeo-fish/pangeo-fish-notebook:2026.11.2` |
| 格子 | WGS84 楕円体上の HEALPix（`ellipsoid = "WGS84"`）、レベル10 |
| 海マスク閾値 | `mask_threshold = 0.25`（`regrid_dataset_hpresample` の既定値は0.5） |
| 移動 | `FFTConv` |
| 軌跡 | `track_modes = ["viterbi_healpix", "mode", "mean"]` |
| 潮汐 | `tide_method = "healpix"`、`tide_model = "tpxo9"` |

格子は WGS84 のみを使います（ノートブックの設定セルで `ellipsoid = "WGS84"`）。

環境は `ghcr.io/pangeo-fish/pangeo-fish-notebook:2026.11.2` で固定されています。実際に入っているパッケージの版は、Complete デモ末尾の付録「Information for bug reports」のセルが表示します。
