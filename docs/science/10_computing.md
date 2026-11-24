# Xarray・Dask・Zarrと計算の大きさ

この章の実装記述は、pangeo-fish `main` の `af4fe17` のソースを読んで確認した内容です（潮汐の書き出しと Complete デモのリンクは `361e9b7` で確認。ノートブックを実行して確かめたものではありません）。

計算設計を説明するときは、科学的な状態の数、データを保存する単位、並列処理する単位を分けます。HEALPixを細かくすると位置状態が増えます。ZarrとDaskは、そのデータをどう読み、どの単位で計算するかを扱います。

## 1. 三つの役割

| 要素 | 役割 | Pangeo-Fishで確認したい点 |
|---|---|---|
| Xarray | 名前付きの次元・座標・変数を扱う | `time`、`cells`、深度、単位、座標ラベルが一致しているか |
| Zarr | 配列をチャンクに分けて保存する | 保存チャンク、版、欠測値、格子属性、圧縮 |
| Dask | チャンク単位で計算を構成する | 同時に必要な配列量、タスク数、再チャンクの転送 |

Xarrayの`open_zarr`では、`chunks={}`が保存側のチャンクを使う指定、`chunks="auto"`がバックエンドの推奨を考慮した自動指定、`chunks=None`がDaskを使わない指定となります。動作は使用版で確認します。[Xarray API](https://docs.xarray.dev/en/stable/generated/xarray.open_zarr.html)

### DataTreeで階層を表す

XarrayのDataTreeは、複数のDatasetを階層として管理します。複数レベルのデータを整理できるが、階層を作ったこと自体はレベル間の集約の正しさを保証しません。[Xarrayのデータ構造](https://docs.xarray.dev/en/stable/user-guide/data-structures.html#datatree)

## 2. 必要なメモリを先に見積もる

時刻数$T$、候補セル数$N$、浮動小数点の1要素あたりのバイト数$b$とすると、ひとつの密な観測配列は

$$M_{\rm array}=T\,N\,b$$

バイトを占めます。これは全要素を同時に展開した場合の配列本体のサイズです。チャンクごとに処理すれば同時に常駐する量はこれより小さくできます。実際のピークメモリは、同時実行するタスクと中間配列にも依存します。

例えば$T=365$、$N=100,000$、float64なら$292,000,000$バイト、約278.5 MiBになります。同じ大きさの温度・音響・水深・潮汐・結合重み・フィルタ分布を同時に保持すれば、必要量はその倍数になります。中間配列、近傍リスト、座標、FFT、タスクの一時データも加わります。100,000セルは説明用に選んだ数であり、A19124の実測値ではありません。

同じ地理的領域を同様のマスクで覆う場合、HEALPixのレベルを一つ上げるとセル数はおおむね4倍になります。時間・深度方向の大きさが同じなら、対応する配列の要素数もおおむね4倍になります。全球セル数の厳密な式と代表長は[楕円体HEALPix](09_ellipsoidal_healpix.md)を参照します。

## 3. 保存チャンクと計算チャンク

Zarrの適切なチャンク形状は、どの向きにスライスするか、圧縮とI/Oの条件で変わります。Daskでは小さすぎるタスクの管理負荷と、同時にメモリに乗るデータ量を釣り合わせます。保存チャンクと計算チャンクを対応させると、同じデータの重複読込を減らせます。[Zarr公式ガイド](https://zarr.readthedocs.io/en/stable/user-guide/performance/)／[Dask公式ガイド](https://docs.dask.org/en/stable/array-best-practices.html)

`main` の Complete デモは、保存チャンクと計算チャンクを次のように扱います。

- 時間ステップの Dask チャンクは設定 `chunk_time` で決まり、配布デモでは `chunk_time = 1`（1つの時間ステップごと）です。空間は `cells` を分割しません（`default_chunk_dims = {"time": chunk_time, "cells": -1}`）。
- 再格子化した水温差（`diff-regridded.zarr`）、水温の観測確率（emission probability、`emission_diff.zarr`）、統合後の PDF（`combined.zarr`）は、このチャンクに揃えて `to_zarr(..., zarr_format=2, consolidated=True)` で書き出されます。つまりこれらの保存チャンクは「1つの時間ステップ × 全セル」の形で、デモでは保存チャンクと計算チャンクが一致します。音響・海底地形・総合 PDF（`total_pdf.zarr`）の書き出しでは、デモは明示的な再チャンクを行いません。
- 読み込みは `xr.open_dataset(..., engine="zarr", chunks={})`（保存チャンクのまま Dask 配列にする）で行い、HMM の最適化の前に `.chunk(default_chunk_dims)` で計算チャンクを明示します。
- パッケージは Zarr-Python 3 を使うが、書き出しは Zarr format 2 を明示しています（`pyproject.toml` のコメントと `storage.py` の docstring）。
- 潮汐の日ごとの PDF（`write_tide_pdf_healpix`）は `storage.write_time_blocks` で書かれます。時間方向の保存チャンクは `gcd(10, step)`（`step` の既定は200なので10）で、`cells` は分割せず、領域書き込みを保存チャンクの境界に揃えます（`safe_chunks` を有効にしたまま）。時間に依存しない変数は最後に書きます。総合 PDF との結合（`merge_tide_with_total`）の後は `{"time": 3, "cells": -1}` に再チャンクし、元ストアのチャンク情報を捨てます。
- `pdf.normal`（水温の観測確率の計算）は要素ごとの計算なので、`cells` が複数のチャンクに分かれていても再チャンクなしで動きます（docstring）。

`pangeo_fish` が保存チャンクのサイズを自動的に決める仕組みは、このコミットにはありません。上の形（1ステップ × 全セル）は、セル数が増えたときの1チャンクのサイズ（時刻数に依存せず $N\times b$ バイト程度）に直結するので、レベルを上げる実験では1チャンクのメモリを先に見積もります。実装参照：[storage.py](https://github.com/pangeo-fish/pangeo-fish/blob/af4fe17/pangeo_fish/storage.py)、[Complete デモ](https://github.com/pangeo-fish/pangeo-fish/blob/361e9b7/notebooks/pangeo-fish-complete-demo.ipynb)（Section 1、3）。

再チャンクはまず遅延計算のグラフを作る場合があり、実行時には全配列の読込・転送・再配置を伴うことがあります。空間・期間の切り出しと、再利用する中間生成物の保存を、処理手順の中で決めます。

## 4. NESTEDとデータ配置

NESTEDの階層構造は親子セルの対応を表せます。そこから、研究海域の全隣接セルがいつも連続する、任意の一次元チャンクが必ず地理的にまとまる、という保証は導けません。疎な海域の切り出しではcell IDに飛びがあります。

データの配列位置ではなく、cell IDとtimeラベルで観測項を合わせるのが望ましいです。楕円体、レベル、順序規約、フットプリントも確認します。`main` のデモは、音響と海底地形を `merge(..., compat="override")` で位置により結合します（海底地形は、その前に総合 PDF のセルIDと時刻で選んでそろえます）。潮汐はセルIDと日付で選んで結合します（詳細は[再格子化と格子・時刻の整合](09b_regridding_alignment.md)）。配列長が同じであるだけでは同じ場所の証拠を掛けたことになりません。

## 5. 移動作用素を選ぶ

| `conv_method` | 対応するクラス（`helpers._get_predictor_factory`） | 比較で確認する事項 |
|---|---|---|
| `HealpixConv` | `Gaussian1DHealpix` | 近傍の打ち切り（`truncate` が必須）、重みの閾値、候補数 |
| `LargeHealpixConv` | `UpDownGaussian1DHealpix` | 大きいカーネルへの処理、解像度間の操作 |
| `FFTConv`（既定） | `FFTGaussian1DHealpix` | 投影（`projection`：`"conservative"`（既定）／`"average"`）、補間、パッチサイズ、対称性の近似 |
| `HealpixAnalyseConv` | `GaussianHealpixAnalyse`（`healpix-analyse`。docstring は WGS84 のみと記す） | `normalization`（`"full_disc"` 既定／`"source"`）、`land_barrier`の選択 |
| `HealpixAnalyseLargeConv` | `LargeGaussianHealpixAnalyse`（同じく WGS84 のみ） | 作用素の定義と数値的な近似 |

これらを「速さだけが違う完全に同一の計算」と説明しません。境界での確率の失われ方、投影、打ち切り、正規化、海陸障壁の扱いが変わり得ます。配布デモは `FFTConv` を使います。`docs/choosing-conv-method.md` によれば、`FFTConv` は領域が半径10度の範囲に収まる必要があり、それを超えると停止します。また同文書は、`LargeHealpixConv` と `HealpixAnalyseLargeConv` では σ に対するコストが階段状・凸凹になり、最適化が誤った値で止まりうると述べています。どの作用素が適切かは対象海域・σ・格子・検証目的と一緒に考えます。[作用素の実装](https://github.com/pangeo-fish/pangeo-fish/blob/af4fe17/pangeo_fish/hmm/prediction.py)／[選択ガイド](https://github.com/pangeo-fish/pangeo-fish/blob/af4fe17/docs/choosing-conv-method.md)

## 6. 時間間隔とσ

σは「1ステップ」の移動スケールです。1日から1時間へ時間間隔を変更して、同じ数値をそのまま残すと、時間あたりの移動モデルが変わります。

例として、平面の等方拡散を仮定すると、各座標方向の分散は$2D\Delta t$で増え、σは$\sqrt{\Delta t}$に比例します。一方、`optimize_pdf`が`maximum_speed`から作る探索上限（`maximum_speed × Δt × adjustment_factor / 地球半径`、単位はラジアン）は$\Delta t$に比例します。探索の下限は$10^{-4}$ラジアンで、$\Delta t$は`time`座標から推定した時間間隔です。地球半径は格子の楕円体から決まり、球なら半径、楕円体なら長半径です（`helpers.py`）。この二つは異なる考え方であり、時間刻みを変える操作では、どの物理仮定でスケールを変えるかを明記します。ここでの拡散式は説明用の導出であり、デモに拡散係数$D$の推定機能があるという意味ではありません。

## 7. 実行記録に残す情報

Notebookごとに、FRA・Pangeo-Fishのコミット、実行環境のイメージ名と可能ならdigest、パッケージ版、データ製品と取得版、時間範囲、海域、格子、海マスク、誤差尺度、移動作用素、最適化の条件を記録します。計算時間とメモリは実行条件とセットで示します。
