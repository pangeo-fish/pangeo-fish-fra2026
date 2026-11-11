
# 当日：Pangeo@EOSC の使い方

Pangeo@EOSC は、ヨーロッパの研究者とその共同研究者に開かれた、Pangeo エコシステムの主要な公開環境です。ヨーロッパのインフラ上で運用されており、Pangeo@Europe は研究者向けのトレーニングに主に Pangeo@EOSC を使っています。計算資源やストレージ（MinIO）については {doc}`pangeo` を見てください。

## ワークショップの環境を起動する（ワンクリック）

参加申請が承認されたら、まず [Pangeo@EOSC にログイン](https://pangeo-eosc.vm.fedcloud.eu/hub/login)します。**Sign in with EGI Check-in** をクリックし、登録に使ったのと同じ ORCID iD / EGI アカウントでログインしてください。ログインしたらこのページに戻り、下の起動リンクを使います。ログインしていない状態では、起動リンクが正しく動かないことがあります。

起動リンクは次のことを行います。

1. **pangeo-fish の Docker イメージ**（`ghcr.io/tinaok/pangeo-fish-notebook:2026.06.04-10751a5`）で JupyterLab サーバーを起動します。
2. **このリポジトリ**（`pangeo-fish-fra2026`）をホームディレクトリに**クローン**し（すでにある場合は更新し）、pangeo-fish のノートブックを開きます。

👉 **<a href="https://pangeo-eosc.vm.fedcloud.eu/hub/spawn?profile=only-choice&amp;profile-option-only-choice--image--unlisted-choice=ghcr.io%2Ftinaok%2Fpangeo-fish-notebook%3A2026.06.04-10751a5&amp;next=%2Fhub%2Fuser-redirect%2Fgit-pull%3Frepo%3Dhttps%253A%252F%252Fgithub.com%252Fpangeo-fish%252Fpangeo-fish-fra2026%26urlpath%3Dlab%252Ftree%252Fpangeo-fish-fra2026%252Fdocs%252Fpangeo-fish.ipynb%26branch%3Dmain">FRA 2026 pangeo-fish ワークショップの環境を起動する</a>** 👈

または、ログインしたあとで、次の URL をブラウザのアドレスバーにコピー＆ペーストしてください。

```
https://pangeo-eosc.vm.fedcloud.eu/hub/spawn?profile=only-choice&profile-option-only-choice--image--unlisted-choice=ghcr.io%2Ftinaok%2Fpangeo-fish-notebook%3A2026.06.04-10751a5&next=%2Fhub%2Fuser-redirect%2Fgit-pull%3Frepo%3Dhttps%253A%252F%252Fgithub.com%252Fpangeo-fish%252Fpangeo-fish-fra2026%26urlpath%3Dlab%252Ftree%252Fpangeo-fish-fra2026%252Fdocs%252Fpangeo-fish.ipynb%26branch%3Dmain
```

:::{note}
JupyterLab サーバーが**すでに動いている**場合（たとえば別のイメージで起動している場合）、上のリンクは pangeo-fish のイメージで新しいサーバーを起動せず、動いているサーバーを開きます。その場合は、先にサーバーを停止してください。JupyterLab で `File > Hub Control Panel` を開き、`Stop My Server` をクリックしてから、もう一度リンクをクリックします。
:::

このブックの各ノートブックのページ上部にある 🚀（ロケット）ボタンの `JupyterHub` からも同じこと（リポジトリのクローン・更新と、そのノートブックを開くこと）ができます。ただし、Docker イメージは自動では選ばれ**ません**。

## Pangeo@EOSC に手動でアクセスする

[https://pangeo-eosc.vm.fedcloud.eu/](https://pangeo-eosc.vm.fedcloud.eu/) から Pangeo@EOSC にアクセスすることもできます。`Sign in with EGI Check-in` をクリックし、ORCID iD でログインしてください。

サーバーのオプションの **Image** で **"Specify an existing docker image"**（カスタムイメージ）を選び、次を入力します。

```
ghcr.io/tinaok/pangeo-fish-notebook:2026.06.04-10751a5
```

固定タグ `2026.06.04-10751a5` には、このワークショップ用に準備した Pangeo-Fish のバージョンが入っています。全員が同じ環境で作業できるよう、この固定タグを使ってください。イメージは [tinaok/pangeo-fish-docker](https://github.com/tinaok/pangeo-fish-docker) でビルド・テストされています。

JupyterLab が起動したら、ターミナルを開いてこのリポジトリをクローンします。

```
git clone https://github.com/pangeo-fish/pangeo-fish-fra2026.git
```

または、前のセクションのワンクリック起動リンクを使ってください。

## どのカーネルを使うか

Docker イメージには 2 つの Python カーネルがあります。**このワークショップのノートブックでは、すべて「Python (pangeo-fish)」を使ってください**（このリポジトリからノートブックを開くと自動で選ばれます）。もう一方の「Python 3 (ipykernel)」は、pangeo-fish を含まない標準の Pangeo ノートブック環境です。

ターミナルでは、`conda activate pangeo-fish` で pangeo-fish の環境を有効にできます。

JupyterLab の実用的なヒント（すべてのセルの実行、カーネルの終了、サーバーの停止、フォルダの削除など）は {doc}`jupyterlab-basics` にまとめています。

## サポート

サポートが必要な場合は、[issue](https://github.com/pangeo-fish/pangeo-fish-fra2026/issues) を作成してください。

その際、Pangeo-Fish ノートブックの最後のセル（付録「**バグ報告用の情報（Information for bug reports）**」）の出力を添えてください。どの Docker イメージ、Pangeo-Fish のコミット、ノートブックのバージョンを使ったかが分かります。
