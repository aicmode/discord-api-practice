import os

import requests
from dotenv import load_dotenv


# .envファイルに書いた環境変数を読み込みます。
load_dotenv()


# DiscordのWebhook URLは、コードに直接書かず.envから取得します。
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# Discordに送信するメッセージです。
MESSAGE = "AIエンジニア講座 課題8 Discord webhook通知テストです。Pythonから自動通知を送信しました。"


def send_discord_notification():
    """Discord webhookを使って通知メッセージを送信します。"""
    if not WEBHOOK_URL:
        print("エラー: .envにDISCORD_WEBHOOK_URLが設定されていません")
        return

    payload = {
        "content": MESSAGE,
    }

    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=10)

        if response.status_code in (200, 204):
            print("Discordへの通知送信に成功しました")
        else:
            print("Discordへの通知送信に失敗しました")
            print(f"ステータスコード: {response.status_code}")
            print(f"エラー内容: {response.text}")
    except requests.exceptions.RequestException as error:
        print("Discordへの通知送信に失敗しました")
        print(f"エラー内容: {error}")


if __name__ == "__main__":
    send_discord_notification()
