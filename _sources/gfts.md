# 将来の海での魚の姿：GFTS

[pangeo-fish のノートブック](pangeo-fish)で計算した地図は、魚が過去にどこにいたらしいかを示しています。**Global Fish Tracking Service（GFTS、全球魚類追跡サービス）** は、[Destination Earth](https://destination-earth.eu) のユースケースの 1 つで、その次の一歩を担います。同じ Pangeo-Fish の手法と同じ HEALPix 格子を使い、復元した移動経路を、Destination Earth の気候変動適応デジタルツインが予測する 2025〜2039 年の海水温と並べて表示します。そこから「自分の魚が使った場所は、魚が経験した水温の範囲にとどまるだろうか？」という問いを立てることができます。

**皆さんが計算した結果は、そのまま GFTS で使えます。** ノートブックの結果は、出力フォルダ（セクション10に表示されます）に保存されています。`states.zarr`（各時刻における存在確率）と `trajectories.parq`（平均の経路と最頻値の経路）です。この 2 つのファイルがあれば、皆さんの魚を GFTS に加えて、将来の水温と比べることができます。

**ワークショップのあとで試してみましょう：**

1. [Destination Earth Platform](https://platform.destine.eu) に登録します（無料アカウント）。
2. [GFTS ダッシュボード](https://gfts.destine.eu)を開き、Destination Earth のアカウントでサインインします。すでに登録されているスズキとポラックの移動経路や、その生息域で予測される水温を見てみましょう。
3. 詳しくは [GFTS のドキュメント](https://destination-earth.github.io/DestinE_ESA_GFTS)（英語）を読んでください。

### 共同研究の相手を探しています

アーカイバルタグ（DST、データストレージタグ）や音響タグを持っていて、自分の魚を GFTS で見てみたい方はいませんか。私たちは、皆さんと一緒に、より多くの魚種と海域を解析したいと考えています。[GFTS の repository](https://github.com/destination-earth/DestinE_ESA_GFTS/issues/new) に issue を作成し、次の点を簡単に書いてください。

- FRA 横浜ワークショップで GFTS を知ったこと。
- タグが対象とする魚種と海域、タグの数、タグの種類（アーカイバル、音響、またはその両方）。
- Pangeo-Fish で自分の魚を解析し、GFTS を使ってみたいこと。

登録後に GFTS ダッシュボードを開けない場合は、同じ issue にそのことを書いてください。アクセスできるようお手伝いします。
