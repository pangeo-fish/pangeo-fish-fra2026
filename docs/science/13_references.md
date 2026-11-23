# 参考文献・データ出典と、確認した範囲

この一覧は「どの説明に、どの文献を使うか」を示します。論文の方法、ワークショップのノートブックの実装、将来試す比較実験を同一視しません。実装の説明は、ワークショップで固定したpangeo-fishのコミット`af4fe17`に基づき、論文の記述からコードの挙動を推測したものではありません。

以下の「本文」は関連する方法節等を確認したことを指し、論文全体の再現実験を行ったという意味ではありません。「要旨」「書誌」のみの文献は、その範囲で利用しています。DOIのある文献は、2026年11月23日にCrossref（データセットはDataCite）の記録で著者・題名・掲載誌・巻・ページ・年を照合し、DOIのないウェブ資料は同日にページが存在し題名が一致することを確認しました。「本文」と記した確認範囲は、この照合より前の調査で付けた区分をそのまま残したもので、上位の区分に引き上げてはいません。

## 1. 研究の系譜・HMM・検証

| 文献 | 本資料で読む目的 | 確認範囲・扱い |
|---|---|---|
| Magin et al. (2026), *pangeo-fish: A Python package for studying fish movement using biologging and earth science data*. [DOI](https://doi.org/10.21105/joss.08332) | ソフトウェア自体の引用 | JOSSの公開論文と書誌。個々の現行パラメータの根拠はコード調査 |
| Pedersen et al. (2008), *Geolocation of North Sea cod … using Hidden Markov Models and behavioural switching*. [DOI](https://doi.org/10.1139/F08-144) | HMMを使う魚の位置推定の背景 | 著者所属機関の書誌・要旨。Completeの二つのσと同一モデルとはしない |
| Thygesen et al. (2009), *Geolocating Fish Using Hidden Markov Models and Data Storage Tags*. [DOI](https://doi.org/10.1007/978-1-4020-9640-2_17) | HMMと記録型タグをつなぐ解説 | 書誌（Crossref）を確認。要旨・章の本文は未取得 |
| Woillez et al. (2016), *A HMM-based model to geolocate pelagic fish from high-resolution individual temperature and depth histories …*. [DOI](https://doi.org/10.1016/j.ecolmodel.2015.10.024) | 水温・深度と移動モデルを結び付ける先行法 | 著者公開PDFの方法節・式を確認。現在の平均符号付き残差とは区別 |
| Braun et al. (2018), *HMMoce: An R package for improved geolocation …*. [DOI](https://doi.org/10.1111/2041-210X.12959) | 他のHMM構成（水温・深度の記録と海洋データの統合）を比較する | 公開本文の関連節。Crossrefのオンライン公開日は2018年1月23日、巻号は2018年5月 |
| Gatti et al. (2021), *A review and tests of validation and sensitivity of geolocation models for marine fish tracking*. [DOI](https://doi.org/10.1111/faf.12568) | 独立位置による検証と感度分析を設計する | 公開本文の検証・感度に関する節 |
| Gonse et al. (2025), *Combining acoustic telemetry with archival tagging … Pollachius pollachius*. [DOI](https://doi.org/10.1111/jfb.15750) | Pangeo-Fishに近い魚種・観測の応用例 | 公開本文、特に方法節2.7。先行公開2024年・巻号掲載2025年を区別 |

書誌参照：{cite:p}`Magin2026,Pedersen2008,Thygesen2009,Woillez2016,Braun2018,Gatti2021,Gonse2025`。

## 2. 音響・海底地形・潮汐による位置情報

| 文献 | 本資料で読む目的 | 確認範囲・扱い |
|---|---|---|
| Metcalfe & Arnold (1997), *Tracking fish with electronic tags*. [DOI](https://doi.org/10.1038/42622) | 環境履歴による位置推定の歴史 | 書誌（Crossref）を確認。要旨・本文は未取得 |
| Hunter et al. (2003), *Geolocation of free-ranging fish … I. Tidal location method*. [DOI](https://doi.org/10.1007/s00227-002-0984-5) | 潮汐位置推定の方法原著をたどる | 書誌をCrossrefで照合。原著の本文・要旨は未取得 |
| Hunter et al. (2004), *Impacts of migratory behaviour on population structure in North Sea plaice*. [DOI](https://doi.org/10.1111/j.0021-8790.2004.00801.x) | 着底中の潮汐を使う研究例 | 公開本文の関連する方法節 |
| Goossens et al. (2023), *Acoustic and archival technologies join forces: A combination tag*. [DOI](https://doi.org/10.1111/2041-210X.14045) | 音響と記録型タグの統合 | 著者機関の書誌と公開PDFの方法 |
| Huveneers et al. (2016), *The influence of environmental parameters on the performance and detection range of acoustic receivers*. [DOI](https://doi.org/10.1111/2041-210X.12520) | 一定受信半径の仮定を評価する | 公開本文のレンジ試験。対象海域の校正値へ直接転用しない |
| Hostetter & Royle (2020), *Movement-assisted localization from acoustic telemetry data*. [DOI](https://doi.org/10.1186/s40462-020-00199-6) | 検出過程を明示する別のモデル構成 | 公開本文。現在の二値フットプリント法の実装説明ではない |
| Nielsen et al. (2019), *Effect of study area bathymetric heterogeneity on parameterization and performance of a depth-based geolocation model for demersal fishes*. [DOI](https://doi.org/10.1016/j.ecolmodel.2019.03.023) | 地形・格子幅・深度分布の感度分析 | 書誌（Crossref）を確認。要旨・本文は未取得 |

書誌参照：{cite:p}`Metcalfe1997,Hunter2003,Hunter2004,Goossens2023,Huveneers2016,Hostetter2020,Nielsen2019`。

## 3. 潮汐モデルの論文とデータを別々に引用する

| 出典 | 何を記録するか | 本資料での位置づけ |
|---|---|---|
| Egbert & Erofeeva (2002), *Efficient Inverse Modeling of Barotropic Ocean Tides* | [出版社](https://journals.ametsoc.org/view/journals/atot/19/2/1520-0426_2002_019_0183_eimobo_2_0_co_2.xml)、DOIはBibTeXに収録 | TPXO公式が示す基礎文献。今回本文は取得できず、公式モデル説明と書誌を確認 |
| [TPXO公式モデル資料](https://www.tpxo.net/global) | TPXO9等のモデル名、解像度、取得ファイルと版 | モデル系列と実際の入力データを特定する |
| CNES (2024), FES2022 (Finite Element Solution) Ocean Tide（データセット） | [データDOI](https://doi.org/10.24400/527896/A01-2024.004)、FES2022bの実ファイル版 | データセットの引用。論文の代わりではない |
| [FES2022 handbook](https://aviso.altimetry.fr/fileadmin/documents/data/tools/hdbk_FES2022.pdf) | 格子、単位、分潮、配布形式 | 配布元の技術説明。実行記録にダウンロード版も残す |
| Lyard et al. (2026), *FES2022 global tide atlas: a step towards SWOT-compliant tidal corrections* | [プレプリントDOI](https://doi.org/10.5194/egusphere-2026-6805) | 2026年11月11日公開。EGUsphereのページに、2026年11月23日時点で「open for discussion and under review for Ocean Science」と表示されている。出版済みの最終論文とはしない |
| Lyard et al. (2021), *FES2014 global ocean tide atlas: design and performance* | [DOI](https://doi.org/10.5194/os-17-615-2021) | FES2014の公開論文。FES2022の検証結果を示す論文として引用しない |
| [PyFES公式資料](https://github.com/CNES/aviso-fes) | 予測ライブラリの版、調和定数の規約と入力形式 | 潮汐モデル、予測ソフトウェア、魚の観測モデルは別々に記録する |
| NOAA分潮資料・Parker (2007) | [分潮表を含む技術資料・付録C](https://tidesandcurrents.noaa.gov/ofs/publications/CS_Techrpt_024_SkillAss_WLsCUs_2006.pdf)、[Tidal Analysis and Prediction](https://tidesandcurrents.noaa.gov/publications/Tidal_Analysis_and_Predictions.pdf) | 潮汐周期と分潮分離の背景。M2/S2の約14.77日は角速度から本教材で計算 |

書誌参照：{cite:p}`Egbert2002,TPXOOfficial,CNESFES2022,AVISOFES2022Handbook,Lyard2026Preprint,Lyard2021,PyFESOfficial,NOAA2006,Parker2007`。

## 4. HEALPix・楕円体・DGGS

| 出典 | 本資料で読む目的 | 確認範囲・扱い |
|---|---|---|
| Górski et al. (2005), *HEALPix: A Framework for High-Resolution Discretization and Fast Analysis of Data Distributed on the Sphere*. [DOI](https://doi.org/10.1086/427976) | 等積性、階層、等緯度環という構成 | 公開本文。地球楕円体の処理は別の資料で補う |
| Calabretta & Roukema (2007), *Mapping on the HEALPix grid*. [DOI](https://doi.org/10.1111/j.1365-2966.2007.12297.x) | 投影・地図表現をさらに読む | 書誌（Crossref）を確認。関連する追加文献 |
| Karney (2024), *On auxiliary latitudes*. [DOI](https://doi.org/10.1080/00396265.2023.2217604) | 測地緯度、地心緯度、等積緯度を区別する | 公開PDF。Crossrefのオンライン公開は2023年6月、巻号年は2024年 |
| Odaka et al. (2026), *Grid4Earth: An Open-Source Python Ecosystem for Geospatial Data Integration Using an Ellipsoidal HEALPix DGGS*. [DOI](https://doi.org/10.5194/isprs-archives-L-4-W1-2026-189-2026) | 楕円体HEALPixの地球科学への適用 | 出版社公開本文と書誌 |
| [HEALPix Primer](https://healpix.sourceforge.io/html/intro_Geometric_Algebraic_Propert.htm) | RING/NESTED、親子関係、セル構成 | 公式技術資料 |
| [healpix-geoの参照系](https://healpix-geo.readthedocs.io/en/latest/reference-system.html)・[座標変換API](https://healpix-geo.readthedocs.io/en/latest/generated/healpix_geo.nested.lonlat_to_healpix.html) | 数式と実際の引数を結び付ける | 公式文書。インストール版のAPIを実習前に照合 |
| [PROJ HEALPix](https://proj.org/en/stable/operations/projections/healpix.html) | 球面と楕円体の扱い | 公式技術資料 |
| [OGC Topic 21](https://docs.ogc.org/as/20-040r3/20-040r3.html) | DGGSの概念モデル | Abstract Specification。Web API仕様とは別文書 |
| [OGC API – DGGS Part 1: Core](https://docs.ogc.org/is/21-038r1/21-038r1.html) | DGGSを扱うAPIの枠組み | 公式仕様。現行Pangeo-Fishがすべてを実装するという意味ではない |

書誌参照：{cite:p}`gorski2005healpix,calabretta2007mapping,karney2024auxiliary,odaka2026grid4earth,healpix_primer,healpixgeo_reference,healpixgeo_lonlat,proj_healpix,ogc2021dggs,ogc2025apidggs`。

## 5. 海洋データと計算環境

| 出典 | 記録・参照する内容 |
|---|---|
| [GEBCO_2024 Grid](https://www.gebco.net/data-products-gridded-bathymetry-data/gebco2024-grid)、[データDOI](https://doi.org/10.5285/1c44ce99-0a0d-5f4f-e063-7086abc0ea0f) | 標高の符号、格子間隔、基準面、TID、取得版。局所的な測深精度とは分ける |
| [IBI再解析](https://data.marine.copernicus.eu/product/IBI_MULTIYEAR_PHY_005_002/description) | 製品ID、dataset ID、変数、時間平均、取得版 |
| [GLORYS12V1](https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_PHY_001_030/description)、[製品DOI](https://doi.org/10.48670/moi-00021) | 全球プロダクトの仕様。日本周辺の適合性は別途評価する |
| [TEOS-10 / GSW](https://www.teos-10.org/pubs/gsw/v3_04/html/gsw_z_from_p.html) | 圧力から高さ・水深への変換における単位・緯度・符号 |
| [Xarray open_zarr](https://docs.xarray.dev/en/stable/generated/xarray.open_zarr.html)・[DataTree](https://docs.xarray.dev/en/stable/user-guide/data-structures.html#datatree) | 座標付き配列、階層、読み込み時のチャンクの意味 |
| [Dask Array](https://docs.dask.org/en/stable/array-best-practices.html)・[Zarr](https://zarr.readthedocs.io/en/stable/user-guide/performance/) | 保存と計算のチャンク、メモリとI/Oの設計 |

書誌参照：{cite:p}`GEBCO2024,IBIOfficial,GLORYSOfficial,GSWPressureDepth,XarrayOpenZarr,XarrayDataTree,DaskArrayGuide,ZarrPerformance`。

## 6. 実装の出典を残す

実装について引用するときは、論文のDOIに加えて、pangeo-fishのコミット（ワークショップでは`5cffccc`）、ノートブック名、データ製品と版、実行したPython環境を記録してください。プルリクエストの説明は、PR番号だけでなくheadのコミットも残してください。実行環境のイメージタグだけでは、実際にimportされたパッケージの版を確認したことにはなりません。

この資料のBibTeXは`references_fra.bib`に収録しています。ブック全体の文献一覧`references.bib`とはDOI・題名で照合済みで、同じ文献を二重に登録していません。
