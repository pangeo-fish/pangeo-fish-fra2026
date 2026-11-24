# 参考文献・データ出典

この一覧は、どの説明にどの文献を使うかを示します。論文の方法、ワークショップのノートブックの実装、これから試す比較実験は、別のものとして区別して読んでください。

## 1. 研究の系譜・HMM・検証

| 文献 | 何のために読むか | 読むときの注意 |
|---|---|---|
| Magin et al. (2026), *pangeo-fish: A Python package for studying fish movement using biologging and earth science data*. [DOI](https://doi.org/10.21105/joss.08332) | ソフトウェア自体の引用 | ソフトウェアとして引用するときの論文です。個々のパラメータの値の根拠は、{doc}`11_parameters_versions` を見てください |
| Pedersen et al. (2008), *Geolocation of North Sea cod … using Hidden Markov Models and behavioural switching*. [DOI](https://doi.org/10.1139/F08-144) | HMMを使う魚の位置推定の背景 | Complete ノートブックの二つのσと、この論文のモデルは同じではありません。`tide_method = "pedersen"` は、この論文の潮汐尤度（likelihood）を移したもので（`docs/tide.rst` に説明があります）、MATLAB 版と完全に同じ結果になるかは、この教材では扱いません。誤差パラメータは較正していません |
| Thygesen et al. (2009), *Geolocating Fish Using Hidden Markov Models and Data Storage Tags*. [DOI](https://doi.org/10.1007/978-1-4020-9640-2_17) | HMMと記録型タグをつなぐ解説 | — |
| Woillez et al. (2016), *A HMM-based model to geolocate pelagic fish from high-resolution individual temperature and depth histories …*. [DOI](https://doi.org/10.1016/j.ecolmodel.2015.10.024) | 水温・深度と移動モデルを結び付ける先行法 | 現在のノートブックが使う平均符号付き残差とは、式が違います |
| Braun et al. (2018), *HMMoce: An R package for improved geolocation …*. [DOI](https://doi.org/10.1111/2041-210X.12959) | 他のHMM構成（水温・深度の記録と海洋データの統合）を比較する | — |
| Gatti et al. (2021), *A review and tests of validation and sensitivity of geolocation models for marine fish tracking*. [DOI](https://doi.org/10.1111/faf.12568) | 独立位置による検証と感度分析を設計する | — |
| Gonse et al. (2025), *Combining acoustic telemetry with archival tagging … Pollachius pollachius*. [DOI](https://doi.org/10.1111/jfb.15750) | Pangeo-Fishに近い魚種・観測の応用例 | 特に方法の節（2.7）を読みます |

書誌参照：{cite:p}`Magin2026,Pedersen2008,Thygesen2009,Woillez2016,Braun2018,Gatti2021,Gonse2025`。

## 2. 音響・海底地形・潮汐による位置情報

| 文献 | 何のために読むか | 読むときの注意 |
|---|---|---|
| Metcalfe & Arnold (1997), *Tracking fish with electronic tags*. [DOI](https://doi.org/10.1038/42622) | 環境履歴による位置推定の歴史 | — |
| Hunter et al. (2003), *Geolocation of free-ranging fish … I. Tidal location method*. [DOI](https://doi.org/10.1007/s00227-002-0984-5) | 潮汐位置推定の方法原著をたどる | — |
| Hunter et al. (2004), *Impacts of migratory behaviour on population structure in North Sea plaice*. [DOI](https://doi.org/10.1111/j.0021-8790.2004.00801.x) | 着底中の潮汐を使う研究例 | — |
| Goossens et al. (2023), *Acoustic and archival technologies join forces: A combination tag*. [DOI](https://doi.org/10.1111/2041-210X.14045) | 音響と記録型タグの統合 | — |
| Huveneers et al. (2016), *The influence of environmental parameters on the performance and detection range of acoustic receivers*. [DOI](https://doi.org/10.1111/2041-210X.12520) | 一定受信半径の仮定を評価する | レンジ試験の結果です。自分の海域の校正値として、そのまま使うことはできません |
| Hostetter & Royle (2020), *Movement-assisted localization from acoustic telemetry data*. [DOI](https://doi.org/10.1186/s40462-020-00199-6) | 検出過程を明示する別のモデル構成 | pangeo-fish の現在の方法（受信範囲を二値で表す方法）の説明ではありません |
| Nielsen et al. (2019), *Effect of study area bathymetric heterogeneity on parameterization and performance of a depth-based geolocation model for demersal fishes*. [DOI](https://doi.org/10.1016/j.ecolmodel.2019.03.023) | 地形・格子幅・深度分布の感度分析 | — |

書誌参照：{cite:p}`Metcalfe1997,Hunter2003,Hunter2004,Goossens2023,Huveneers2016,Hostetter2020,Nielsen2019`。

## 3. 潮汐モデルの論文とデータを別々に引用する

| 出典 | 内容 | この資料での使い方 |
|---|---|---|
| Egbert & Erofeeva (2002), *Efficient Inverse Modeling of Barotropic Ocean Tides* | [出版社](https://journals.ametsoc.org/view/journals/atot/19/2/1520-0426_2002_019_0183_eimobo_2_0_co_2.xml)、DOIはBibTeXに収録 | TPXO の基礎になる論文です |
| [TPXO公式モデル資料](https://www.tpxo.net/global) | TPXO9等のモデル名、解像度、取得ファイルと版 | モデル系列と実際の入力データを特定する |
| CNES (2024), FES2022 (Finite Element Solution) Ocean Tide（データセット） | [データDOI](https://doi.org/10.24400/527896/A01-2024.004)、FES2022bの実ファイル版 | データセットの引用。論文の代わりではない |
| [FES2022 handbook](https://aviso.altimetry.fr/fileadmin/documents/data/tools/hdbk_FES2022.pdf) | 格子、単位、分潮、配布形式 | 配布元の技術説明。実行記録にダウンロード版も残す |
| Lyard et al. (2026), *FES2022 global tide atlas: a step towards SWOT-compliant tidal corrections* | [プレプリントDOI](https://doi.org/10.5194/egusphere-2026-6805) | 2026年11月時点では査読中のプレプリントです。出版された論文としては引用しません |
| Lyard et al. (2021), *FES2014 global ocean tide atlas: design and performance* | [DOI](https://doi.org/10.5194/os-17-615-2021) | FES2014の公開論文。FES2022の検証結果を示す論文として引用しない |
| [PyFES公式資料](https://github.com/CNES/aviso-fes) | 予測ライブラリの版、調和定数の規約と入力形式 | 潮汐モデル、予測ソフトウェア、魚の観測モデルは別々に記録する |
| NOAA分潮資料・Parker (2007) | [分潮表を含む技術資料・付録C](https://tidesandcurrents.noaa.gov/ofs/publications/CS_Techrpt_024_SkillAss_WLsCUs_2006.pdf)、[Tidal Analysis and Prediction](https://tidesandcurrents.noaa.gov/publications/Tidal_Analysis_and_Predictions.pdf) | 潮汐周期と分潮分離の背景。M2/S2の約14.77日は角速度から本教材で計算 |

書誌参照：{cite:p}`Egbert2002,TPXOOfficial,CNESFES2022,AVISOFES2022Handbook,Lyard2026Preprint,Lyard2021,PyFESOfficial,NOAA2006,Parker2007`。

## 4. HEALPix・楕円体・DGGS

| 出典 | 何のために読むか | 読むときの注意 |
|---|---|---|
| Górski et al. (2005), *HEALPix: A Framework for High-Resolution Discretization and Fast Analysis of Data Distributed on the Sphere*. [DOI](https://doi.org/10.1086/427976) | 等積性、階層、等緯度環という構成 | 地球が楕円体であることの扱いは、この論文にはありません。ほかの資料で補います |
| Calabretta & Roukema (2007), *Mapping on the HEALPix grid*. [DOI](https://doi.org/10.1111/j.1365-2966.2007.12297.x) | 投影・地図表現をさらに読む | 関連する追加の文献です |
| Karney (2024), *On auxiliary latitudes*. [DOI](https://doi.org/10.1080/00396265.2023.2217604) | 測地緯度、地心緯度、等積緯度を区別する | — |
| Odaka et al. (2026), *Grid4Earth: An Open-Source Python Ecosystem for Geospatial Data Integration Using an Ellipsoidal HEALPix DGGS*. [DOI](https://doi.org/10.5194/isprs-archives-L-4-W1-2026-189-2026) | 楕円体HEALPixの地球科学への適用 | — |
| [HEALPix Primer](https://healpix.sourceforge.io/html/intro_Geometric_Algebraic_Propert.htm) | RING/NESTED、親子関係、セル構成 | 公式の技術資料です |
| [healpix-geoの参照系](https://healpix-geo.readthedocs.io/en/latest/reference-system.html)・[座標変換API](https://healpix-geo.readthedocs.io/en/latest/generated/healpix_geo.nested.lonlat_to_healpix.html) | 数式と実際の引数を結び付ける | インストールした版の API は、実習の前に確かめてください |
| [PROJ HEALPix](https://proj.org/en/stable/operations/projections/healpix.html) | 球面と楕円体の扱い | 公式の技術資料です |
| [OGC Topic 21](https://docs.ogc.org/as/20-040r3/20-040r3.html) | DGGSの概念モデル | 概念モデルを定めた文書です。Web API の仕様とは別の文書です |
| [OGC API – DGGS Part 1: Core](https://docs.ogc.org/is/21-038r1/21-038r1.html) | DGGSを扱うAPIの枠組み | 公式の仕様です。pangeo-fish がそのすべてを実装している、という意味ではありません |

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

実装について引用するときは、論文のDOIに加えて、pangeo-fishのコミット（ワークショップでは`361e9b7`）、ノートブック名、データ製品と版、実行したPython環境を記録してください。プルリクエストを引用するときは、PR 番号に加えて、head のコミットも残してください。

この資料の BibTeX は `references_fra.bib` にあります。
