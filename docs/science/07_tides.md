# 潮汐から位置を絞る：海面高度、着底区間、調和定数（仮）

この章では、タグの水深記録に現れる潮汐の形を、候補地点の予測潮汐と比べます。観測に必要なのは「水深が変化していること」に加え、その変化を海面の昇降として解釈できる区間です。

この章は、ワークショップで使う pangeo-fish（`361e9b7`）の Complete ノートブックに対応しています。詳しくは `pangeo_fish/tide.py`、`pangeo_fish/tide_healpix.py`、`docs/tide.rst` を見てください。

## 1. 海底に留まるタグが潮汐を記録する理由

平均海面を基準とする海底水深を $H_c>0$、海面高度を上向き正の $\eta_c(t)$ とします。海底の固定点にタグがある場合、水面から測った正の水深は

$$
d(t)=H_c+\eta_c(t)+\epsilon(t)
$$

となります。満潮では上にある水柱が厚くなり、タグの水深は増えます。一定の海底上高度 $h$ を許すなら $H_c$ を $D_c=H_c-h$ に置き換えられます。一方、魚の鉛直移動が大きければ、この単純な式だけで観測を説明できません。

この説明は、本教材の座標・符号の定義から得られる関係式です。歴史的な研究では、Metcalfe & Arnold (1997) が深度・水温を用いた魚の移動復元を示し、Hunter らの tidal location method が発展しました。Hunter et al. (2004) の実例では、海底に留まる区間の満潮時刻と潮差をモデルと照合しています。{cite:p}`Metcalfe1997,Hunter2004`

Hunter et al. (2003) は方法の原著候補です。原著の詳細な精度値や数式は、本章では引用していません。{cite:p}`Hunter2003`

## 2. 潮汐の検出と位置の尤度（likelihood）は異なる処理

Complete Notebook の潮汐の部分は、二段に分かれています。まず `detect_tide` が、水深時系列から「潮汐に似た形をしている区間」のフラグを作ります。次に、そのフラグを使う二つの方式（3 節）のどちらかが、候補セルごとの予測潮汐と比べて位置の重みを作ります。`detect_tide` 自体は位置を返しません。

### 2.1 検出（`detect_tide`）

| 処理 | 実装の挙動 | 科学的な読み方 |
|---|---|---|
| 時刻間隔の準備 | 10分（`DT_TARGET`）を対象とする。それより細かい記録は `resample(...).first()`（各10分間の最初のサンプル）で再標本化し、それより粗い記録は `NotImplementedError`。`smooth=True` のときだけ中央値フィルタでスパイクを置き換えるが、デモは指定しない | 平均化とは異なる前処理。元の記録間隔とサブサンプリングを記載する |
| 単位の検査 | 圧力の `units` 属性が dbar または m 以外なら `ValueError`。値が3000を超える、または −50 を下回る場合も `ValueError` | Pa や hPa のまま渡して潮汐の証拠が静かに消えるのを防ぐ |
| 規則格子と欠測 | 10分間隔の規則格子に置き、欠測は NaN のままにする。窓は常に同じ時間幅を持つ | 記録の欠落があっても窓の長さは変わらない |
| 窓 | 既定 25 時間（M2 の約2周期）。M2 の周期 12.42 時間より短い窓は `ValueError` | 窓を1サンプルずつずらす |
| 波形の当てはめ | 各窓で、1次の線形トレンドと周期 12.42 時間の正弦・余弦を最小二乗で当てはめる（平滑化はしない）。$R^2$ はトレンドを除いた系列に対して、「トレンドで説明されなかった分散のうち調和成分が説明する割合」として計算し、RMSE は全体の当てはめの残差から求める | 半日周に近い信号を探す処理。S2 などは当てはめず、残差に残す |
| 潮汐フラグ（`tide_found`） | RMSE < 0.42 m、$R^2>0.85$、0.6 m < 振幅 < 5 m（等号は含まない） | `detect_tide` を経由する既定値 |
| 行動フラグ（`behav_found`） | 窓は同じ25時間、RMSE < 0.42 m、$R^2>0.70$、0.2 m < 振幅 < 5 m | 同じ当てはめに緩い閾値を当てたもの。独立した行動分類でも、着底の直接観測でもない |
| フラグの位置 | 各フラグと各統計量は**窓の中心**のサンプルに記録される。窓内の有効サンプルが80%未満の窓は統計量が NaN でフラグ0 | 記録の最初と最後の約12.5時間にはフラグがない |

下位関数 `tide_behav_extr` の既定値（閾値は潮汐・行動ともに `[0.5, 0.7, 0.5]`）は `detect_tide` の既定値（`TIDE_PARAMS`）とは別なので、教材では呼び出す関数を必ず添えます。`detect_tide` に `tideLV` などを渡すとリスト全体が置き換わります。閾値を緩めて検出区間を増やすと、魚の鉛直行動を潮汐として取り込む可能性も検討対象になります。反対に厳しくすると、実際の潮汐区間を減らす場合があります。この魚のデータでどちらが起きるかは、比較実行によって確かめます。

上流の `docs/tide.rst` は、検出の限界として次の点を挙げています。

- **潮汐振幅が小さい海域は検出されません。** 振幅が 0.6 m 以上でなければならないので、M2 の振幅がそれより小さい海域（例として、バルト海や地中海）ではフラグが立ちません。
- **フラグが立つのは、海底に静止している魚の記録です。** 合成記録では、M2 と S2 の下で静止している魚はすべての窓で検出され、直線的な上昇、正弦波や矩形波の日周鉛直移動、ノイズは検出されませんでした。ただし、これらの試験は実際のタグを対象にしておらず、水柱内で潮流に乗る魚や、ほとんど着底しない魚では、フラグが立たない可能性があります。
- **窓とラベルの約束。** 窓は25時間、フラグは窓の中心に記録され、日 $T$ は $(T-12\,\mathrm{h},\,T+12\,\mathrm{h}]$ の区間です（水温の観測確率と同じ）。別のコミットで作った結果とは、窓とラベルの定義が同じか確認します。

実装出典：[単位の検査](https://github.com/pangeo-fish/pangeo-fish/blob/361e9b7/pangeo_fish/tide.py#L40-L82)、[当てはめと窓ごとの計算](https://github.com/pangeo-fish/pangeo-fish/blob/361e9b7/pangeo_fish/tide.py#L133-L365)、[既定値・前処理・`detect_tide`](https://github.com/pangeo-fish/pangeo-fish/blob/361e9b7/pangeo_fish/tide.py#L685-L792)。

### 2.2 日ごとの区間と、証拠のない日

位置の尤度（likelihood）は、日 $T$ ごとに $(T-12\,\mathrm{h},\,T+12\,\mathrm{h}]$ の区間で作られます（コードのコメントでは水温の観測確率の時刻ビンと同じ閉じ方に揃えたと説明されており、正午ちょうどのサンプルは日 $T$ に入ります）。**潮汐の窓がない日、つまり証拠のない日の潮汐 PDF は、方式によらず一様です。** これは「その日の潮汐からは絞らない」という意味であり、観測がないことを、潮汐のない場所である証拠には変えません。

## 3. Complete Notebook の二つの潮汐方式

Complete デモの設定セルの `tide_method` の既定値は `"healpix"` で、もう一つの選択肢が `"pedersen"` です。どちらも、セルごとの調和定数と PyFES（`pyfes` は任意の依存パッケージ。conda-forge から入れるのが勧められており、PyPI には wheel がありません）を使って、HMM の HEALPix セル上で潮汐を予測します。どちらも `pyfes` が入っていないと、設定セルの直後の検査（セル 8）が `ImportError` を出します。

予測の式（位相規約は `tide_healpix.py` の `PHASE_CONVENTION`）は、調和定数を複素数 $C_k=A_k e^{+iG_k}$ として実部・虚部の2変数（`tide_real`、`tide_imag`）で保存し、

$$
\eta_c(t)=\sum_k f_k(t) A_{kc}
\cos\{V_k(t)+u_k(t)-G_{kc}\}
$$

で与えられます。$A$ は m、$G$ は Greenwich phase lag、$f_k$、$V_k+u_k$ は PyFES が与える節点補正と天文引数です。ここで使われる分潮は保存された分潮のみで、保存されていない分潮は推定して補われません。

調和定数はセル中心で評価されるため、`cell_ids` に `level` と `ellipsoid` の属性が必要です（欠けると `ValueError`）。セル中心の緯度はその楕円体で計算され、`"WGS84"` は測地緯度を与えます。これが潮汐モデルの緯度に当たります（`tide_healpix.py` のモジュール docstring）。

### 3.1 既定の `"healpix"`：自由な平均水深を除いた波形照合

観測と予測潮汐を同じサンプル時刻で1時間ごとに平均し、日ごとに HEALPix 格子上の尤度（likelihood）を1つ作ります（`still_tag_tide_likelihood`）。1時間平均は、そのサンプルの平均時刻に帰属させます。区間は右側が閉じていて、1時間平均が二つの日にまたがらないようになっています。

デモは `valid=(tag_test.tide_found > 0)` を渡すので、使われるのはフラグが立ったサンプル（各窓の中心）だけです。各セル・各日で

$$
\widehat D_c=\overline{d-\eta_c},\qquad
r_c(t)=d(t)-\widehat D_c-\eta_c(t)
$$

を求め、

$$
\log w_c=-\frac{n_{\mathrm{eff}}}{2\sigma_{\mathrm{tide}}^2}
\overline{r_c(t)^2}
$$

を使います（ソースでは `loglik = -0.5 * n * mean(r**2) / sigma**2`。$n$ は `n_eff` が `None` のとき、その日の1時間平均の数）。平均水深 $D_c$ を候補ごとに最適化するため、これは平均を差し引いた時系列の形を照合する説明になります。$D_c$ の不確実性を積分した完全な周辺尤度（likelihood）とは別です。したがって**この方式は潮汐の形だけを使い、絶対水深の情報は Complete デモの別の海底地形の PDF から来ます**。

`sigma`（デモでは `tide_sigma_m = 2.0`）は、潮汐モデル・高潮・センサーの誤差であって、1時間内の水深の変動ではありません（docstring）。誤差は独立と仮定されます。有効な1時間平均が `min_samples`（デモでは `tide_min_samples = 6`、関数の既定は12）より少ない日は、一様な重みになります。有限の調和定数を持つ海のセルだけが候補になります。

| 引数・設定 | 関数の既定値／必要条件 | Complete デモの設定 | 解釈 |
|---|---|---|---|
| `sigma` | 必須（キーワード引数）、m | `tide_sigma_m = 2.0` | モデル誤差の尺度。`"pedersen"` では読まれない |
| `freq` | `"1h"` | 指定なし（既定） | 観測と予測を同じサンプル時刻で集約する間隔。`None` ならサンプルをそのまま使う |
| `time_step` | `"1D"` | 指定なし（既定） | 位置重みを作る窓（HMM の時間ステップ）。ラベル $T$ は $(T-12\,\mathrm{h},\,T+12\,\mathrm{h}]$ |
| `min_samples` | 12 | `tide_min_samples = 6` | 窓内の有効な集約サンプルがこれより少ないと一様な重み |
| `n_eff` | `None`：窓内のサンプル数を使う | 指定なし | 重みの鋭さに関係。窓の一部しか覆われないときは `n_eff` に被覆率を掛けた値を使う |
| `valid` | `None` | `tag_test.tide_found > 0` | 採用する観測。それ以外のサンプルは無視される |
| `water_column` | `None` | 指定なし | `None`：セル・窓ごとに平均水深を推定。与える場合は平均海面基準の水深（m、正）。最低天文潮位基準の海図（例：EMODnet DTM）は大潮差の大きい海域で数 m 深いので、事前の変換が必要 |
| `detection_ratio` | `None` | 指定なし | `None` のときモデルに基づく窓の判定を行わない |
| `min_tidal_signal` | 0.05 m | 指定なし | `detection_ratio` を指定したときだけ使われる。デモでは効かない |

実装出典：[`still_tag_tide_likelihood`](https://github.com/pangeo-fish/pangeo-fish/blob/361e9b7/pangeo_fish/tide_healpix.py#L488-L704)、[1時間平均](https://github.com/pangeo-fish/pangeo-fish/blob/361e9b7/pangeo_fish/tide_healpix.py#L419-L462)、[予測](https://github.com/pangeo-fish/pangeo-fish/blob/361e9b7/pangeo_fish/tide_healpix.py#L284-L341)。

### 3.2 `"pedersen"`：Pedersen et al. (2008) の潮汐尤度（likelihood）

`tide_method = "pedersen"` は、Pedersen et al. (2008) の潮汐尤度（likelihood）を、DTU の HMM 位置推定ツールの MATLAB コードから移植したものです。{cite:p}`Pedersen2008` 上流の `docs/tide.rst` は、MATLAB の出典を `cliu3/hmm_smast` の `datalik/datalikelihood.m` と `datalik/datalikparam.m`（ver. 0.52、2008）としています。実装は `pedersen_tide_likelihood` で、その docstring が MATLAB からの変更点をすべて列挙しています。移植が MATLAB 版と完全に同じ結果になるかは、この教材では扱いません。

**何を比べるか。** `detect_tide` が潮汐を見つけた窓ごとに、窓内の深度サンプル $\mathbf y$ を、セル $c$ で予測される水深のまわりのガウス分布に従う一つのベクトルとして扱います。

$$
\mu_c(t)=D_c+\eta_c(t),\qquad
\log L_c=\log\mathcal N(\mathbf y;\ \boldsymbol\mu_c,\ S)
$$

$D_c$ はセルの平均水深（m、正の向き、平均海面基準）、$\eta_c$ は 3 節の調和定数から求めた潮位です。窓は1時間平均せず、10分サンプルのまま使います（`freq=None`）。共分散 $S$ はセルに依存しないので、窓ごとに1回のコレスキー分解で全セルを計算し、計算は対数空間で行います。

**共分散 $S$（`pedersen_covariance`）。** サンプル間の時間差を $\tau$（時間）として、次の四つの和です。

- 白色ノイズ（センサー）：標準偏差 0.2 m
- 時間相関のある項（潮汐モデル誤差）：標準偏差はその窓の正弦当てはめの RMSE（`detect_tide` の `rmse_tide`。取れない場合は 0.4 m）。相関は 6.67 時間（40サンプル × 10分）で 0.05 まで下がる
- 平均水深に対する一定の標準偏差 10 m（`depth_offset_sd`）
- 潮汐の粗さの項：既定は 0（使わない）

平均水深の標準偏差が 10 m と大きいので、窓の内側では絶対水深の情報はほとんど効きません（上流の説明）。

**平均水深 $D_c$ の出どころ。** デモは `cell_bathymetry(subset_bathy.elevation, cell_ids)` で、第 6 節の GEBCO の部分集合から、各セルの海のサンプル点（標高が負の点）の水深の平均 `water_column`（正の向き）と、水深の分散 `bathy_variance`（最小 1 m²）を作ります。標高は平均海面基準でなければなりません。このうち分散は、証拠のない日にも海底地形だけの尤度（likelihood）を使う設定（`non_tidal="bathymetry"`、デモでは指定しない既定は `"uniform"`）でしか使われません。

**どの窓を使うか。** 日 $T$ には、中心が $(T-12\,\mathrm{h},\,T+12\,\mathrm{h}]$ にある窓のうち、当てはめの RMSE が最小の窓を最大1つ使います。窓は記録全体から RMSE の小さい順に選ばれ、期待サンプル数の80%（`min_fraction`）以上を持つ窓だけが候補です。同じサンプルを二重に数えないよう、異なる日の窓が共有できる時間は最大1時間です。25時間の窓では中心が24時間以上離れる必要があるので、隣の日の最良の窓が近くにある日は、窓を持てないことがあります（`tide_windows`）。

**証拠のない日。** 窓のない日は一様な PDF になります。理由は、デモの海底地形 PDF が既に「最深の深度より浅い海底にはいられない」を表しているためです。`non_tidal="bathymetry"` は MATLAB の海底地形だけの尤度（likelihood）を再現しますが、このとき海底地形を二重に数えることになります。

**誤差パラメータは未較正です。** `"pedersen"` の誤差パラメータは MATLAB コードのものであり、このパッケージ向けには較正されていません。上流の `docs/tide.rst` は特に次の点を挙げます。

- 平均水深の標準偏差 10 m により、潮汐の窓の内側では絶対水深がほとんど情報にならない（MATLAB と同じ）
- 時間相関の項は `detect_tide` の窓の RMSE を使い、検出の閾値がそれを 0.42 m 未満に保つ
- `bathy_variance`（`non_tidal="bathymetry"` のときだけ使用）の既定は、MATLAB ソースのデバッグ値 20 m²
- $D_c$ は GEBCO が平均海面基準であることを仮定しており、沿岸では成り立たないことがある

**二方式の比較と選び方**（上流の `docs/tide.rst` の整理による）

| | `"healpix"`（既定） | `"pedersen"` |
|---|---|---|
| 使うデータ | 水深と予測潮汐の1時間平均 | 潮汐フラグの立った窓の生のサンプル（1日1窓、25時間） |
| 平均水深 | 未知。セルと日ごとに推定。絶対水深は海底地形 PDF のみ | GEBCO のセル平均水深、標準偏差 10 m（弱い絶対水深情報） |
| 誤差 | 独立、標準偏差 `tide_sigma_m` | 時間相関あり（白色ノイズ、6.67 時間の記憶、一定のオフセット） |
| 窓のない日 | 一様 | 一様 |
| 由来 | このパッケージ向けに書かれた | 公表された方法の移植 |
| 既知の弱点 | 魚が静止していないと、潮汐振幅の小さいセルに偏る（観測振幅が予測より小さくなるため） | 海底地形の基準面に敏感。誤差パラメータは未較正。メモリは（窓のサンプル数）×（セル数）で増える |

上流は、海底地形が不確かな場合（沿岸、河口）には、平均水深を推定する `"healpix"` を、公表手法や MATLAB との比較が目的で海底地形が信頼できる場合には `"pedersen"` を使うよう勧め、どちらも既知の経路を持つタグで検証されていないと述べています。潮汐の証拠に頼る場合は、両方を実行して比べます。どちらも `detect_tide` が見つけた静止区間に頼るので、フラグが一つも立たない魚ではすべての日の PDF が一様になり、方式の違いは出ません。まず `tide_found` を確認します。

実装出典：[`tide_windows`](https://github.com/pangeo-fish/pangeo-fish/blob/361e9b7/pangeo_fish/tide_healpix.py#L724-L796)、[`pedersen_covariance`](https://github.com/pangeo-fish/pangeo-fish/blob/361e9b7/pangeo_fish/tide_healpix.py#L819-L861)、[`pedersen_tide_likelihood`](https://github.com/pangeo-fish/pangeo-fish/blob/361e9b7/pangeo_fish/tide_healpix.py#L890-L1196)、[`cell_bathymetry`](https://github.com/pangeo-fish/pangeo-fish/blob/361e9b7/pangeo_fish/tide_healpix.py#L1199-L1249)。

### 3.3 調和定数の供給元：TPXO9 と FES2022b

調和定数を得る経路は、Complete デモでは次の三つに分かれます（どちらの方式でも同じ）。

| `tide_model` | 調和定数の入手 | 条件 |
|---|---|---|
| `"tpxo9"`（既定） | `latlon_constants_from_tmd` で TMD3 形式の NetCDF を読み、位相を PyFES の基準に直したうえで、実部・虚部を `constants_to_healpix` で双一次補間してセル中心へ移す | `tide_model_source = None` なら Ifremer のデモ用ファイルを使う。ローカルの同形式ファイルも指定できる |
| `"fes2022b"`＋`tide_model_source` | AVISO+ のネイティブ格子（LGP2）のファイル `FES2022b_OceanTide_NSgrid.nc` から `fes2022b_constants_to_healpix` で PyFES の補間を使ってセル中心へ移す | `ellipsoid = "WGS84"` が必須（セル 8 の検査と、関数内の検査でどちらも `ValueError`） |
| `"fes2022b"`＋`tide_constants_store` | 事前に計算した調和定数の Zarr（ローカルまたは `s3://`）を `open_harmonic_constants` で読む | 同上。単位 m と位相規約が一致するか検証される。候補の全セルを含む必要があり（`require_all_cells=True`）、ネイティブ格子の外のセルは欠測値のまま保存される |

`tide_constituents` に分潮の名前のリストを渡すと、FES2022b の両経路で使う分潮を選べます（`None` ならすべて）。TPXO9 経路では指定できず、`tide_model` が `"fes2022b"` でないときに `tide_constituents` を与えると `ValueError` になります。デモが使うのは FES2022b の ocean tide の海面高度の分潮成分です（`docs/tide.rst`）。ネイティブ格子の外のセルでは調和定数が欠測となり、そのセルは候補から外れます。例えば `docs/tide.rst` は、ネイティブ格子が下流スヘルデ川の Bath 付近までで、Temse の放流地点はその外側だと述べています。

TPXO9 の経路は緯度・経度格子の定数を双一次補間し、FES2022b の経路はネイティブ格子上で PyFES の補間を使うため、補間法が異なります。結果の差を調べるときは、`scratch_root` を実行ごとに分け、同じ `time` と `cell_ids` で比較します（`docs/tide.rst`）。

### 3.4 総合 PDF への結合と、欠けているセル・日

`merge_tide_with_total` は、総合 PDF（`total_pdf.zarr`）のセルと日をすべて保ち、潮汐 PDF を `pdf_tide` として加えます。`initial`・`final`・`mask` は変更しません。

- `grid_name`・`level`・`indexing_scheme`・`ellipsoid` の属性が潮汐のストアと総合 PDF で食い違うと `ValueError` になります。
- 潮汐の格子にないセル、調和定数（`"pedersen"` では水深も）のないセル、潮汐のストアにない日、証拠のない日（`has_likelihood` が0の日）には、**一定の中立な因子**が入ります。これらは「不可能」ではなく「不明」として扱われます。証拠のない日は全セルで $1/n_{\mathrm{cells}}$、一部のセルだけが欠ける日は、その日の利用可能な値の平均です。件数は警告で報告されます。
- 日ごとの `tide_found`・`behav_found` は、ストアにない日を0として別の変数（`tide_mask`・`behav_mask`）で返されます。

実装出典：[`merge_tide_with_total`](https://github.com/pangeo-fish/pangeo-fish/blob/361e9b7/pangeo_fish/tide.py#L929-L1078)、[`write_tide_pdf_healpix`](https://github.com/pangeo-fish/pangeo-fish/blob/361e9b7/pangeo_fish/tide_healpix.py#L1392-L1453)。

## 4. 短い窓で何ができるか

M2 と S2 の角速度をそれぞれ $28.9841042$、$30.0000000$ 度／時間とすると、二つの周期の相対位相が一周する時間は

$$
T_{\mathrm{beat}}=\frac{360}{30-28.9841042}
\simeq 354.37\ \mathrm{h}\simeq14.77\ \mathrm{days}.
$$

角速度は NOAA の分潮表で確認しました。上の値は、その角速度から本教材で計算したものです。14.77日は分潮分離の代表的な目安であり、信号対雑音比や解析法を無視した絶対的な境界ではありません。{cite:p}`NOAA2006,Parker2007`

25時間の検出窓や1日の位置尤度（likelihood）窓を使うことは、M2・S2 の未知の振幅と位相をタグだけから独立に精密推定できることを意味しません（`lssinfit` の docstring も、M2 と S2 は約15日より短い窓では分離できないので S2 は残差に任せる、と述べています）。一方、海洋モデルが候補ごとの調和定数を既に与えているなら、その予測波形を短い記録と比較することはできます。**未知の分潮を分離する問題と、既知の候補波形を照合する問題を分けます。**

この違いは `harmonic_analysis` と、二つの尤度（likelihood）関数の説明にも反映します。前者の分潮分離診断は既定の位置尤度（likelihood）そのものではありません。また、波形照合を行うために FFT を使う必要はありません。`FFTConv` は HMM の空間的な移動計算に使われる名称であり、潮汐の周波数分析を意味しません。

## 5. TPXO、FES2022b、PyFES の出典を分ける

| 引用対象 | 教材で付ける出典 | 役割 |
|---|---|---|
| TPXO のモデル化 | Egbert & Erofeeva (2002) と OSU の使用版ページ | モデルの考え方と、実際に使った TPXO9 の版を記録 |
| FES2022b データ | CNES (2024), DOI `10.24400/527896/A01-2024.004` | 使用したデータへの引用 |
| FES2022 の科学的説明 | Lyard et al. (2026), DOI `10.5194/egusphere-2026-6805` | 2026-11-23時点で査読中のプレプリントと明記 |
| FES2014 の設計・検証 | Lyard et al. (2021) | 先行モデルの論文。FES2022b の検証論文として代用しない |
| 潮汐予測ソフトウェア | CNES PyFES の公式資料と使用バージョン（`pyproject.toml` の任意依存 `tide` は `pyfes>=2026.10`。実際に入った版は実行環境で確認する） | 調和定数を時系列へ変換する計算系の出典 |
| 潮汐尤度（likelihood）の方法 | Pedersen et al. (2008)（`"pedersen"` 方式） | 公表された方法と、その移植であることの記録 |

FES2022b の配布元は規則格子とネイティブ格子を区別しています。本教材では、Complete デモが利用するネイティブ LGP2 データまたは事前計算 Zarr の来歴を記します。海面高度の ocean tide と loading tide を混同せず、タグ水深で観測している量に対して必要な項を確認します。{cite:p}`Egbert2002,TPXOOfficial,CNESFES2022,AVISOFES2022Handbook,Lyard2026Preprint,Lyard2021,PyFESOfficial,Pedersen2008`

コードでは、`latlon_constants_from_tmd` が TPXO/TMD の位相を PyFES の Greenwich 天文引数の基準へ変換し（docstring によれば TPXO9 ファイルではこの補正は S1 の180度だけ）、`constants_to_healpix` が複素調和定数の実部 $A\cos G$・虚部 $A\sin G$ を双一次補間してセル中心へ移します。振幅と位相は直接補間しません。これは位相が $359^\circ$ と $1^\circ$ の近傍で単純な角度平均を取るような不連続を避ける設計です。元データの陸の点は除外して重みを再正規化します。`fill_distance_km` を指定すれば近い補間済みセルの値で海岸の欠測を埋められるが、既定は `None` で、Complete デモは指定しません。docstring は、この双一次補間が元データと同程度かそれより細かいセルを想定しており、粗いセルには面積重み平均が必要だと述べています。再格子化した場が沿岸の細かな潮汐を復元できるとは限りません。欠測セルを補間で埋める範囲や境界の扱いも記録します。

実装出典：[`latlon_constants_from_tmd`](https://github.com/pangeo-fish/pangeo-fish/blob/361e9b7/pangeo_fish/tide_healpix.py#L1502-L1550)、[`constants_to_healpix`](https://github.com/pangeo-fish/pangeo-fish/blob/361e9b7/pangeo_fish/tide_healpix.py#L1586-L1650)、[`fes2022b_constants_to_healpix`](https://github.com/pangeo-fish/pangeo-fish/blob/361e9b7/pangeo_fish/tide_healpix.py#L1653-L1743)。

## 6. 面談で確認したい条件と比較実験

1. 固定点または着底に近い区間がありますか。単なる半日周期の鉛直行動との区別はできますか。`tide_found` が立つ日はどれだけありますか。
2. 圧力が m（または dbar）に変換されていますか（`detect_tide` は単位を検査します）。時計の UTC、時差、ドリフト、記録欠落を確認しましたか。
3. 対象海域で候補セル間の潮汐波形が十分に違いますか。同じ波形が複数海域に現れていませんか。振幅が小さい海域では検出自体が起きません。
4. 同じデータで `"healpix"` と `"pedersen"` を比較するとき、絶対水深の使用（海底地形の基準面を含む）、時刻原点、単位、位相、集約方法（1時間平均か生のサンプルか）を揃えましたか。
5. 同じ水深記録から潮汐項と海底地形項を作るため、統合で情報を強く数え過ぎていませんか。

最後の点は、独立性が自動的に保証されないというモデル上の論点です。`"healpix"` は潮汐項から絶対水深を除くが、両項が同じタグに由来することは残ります。`"pedersen"` は平均水深を弱い情報として使うため、海底地形項との重複を別に確認します。潮汐あり／なし、海底地形あり／なしの4条件で、経路だけでなく分布の広がりを比較する計画が適しています。ここに示したのは比較の進め方の提案で、実際の魚での改善率は示していません。
