# JupyterLab の使い方のヒント

JupyterHub、JupyterLab、Python の環境にまだ慣れていない方のために、ワークショップ中（そして終了後）に役立つ実用的なヒントをまとめました。

下のスクリーンショットは、JupyterHub 上の標準的な JupyterLab 4 の画面で、小さな練習用ノートブックを開いたものです。お使いのサーバーでは、メニューや見た目が少し違うことがあります。
スクリーンショットのキーボードショートカットは macOS のものです（Windows では `Cmd` を `Ctrl` に読み替えてください）。

## ノートブックのセルを実行する

- **1つのセル**を実行する：セルをクリックして `Shift + Enter` を押します（ツールバーの ▶ ボタンでも実行できます）。
- **すべてのセル**を上から実行する：`Run > Run All Cells`。
- きれいな状態からやり直す：`Kernel > Restart Kernel and Run All Cells…`。
- 今いる場所の直前まですべて実行する：`Run > Run All Above Selected Cell`。

:::{figure} images/jupyterlab-run-menu.png
:alt: JupyterLab の Run メニュー。Run All Above Selected Cell と Run All Cells が表示されている。
:width: 800px

**Run** メニューから、すべてのセル、または選択中のセルより上のセルをまとめて実行できます。
:::

セルの実行中は、左側に `[*]` が表示され、右上のカーネルの状態表示が塗りつぶしの丸 ● になります。実行が終わると、`[*]` が `[12]` のような番号に変わります。

実行に時間がかかりすぎるセルを止めるには、ツールバーの ■ ボタンを押すか、`Kernel > Interrupt Kernel` を選びます。

:::{figure} images/jupyterlab-kernel-menu.png
:alt: JupyterLab の Kernel メニュー。Interrupt Kernel、Restart Kernel and Run All Cells、Shut Down All Kernels が表示されている。
:width: 800px

**Kernel** メニューには、中断・再起動・終了のコマンドがあります。
:::

## 作業内容を保存する

`File > Save Notebook`（`Ctrl + S`、Mac では `Cmd + S`）。Pangeo@EOSC のホームディレクトリは永続的です。保存したファイルは、次にログインしたときにも残っています。

## カーネルを終了してタブを閉じる

ノートブックのタブを閉じても、そのカーネルは**停止しません**。カーネルは動き続け、メモリも使い続けます。ノートブックを使い終えたら、次のいずれかで終了してください。

- `Kernel > Shut Down Kernel`：今開いているノートブックのカーネルだけを終了します。
- `Kernel > Shut Down All Kernels…`：すべてのカーネルを終了します。
- 左のサイドバーにある **Running Terminals and Kernels** パネル（丸の中に四角のアイコン）：「Kernels」と「Terminals」の横にある `Shut Down All` をそれぞれ押します。

:::{figure} images/jupyterlab-running-panel.png
:alt: Running Terminals and Kernels サイドバー。Kernels と Terminals にそれぞれ別の Shut Down All ボタンがある。
:width: 440px

左側の丸に四角のアイコンで、実行中のセッションのパネルを開きます。
**Kernels** と **Terminals** には、それぞれ専用の **Shut Down All** ボタンがあります。
:::

そのあと、`File > Close All Tabs` ですべてのタブを閉じます。

:::{figure} images/jupyterlab-close-all-tabs.png
:alt: JupyterLab の File メニュー。Close All Tabs が強調表示されている。
:width: 600px

カーネルとターミナルを終了したら、**File > Close All Tabs** を選びます。
:::

## 終わったらサーバーを停止する

JupyterLab のサーバーは、ブラウザを閉じても、停止するまで共有インフラの CPU・メモリ・電力を使い続けます。作業の最後に、必ず停止してください。

1. `File > Hub Control Panel`
2. **Stop My Server** をクリック
3. （任意）`File > Log Out`

:::{figure} images/jupyterlab-hub-control-panel.png
:alt: JupyterLab の File メニュー。下のほうに Hub Control Panel がある。
:width: 600px

まず **File > Hub Control Panel** を開きます。
:::

:::{figure} images/jupyterhub-stop-server.png
:alt: JupyterHub のホーム画面。My Server の横に赤い Stop My Server ボタンがある。
:width: 800px

次に、JupyterHub の画面で **Stop My Server** をクリックします。
:::

サーバーを停止しても、ファイルは削除されません。次回は **Start My Server**（またはワンクリック起動リンク）をクリックすれば、再び起動できます。

## フォルダを削除する

ファイルブラウザ（左のサイドバー）で、ファイルまたはフォルダを右クリックし、`Delete` を選びます。

:::{figure} images/jupyterlab-delete-folder.png
:alt: example-folder で開いたファイルブラウザの右クリックメニュー。Delete コマンドがある。
:width: 800px

フォルダを右クリックして **Delete** を選びます。
:::

サーバーのごみ箱や削除の設定によっては、ファイルが残っているフォルダの削除が、**Directory ... not empty** というエラーで拒否されることがあります。フォルダごとごみ箱に移すサーバーもあります。

:::{figure} images/jupyterlab-delete-nonempty-error.png
:alt: example-folder が空でないことを知らせる Delete Failed ダイアログ。
:width: 700px

このサーバーは、空でないフォルダの削除を拒否します。実際のエラーに表示されるパスは、これとは異なります。
:::

このエラーが出たときの対処は 2 つあります。入れ子になったサブフォルダ（Zarr ストアなど）や隠しファイル（名前が `.` で始まるもの）があるフォルダは、ファイルブラウザで 1 つずつ空にするより、ターミナルを使うほうがたいてい早く済みます。

- **ファイルブラウザ**：フォルダを開き、すべてのファイルを選択して（最初と最後のファイルを `Shift + クリック`）、右クリック > `Delete`。1 つ上の階層に戻って、空になったフォルダを削除します。サブフォルダがある場合は、先にそれらを空にして削除してください。隠しファイルは初期設定では表示されず、それでも削除を妨げることがあります。
- **ターミナル**（`File > New > Terminal`）：

  ```bash
  cd ~
  ls                      # フォルダ名を正確に確認する
  rm -rf name-of-the-folder
  ```

  :::{warning}
  `rm -rf` は、フォルダとその中身を、その場で完全に削除します。ごみ箱はありません。フォルダ名を二度確認してください。
  :::

ワークショップの環境をすべて片づけるには、ホームディレクトリの `pangeo-fish-fra2026` フォルダを削除してください。また必要になったときは、ワンクリック起動リンクで再び clone されます。

## ファイルのアップロードとダウンロード

- **アップロード**：パソコンのファイルをファイルブラウザにドラッグ＆ドロップするか、⬆ ボタンを使います。
- **ダウンロード**：ファイルブラウザでファイルを右クリックし、`Download` を選びます。
  （フォルダの場合は、先にターミナルで圧縮してください：`zip -r results.zip my-folder`）
