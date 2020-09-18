# 新着チャンネル通知

slackに作られたchannelをポストする。

## Getting Started

このプロジェクトはslack_api、及びslack_appを利用します。
slack_botに対して権限を付与したBotの`Token`が必要になります。

`Token`を持っていればlocal環境で検証することが出来ます。

## Prerequisites

* Python 3.8 (AWS Lambdaのバージョンに合わせる)

### SlackApp

`Slack App` の作成を行う。

`Basic Information` > `Add features and functionality` > `Bots`からBotを追加。

`Basic Information` > `Add features and functionality` > `Permissions`からBotに権限を付与する。

> Bot Tokens Scopes
* channels:history
* channels:read
* chat:write

`Basic Information` > `Install your app to your workspace` でslack appをインストール。

`Installed App Setting` > `OAuth Tokens for Your Team` > `Bot User OAuth Access Token` をコピーしとく。

このTokenがあればLocalからSlackに通知することが可能。

## Installing

リポジトリを適当な所にcloneしてください。
```sh
git clone https://github.com/gamiyama3110/new_slackchannel_notice.git & cdnew_slackchanne l_notice 
```

Pythonの仮想環境を用意するために、`pip`が利用できるPythonをインストールする。
Python3.4以上（Python2の場合は2.7.9以上）で`pip`が利用できる。

> macは標準でインストールされているのでスキップ。

`pip`を利用して`pipenv`をインストールする。

```sh
pip install pipenv
```

Pipfileを元に`pipenv`で`python`の仮想環境をインストールする。
開発を前提にする場合はオプションがあります。
```sh
pipenv install
```

開発環境用のライブラリを含めてインストールする場合。
```sh
pipenv install --dev
```

---
> `Locking Failed !` が出た時

```sh
pipenv lock --clear
```
または
```sh
pipenv lock --pre
```

---
仮想環境に入ってpythonコマンドで実行する。
```sh
pipenv shell
python src/handler.py {token} {channle_id or ""} {slack_domain or ""}
exit
```

### AWSへの配置

`Lambda`に配置して`EventBridge（CloudWatch Event）`で定期実行をする。

#### Lambda

> 関数コード
```
lambda_name
└handler.py
└slackmodule.py
```

> 環境変数
* CHANNEL_ID：通知先slack channel（channel名でも、IDでも。）
    * 通知先はBotが参加しているchannelに限る。
* TOKEN：`slack app` のToken
* SLACK_DOMAIN:チャンネルリンク生成用ドメイン（任意）

> 基本設定

* タイムアウト：1分
    * slackのチャンネル数が多いと時間がかかる。

#### EventBridge

> パターンを定義
* Cron 式：`0 0 ? * MON *`
    * 毎週月曜日に通知

> ターゲットを設定
先に作成したLambda関数を指定。

## Running the tests
開発環境用のインストールコマンドにはテストのライブラリが含まれています。

* `flake8` : 文法チェック。コーディング規約`PEP 8`に準拠したソースチェックスタイル。
* `mypy` : 型ヒントによる構文チェック。（指定ディレクトリの直下しか対象にしてくれないので手動で実行）
* `black` : 制限が強めの自動フォーマッタ。`PEP 8`にも準拠しているのでこれに沿っておけば間違いはない。
* `pytest`：ユニットテスト。
