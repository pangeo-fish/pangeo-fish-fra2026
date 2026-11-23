# 科学・技術解説の図を作るスクリプト

`docs/science/figures/` の図を作った Python スクリプトです。図はどれも説明のための合成例、または定義式から計算した値の図で、実際の魚の観測データや pangeo-fish の実行結果ではありません。

| スクリプト | 描く図 |
|---|---|
| `make_hmm_figures.py` | 平均・最頻・Viterbi を比べる小さな HMM の例、水温残差の集約の比較（全体像の図も作るが、本に載せていない） |
| `make_observation_figure.py` | 潮汐・海底地形・音響で「位置に合う」の意味が違うことを示す三つの合成例 |
| `make_healpix_figure.py` | WGS84 の緯度の数値差と、HEALPix の level ごとのセルの代表長 |

- 必要なもの：Python 3、NumPy、Matplotlib（SciPy があれば追加の数値も計算）。日本語フォント（Noto Sans CJK JP など）も必要です。
- 本に載せた図は作成済みなので、読むだけなら実行は不要です。ビルド時にも実行しません。
- スクリプトの出力先は、元の資料の配置（スクリプトの一つ上のフォルダーに `docs/science/figures` と `evidence`）を前提にしています。この場所で実行する場合は、出力先のパス（`OUT`、`EVIDENCE`、`--output`）を確認してください。
