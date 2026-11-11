# 研究で pangeo-fish を使ったら：引用のしかた

pangeo-fish はオープンソースのソフトウェアで、開発を続けるには、使われていることが論文の引用で見えることがとても大切です。研究で pangeo-fish を使った場合は、論文や報告書で次のように引用してください。

## pangeo-fish 本体

pangeo-fish を使った場合は、次の論文を引用してください。

- Magin, J., Mazouni, Q., Cap, E., Gonse, M., Woillez, M., Fouilloux, A., Delouis, J.-M., and Odaka, T.: pangeo-fish: A Python package for studying fish movement using biologging and earth science data, *Journal of Open Source Software*, 11(122), 8332, [https://doi.org/10.21105/joss.08332](https://doi.org/10.21105/joss.08332), 2026.

論文のページ：[https://joss.theoj.org/papers/10.21105/joss.08332](https://joss.theoj.org/papers/10.21105/joss.08332)（BibTeX などの形式もここから取得できます）

使ったバージョンを明記したい場合は、ソフトウェアの DOI（Zenodo）[https://doi.org/10.5281/zenodo.15110142](https://doi.org/10.5281/zenodo.15110142) もあわせて書いてください。使っているバージョンは、pangeo-fish ノートブックの付録「バグ報告用の情報（Information for bug reports）」で確認できます。

:::{note}
論文の本文では、たとえば次のように書けます。

> 標識魚の位置推定には pangeo-fish（Magin et al., 2026）を用いた。

> Fish positions were reconstructed with pangeo-fish (Magin et al., 2026).
:::

## 一緒に使ったデータやツール

解析で使ったものに合わせて、次も引用してください。

- **HEALPix の格子（楕円体上の HEALPix DGGS）と GRID4EARTH のパッケージ**：Odaka, T., Delouis, J.-M., Magin, J., Gueguen, C., Cap, E., Fouilloux, A., Bovy, B., Richard, P., Chan, W. T., Chrapkiewicz, K. M., and Kmoch, A.: Grid4Earth: An Open-Source Python Ecosystem for Geospatial Data Integration Using an Ellipsoidal HEALPix DGGS, *Int. Arch. Photogramm. Remote Sens. Spatial Inf. Sci.*, L-4/W1-2026, 189–195, [https://doi.org/10.5194/isprs-archives-L-4-W1-2026-189-2026](https://doi.org/10.5194/isprs-archives-L-4-W1-2026-189-2026), 2026.
- **海洋モデル（Copernicus Marine Service）**：使った製品の DOI を書いてください。
  - 全球の再解析 GLORYS：Global Ocean Physics Reanalysis, E.U. Copernicus Marine Service Information, [https://doi.org/10.48670/moi-00021](https://doi.org/10.48670/moi-00021)
  - IBI 海域の再解析：Atlantic-Iberian Biscay Irish- Ocean Physics Reanalysis, E.U. Copernicus Marine Service Information, [https://doi.org/10.48670/moi-00029](https://doi.org/10.48670/moi-00029)
- **このワークショップのタグデータ（A19124）**：Gonse et al. (2024)（下の一覧を見てください）。
- **Pangeo@EOSC で計算した場合**：謝辞に {doc}`pangeo` の「Pangeo@EOSC の謝辞の書き方」の文を入れてください。

## pangeo-fish を使った研究

pangeo-fish を使った論文の一覧です。

- Magin, J., Mazouni, Q., Cap, E., Gonse, M., Woillez, M., Fouilloux, A., Delouis, J.-M., and Odaka, T.: pangeo-fish: A Python package for studying fish movement using biologging and earth science data, *Journal of Open Source Software*, 11(122), 8332, [https://doi.org/10.21105/joss.08332](https://doi.org/10.21105/joss.08332), 2026.
- Gonse, M., Laurans, M., Magin, J., Odaka, T., Delouis, J.-M., Martin, S., Garren, F., Lazard, C., Drogou, M., Stamp, T., Davies, P., Hall, A., Sheehan, E., and Woillez, M.: Combining acoustic telemetry with archival tagging to investigate the spatial dynamic of the understudied pollack, *Pollachius pollachius*, *Journal of Fish Biology*, 106(5), 1400–1421, [https://doi.org/10.1111/jfb.15750](https://doi.org/10.1111/jfb.15750), 2024.

pangeo-fish を使った論文を発表したら、[issue](https://github.com/pangeo-fish/pangeo-fish-fra2026/issues) でお知らせください。この一覧に追加します。
