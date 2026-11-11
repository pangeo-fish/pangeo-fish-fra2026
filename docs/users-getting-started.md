
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

承認のメールが届いたら、時間があれば {doc}`pangeo-eosc` の「ワークショップの環境を起動する」の手順で一度ログインし、環境を起動してみてください。当日の待ち時間を減らせます。うまくいかない場合は、[issue](https://github.com/pangeo-fish/pangeo-fish-fra2026/issues) でお知らせください。

:::{note}
**FRA 横浜ワークショップ**の終了後も、同じアカウントで引き続きこの環境を使うことができます。

オンラインのミートアップ「Pangeo show and tell」で発表していただくこともできます。
:::
