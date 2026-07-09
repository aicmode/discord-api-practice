# discord-api-practice

## 課題概要

Discord webhookを使って、Pythonから特定のDiscordチャンネルに自動通知を送信するプログラムです。

送信するメッセージ:

```text
AIエンジニア講座 課題8 Discord webhook通知テストです。Pythonから自動通知を送信しました。
```

## 使用技術

- Python
- requests
- python-dotenv
- Discord Webhook

## ファイル構成

```text
discord-api-practice/
├── discord_notify.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## セットアップ方法

1. 仮想環境を作成します。

```bash
python3 -m venv .venv
```

2. 仮想環境を有効化します。

```bash
source .venv/bin/activate
```

3. 必要なライブラリをインストールします。

```bash
pip install -r requirements.txt
```

## .envの作成方法

`.env.example`をコピーして、`.env`ファイルを作成します。

```bash
cp .env.example .env
```

作成した`.env`を開き、DiscordのWebhook URLを入力します。

```env
DISCORD_WEBHOOK_URL=ここに本物のWebhook URLを入力してください
```

## 実行方法

以下のコマンドでプログラムを実行します。

```bash
python discord_notify.py
```

## 動作確認方法

実行後、ターミナルに以下のように表示されれば成功です。

```text
Discordへの通知送信に成功しました
```

Discordの指定チャンネルに通知メッセージが投稿されていることも確認してください。

失敗した場合は、ターミナルにステータスコードやエラー内容が表示されます。Webhook URLが正しいか、`.env`に設定できているかを確認してください。

## セキュリティ上の注意

- Discord Webhook URLは外部に公開しないでください。
- `.env`には本物のWebhook URLを書くため、GitHubに公開してはいけません。
- このプロジェクトでは`.gitignore`に`.env`を追加して、Gitの管理対象から外しています。
- `.env.example`には本物のWebhook URLを書かず、設定例だけを記載してください。
