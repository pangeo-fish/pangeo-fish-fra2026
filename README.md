# Pangeo-Fish による魚類の位置推定 - FRA 横浜ワークショップ 2026

*Fish geolocation with Pangeo-Fish — hands-on workshop (in Japanese) at the Japan Fisheries Research and Education Agency (FRA), Yokohama, 25 November 2026.*

このリポジトリの内容（`docs` フォルダ）は、[Jupyter Book](https://jupyterbook.org/en/stable/intro.html) でウェブ上の教材として公開しています。**教材は[こちら](https://pangeo-fish.github.io/pangeo-fish-fra2026)から読めます。**

## ワークショップ：Pangeo-Fish による魚類の位置推定

このハンズオンワークショップは、**2026年11月25日（水）10:00〜12:00** に、水産研究・教育機構（FRA）横浜庁舎で、対面とリモートのハイブリッドで開催します。リモート参加を希望する方は、FRA 研究戦略部 研究調整課にご連絡ください。

[Pangeo](https://pangeo.io) のエコシステム（Xarray、Dask、HEALPix）を紹介したうえで、バイオロギングデータを使い、[pangeo-fish](https://github.com/pangeo-fish/pangeo-fish) による位置推定の一連の流れを体験します。

ノートブックは [Pangeo@EOSC](https://pangeo-data.github.io/pangeo-eosc/) 上で、Docker イメージ [`ghcr.io/tinaok/pangeo-fish-notebook:2026.06.04-10751a5`](https://github.com/tinaok/pangeo-fish-docker) を使って実行します。

## 事前登録（できれば 11 月 22 日まで）

ワークショップの前に、[事前登録](https://pangeo-fish.github.io/pangeo-fish-fra2026/users-getting-started.html)の 3 つのステップを済ませてください。

1. EGI Check-in のアカウントを作る（ORCID でサインイン）
2. `vo.pangeo.eu` に参加申請する（承認は手作業なので早めに）
3. Copernicus Marine の無料アカウントを作る

## 環境を起動する（ワンクリック）

参加申請が承認されたら、まず [Pangeo@EOSC にログイン](https://pangeo-eosc.vm.fedcloud.eu/hub/login)します。ログインしたらこのページに戻り、下の起動リンクを使います。ログインしていない状態では、起動リンクが正しく動かないことがあります。

👉 **Pangeo@EOSC でワンクリック起動**（pangeo-fish のイメージでサーバーを起動し、このリポジトリをクローン・更新して、ノートブックを開きます）：
[ワークショップの環境を起動する](https://pangeo-eosc.vm.fedcloud.eu/hub/spawn?profile=only-choice&profile-option-only-choice--image--unlisted-choice=ghcr.io%2Ftinaok%2Fpangeo-fish-notebook%3A2026.06.04-10751a5&next=%2Fhub%2Fuser-redirect%2Fgit-pull%3Frepo%3Dhttps%253A%252F%252Fgithub.com%252Fpangeo-fish%252Fpangeo-fish-fra2026%26urlpath%3Dlab%252Ftree%252Fpangeo-fish-fra2026%252Fdocs%252Fpangeo-fish.ipynb%26branch%3Dmain)

または、ログインしたあとで、次の URL をブラウザのアドレスバーにコピー＆ペーストしてください。

```
https://pangeo-eosc.vm.fedcloud.eu/hub/spawn?profile=only-choice&profile-option-only-choice--image--unlisted-choice=ghcr.io%2Ftinaok%2Fpangeo-fish-notebook%3A2026.06.04-10751a5&next=%2Fhub%2Fuser-redirect%2Fgit-pull%3Frepo%3Dhttps%253A%252F%252Fgithub.com%252Fpangeo-fish%252Fpangeo-fish-fra2026%26urlpath%3Dlab%252Ftree%252Fpangeo-fish-fra2026%252Fdocs%252Fpangeo-fish.ipynb%26branch%3Dmain
```

## 教材を手元でビルドする

```bash
micromamba create -n fra2026 -f .binder/environment.yml
micromamba activate fra2026
jupyter-book build docs
```

HTML は `docs/_build/html` に作られます。`docs/` を変更して `main` に push すると、[`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) が GitHub Pages に自動で公開します。

## pangeo-fish の引用

研究で pangeo-fish を使った場合は、次の論文を引用してください。

Magin, J., Mazouni, Q., Cap, E., Gonse, M., Woillez, M., Fouilloux, A., Delouis, J.-M., and Odaka, T.: pangeo-fish: A Python package for studying fish movement using biologging and earth science data, *Journal of Open Source Software*, 11(122), 8332, https://doi.org/10.21105/joss.08332, 2026.

一緒に引用するデータやツール、pangeo-fish を使った研究の一覧は「[研究で pangeo-fish を使ったら：引用のしかた](https://pangeo-fish.github.io/pangeo-fish-fra2026/cite.html)」にまとめています。

## 謝辞

この教材は、ETN Symposium 2026（コペンハーゲン）のワークショップ教材 [pangeo-fish/pangeo-fish-etn2026](https://github.com/pangeo-fish/pangeo-fish-etn2026) をもとに、FRA 横浜ワークショップ向けに日本語化・改訂したものです。その元になったのは [pangeo-data/pangeo-bids25](https://github.com/pangeo-data/pangeo-bids25)（BiDS 2025 の Pangeo チュートリアル）です。GLORYS のノートブック（Xarray、Dask、Zarr、HEALPix）は、その *Introduction to HEALPix and Dask* ノートブックを改変したものです。pangeo-fish のノートブックは [pangeo-fish/pangeo-fish](https://github.com/pangeo-fish/pangeo-fish/blob/main/notebooks/pangeo-fish.ipynb) から取っています。
