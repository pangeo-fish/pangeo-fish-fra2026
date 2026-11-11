# EOSC と Pangeo コミュニティ

## 欧州オープンサイエンスクラウド（EOSC）

このページでは、ワークショップで使う Pangeo@EOSC の背景として、欧州オープンサイエンスクラウド（European Open Science Cloud、EOSC）と Pangeo コミュニティを紹介します。Pangeo@EOSC の計算資源とストレージ（MinIO）についても説明します。

![EOSC のロゴ](./images/EOSC_logo-small.png)

[欧州オープンサイエンスクラウド（EOSC）](https://open-science-cloud.ec.europa.eu/)は、研究データの保管と処理を担う主要な環境となり、欧州の科学を支えることを目指しています。

## Pangeo Europe

![Pangeo のロゴ](./images/pangeo_name_logo.png)

[Pangeo](https://pangeo.io/) は、オープンで再現可能、かつスケーラブルな科学を推進する、地球科学ビッグデータの世界的なコミュニティです。

[Pangeo Europe](https://pangeo.io/meeting-notes.html) は、Pangeo コミュニティへの欧州からの貢献を広く紹介するとともに、EOSC 上の Pangeo の標準的な展開環境（reference deployment）を提供することを目指しています。EOSC 上の Pangeo の展開は、[EGI-ACE プロジェクト](https://youtu.be/Vc9SZNa2-Os)と [C-SCALE プロジェクト](https://youtu.be/-jBkR_2_vg8)の枠組みで、[CESNET](https://www.cesnet.cz/en/) の協力により実現しました。

## Pangeo@EOSC の概要

<style>
.responsive-wrap iframe{ max-width: 100%;}
</style>
<div class="responsive-wrap">
<!-- this is the embed code provided by Google -->
  <iframe src="https://docs.google.com/presentation/d/1F8BM1Xk7vaKlJUkNFXkABW6DouHCgTgwhUGuF2H5SSs/embed?start=false&loop=false&delayms=3000" frameborder="0" width="960" height="569" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>
<!-- Google embed ends -->
</div>

## Pangeo@EOSC の計算資源

現在（2023 年 9 月時点）、Pangeo@EOSC は、Jupyter（8 CPU、32 GB RAM）と Dask クラスター（最大 4 ワーカー、各ワーカー 8 CPU・32 GB RAM）を 20 人が同時に使える構成になっています。この構成は、利用状況や CESNET の資源の空き状況によって変わることがあります。

計算をスケールさせるために [Dask Gateway](https://gateway.dask.org/) が使えます。この環境の詳細は [Daskhub の Helm チャート](https://github.com/dask/helm-chart/tree/main/daskhub)を参照してください。

## MinIO（オブジェクトストレージ）へのアクセス

DaskHub は大きなデータを保存するためのものではないので、各ユーザーのローカルストレージはごくわずかです。その代わりに、専用の [MinIO オブジェクトストレージ](https://min.io)が用意されています。

MinIO コンソールのエンドポイントは [https://pangeo-eosc-minio.vm.fedcloud.eu/](https://pangeo-eosc-minio.vm.fedcloud.eu/) です。MinIO オブジェクトストレージには、DaskHub と同じ方法でログインできます。下の図のように、"Select Other Authentication Method" を選び、"Login with SSO (checkin)" から MinIO コンソールに入ってください。そのあと ORCID iD でログインします。

![MinIO のログイン画面](images/minIO_login.png)

MinIO コンソールでは、バケットの作成・アクセス・管理ができます（[MinIO の Python パッケージ](https://min.io/docs/minio/linux/developers/python/minio-py.html)を使うこともできます）。下の図はその画面です（左側にいくつかのタブがあり、図ではバケットのタブが選ばれています）。最初はバケットが 1 つもないので、公開・非公開のバケットを自由に作成してください。

![MinIO のバケット](images/minIO_buckets.png)

API で MinIO を操作したい場合は、MinIO コンソールのほかに API エンドポイント `https://pangeo-eosc-minioapi.vm.fedcloud.eu/` が使えます。

## Pangeo@EOSC の謝辞の書き方

[Pangeo@EOSC](https://github.com/pangeo-data/pangeo-eosc/) は、[EGI-ACE プロジェクト](https://www.egi.eu/project/egi-ace/)（欧州連合の Horizon 2020 研究・イノベーションプログラムの助成、助成契約番号 101017567）と [C-SCALE プロジェクト](https://c-scale.eu/)（同プログラムの助成、助成契約番号 101017529）が提供するサービスと資源の恩恵を受けており、[CESNET](https://www.cesnet.cz/en/) が専任で支援しています。

英語の謝辞の原文（論文などにそのまま使う場合）：

> Pangeo@EOSC has benefited from services and resources provided by the EGI-ACE project (funded by the European Union's Horizon 2020 research and innovation programme under Grant Agreement no. 101017567), and the C-SCALE project (funded by the European Union's Horizon 2020 research and innovation programme under grant agreement no. 101017529), with the dedicated support of CESNET.
