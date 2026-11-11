
# 事前登録（できれば 11 月 22 日まで）

ワークショップでは、クラウド上の [Pangeo@EOSC](https://pangeo-data.github.io/pangeo-eosc/) でノートブックを動かします。当日すぐに始められるよう、**次の 3 つのステップを、できれば 11 月 22 日までに**済ませてください。どれも無料です。

::::{grid} 1 1 3 3
:gutter: 3

:::{grid-item-card} 1. EGI Check-in のアカウント
:link: step1-egi
:link-type: ref

ORCID でサインインするのが簡単です（ORCID がなければ先に作ります）。
:::

:::{grid-item-card} 2. `vo.pangeo.eu` への参加申請
:link: step2-vo
:link-type: ref

理由欄に指定の一文を貼るだけ。承認は手作業なので早めに。
:::

:::{grid-item-card} 3. Copernicus Marine の無料アカウント
:link: step3-cmems
:link-type: ref

GLORYS を読むために必要です。登録後、一度ログインできることを確認します。
:::
::::

(step1-egi)=
## ステップ 1：EGI Check-in のアカウントを作る

Pangeo@EOSC へのログインには [EGI Check-in](https://www.egi.eu/service/check-in/) のアカウントを使います。

1. [ORCID iD](https://orcid.org/) を持っていない場合は、先に [ORCID に登録](https://orcid.org/register)します（数分で終わります）。
2. [EGI Check-in のサインアップ手順](https://docs.egi.eu/users/aai/check-in/signup/)に従ってアカウントを作ります。ログイン方法の選択では **ORCID** を選ぶのがおすすめです。

(step2-vo)=
## ステップ 2：`vo.pangeo.eu` に参加申請する

Pangeo@EOSC を使うには、仮想組織（Virtual Organisation、VO）`vo.pangeo.eu` のメンバーになる必要があります。

1. ステップ 1 のアカウント（ORCID）でログインした状態で、[参加申請用の URL](https://aai.egi.eu/auth/realms/id/account/#/enroll?groupPath=/vo.pangeo.eu) を開きます。
2. **"reason to join"**（参加理由）の欄に、次の一文を**そのまま**貼り付けます。

   ```text
   Attend the pangeo-fish workshop at FRA in Yokohama, November 2026
   ```

   この文でワークショップの参加者だと分かり、すぐに承認できます。
3. 内容を確認して `Submit` をクリックします。

:::{warning}
参加申請の承認は、ワークショップの講師が**手作業**で行います。承認されるまで Pangeo@EOSC にはログインできないので、**早めに**申請してください。承認されると EGI からメールが届きます。
:::

(step3-cmems)=
## ステップ 3：Copernicus Marine の無料アカウントを作る

どちらのノートブックも、[Copernicus Marine Service](https://data.marine.copernicus.eu/) から海洋モデルのデータ（GLORYS、全球海洋物理再解析）をダウンロードします。そのため、Copernicus Marine の（無料の）アカウントが必要です。

1. [https://data.marine.copernicus.eu/register](https://data.marine.copernicus.eu/register) でアカウントを作成します（メールアドレスがあれば作れます。届いたメールのリンクをクリックして確認してください）。
2. **ユーザー名**（多くの場合メールアドレス）と**パスワード**を控えておきます。
3. [https://data.marine.copernicus.eu/](https://data.marine.copernicus.eu/) で一度ログインし、そのユーザー名とパスワードでログインできることを確認します。

当日は、最初のノートブックで一度だけユーザー名とパスワードの入力を求められます（`copernicusmarine.login()`）。入力した情報は Pangeo@EOSC のホームディレクトリの `~/.copernicusmarine/.copernicusmarine-credentials` に保存されます。ホームディレクトリは永続的なので、再び入力を求められることはありません。

## 事前登録はこれで完了です

承認のメールが届いたら、時間があれば下の「ワークショップの環境を起動する」の手順で一度ログインし、環境を起動してみてください。当日の待ち時間を減らせます。うまくいかない場合は、[issue](https://github.com/pangeo-fish/pangeo-fish-fra2026/issues) でお知らせください。

:::{note}
**FRA 横浜ワークショップ**の終了後も、同じアカウントで引き続きこの環境を使うことができます。
ぜひご感想をお寄せください。プラットフォームの今後の情報もお知らせします。連絡には [GitHub Discussions](https://github.com/pangeo-data/pangeo-eosc/discussions) をお使いください。

オンラインのミートアップ「Pangeo show and tell」で発表していただくこともできます。
:::

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
