---
# File metadata may be provided as frontmatter YAML
title: Pangeo-Fish による魚類の位置推定
subtitle: FRA 横浜ワークショップ 2026
description: バイオロギング（アーカイバルタグや音響テレメトリー）データを pangeo-fish と Pangeo のエコシステムで解析する、水産研究・教育機構（FRA）向けのハンズオンワークショップ。Pangeo@EOSC の JupyterHub 上で実行します。
date: 2026-11-25
authors:
  - id: tinaok
    name: Tina Erica Odaka
    orcid: 0000-0002-1500-0156
    corresponding: true
    roles:
      - Pangeo-Fish
    affiliations:
      - ifremer
affiliations:
  - id: ifremer
    name: フランス海洋開発研究所（IFREMER）
    city: ブレスト
    country: フランス
    url: https://www.ifremer.fr
    ror: https://ror.org/044jxhp58
tags:
  - pangeo
  - pangeo-fish
  - biologging
  - fish-tracking
  - HEALPix
thumbnail: images/pangeo-fish-logo.png
---

# Pangeo-Fish による魚類の位置推定

+++ {"part":"abstract"}

バイオロギングタグ（アーカイバルタグ、ポップアップ式衛星タグ）や音響テレメトリーからは、水温・水圧・受信イベントの長い時系列が得られますが、位置そのものは直接わかりません。[pangeo-fish](https://github.com/pangeo-fish/pangeo-fish) は、Pangeo のエコシステム（Xarray、Dask、HEALPix）の上に作られたオープンソースの Python パッケージで、タグの記録を海洋の参照モデルと突き合わせることで、標識した魚の最も確からしい移動経路を復元します。このハンズオンワークショップでは、Pangeo のエコシステムを紹介したうえで、タグの読み込みから推定した経路の可視化まで、pangeo-fish による位置推定の一連の流れを Pangeo@EOSC クラウド上で体験します。インストールは不要で、すべてウェブブラウザの中で動きます。

+++

# 日時・場所・時間割・事前登録

ワークショップは **2026年11月25日（水）10:00〜12:00** に、水産研究・教育機構（FRA）**横浜庁舎**で、対面とリモートのハイブリッドで開催します。**リモート参加を希望する方は、FRA 研究戦略部 研究調整課にご連絡ください。**

## 時間割

```{include} agenda.md
:start-after: <!-- timetable-start -->
:end-before: <!-- timetable-end -->
```

詳しくは {doc}`agenda` のページを見てください。

## 事前登録

Pangeo@EOSC の[事前登録](users-getting-started)（3 ステップ）を、**できれば 11 月 22 日までに**済ませてください。参加申請の承認は手作業で行われるため、時間がかかることがあります。

# 概要

このワークショップでは、1) 海洋データを大規模に解析するための Pangeo のエコシステム（Xarray、Dask、HEALPix）の使い方と、2) [pangeo-fish](https://pangeo-fish.readthedocs.io/) を使い、バイオロギングデータ（水温・水圧）と音響テレメトリーの受信記録から標識魚の位置を推定する方法を学びます。参照モデルには、Copernicus Marine Service の海洋再解析（reanalysis）を使います。

教材はすべて共同で開発し、CC-BY-4 ライセンスでオンライン公開しています。参加しやすいよう、pangeo-fish を組み込んだ Docker イメージをあらかじめ用意した [Pangeo@EOSC](https://pangeo-data.github.io/pangeo-eosc/) プラットフォームを提供します。ほかのプラットフォームで教材を動かすために必要な情報も、すべて掲載しています。

## 学習目標

このワークショップを終えると、次のことができるようになります。
- Pangeo のエコシステムと、それが海洋データやバイオロギングデータの大規模解析で果たす役割を理解する。
- 海洋モデル（Copernicus Marine Service の GLORYS）を Xarray で開いて中身を確認・可視化し、Dask で計算を並列化して、結果を Zarr 形式で保存する。
- HEALPix（等面積の離散全球格子システム、DGGS: Discrete Global Grid System）とは何か、pangeo-fish がなぜそれを使うのかを理解し、xdggs でデータを HEALPix に変換して描画する。
- バイオロギングタグに対して pangeo-fish の位置推定の流れを実行する。タグの記録を参照モデルと比較して観測確率（emission probability）を作り、音響テレメトリーの受信記録を加え、パラメータを最適化して、推定した移動経路を可視化する。

## 前提知識

ワークショップの前に、次のものを用意してください。

- R など、何らかのプログラミング言語の基礎知識（Python の経験は不要です。ノートブックは R ユーザー向けに書かれています）。
- バイオロギング・魚類追跡データ（アーカイバルタグ、音響テレメトリー）の基礎知識。
- [Copernicus Marine Service](https://data.marine.copernicus.eu/register) のアカウント（無料）。pangeo-fish のノートブックが参照用の海洋モデルをダウンロードするときに使います。

## 環境の準備

FRA 横浜ワークショップに参加する方は、[Pangeo@EOSC](https://pangeo-data.github.io/pangeo-eosc/) 上でノートブックを実行します。**ワークショップの前に**、[事前登録](users-getting-started)の 3 つのステップを済ませてください（できれば 11 月 22 日まで）。ワークショップ後も Pangeo@EOSC を使い続けたい場合は、同じアカウントをそのまま使えます。
