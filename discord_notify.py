import os
from datetime import datetime
from zoneinfo import ZoneInfo

import requests
from dotenv import load_dotenv


# Discord Embedで使用する重要度ごとの表示名と色（整数値）です。
SEVERITY_SETTINGS = {
    "1": {"label": "🟢 通常", "color": 0x2ECC71},
    "2": {"label": "🟠 重要", "color": 0xF39C12},
    "3": {"label": "🔴 緊急", "color": 0xE74C3C},
}
CANCEL_WORDS = {"exit", "quit"}


def load_webhook_url():
    """.envを読み込み、Discord Webhook URLを返します。"""
    load_dotenv()
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    if not webhook_url:
        print("エラー：.envにDISCORD_WEBHOOK_URLが設定されていません。")
        print(".envの設定内容を確認してください。")
        return None

    return webhook_url


def input_title():
    """有効な通知タイトルを受け取ります。キャンセル時はNoneを返します。"""
    while True:
        title = input("通知タイトルを入力してください：").strip()

        if title.lower() in CANCEL_WORDS:
            return None
        if not title:
            print("タイトルが入力されていません。もう一度入力してください。")
        elif len(title) > 256:
            print("タイトルは256文字以内で入力してください。")
            print(f"現在の文字数：{len(title)}文字")
        else:
            return title


def input_body():
    """有効な通知本文を受け取ります。キャンセル時はNoneを返します。"""
    while True:
        body = input("通知本文を入力してください：").strip()

        if body.lower() in CANCEL_WORDS:
            return None
        if not body:
            print("通知本文が入力されていません。もう一度入力してください。")
        elif len(body) > 4096:
            print("通知本文は4096文字以内で入力してください。")
            print(f"現在の文字数：{len(body)}文字")
        else:
            return body


def select_severity():
    """1～3から重要度を選んでもらい、設定情報を返します。"""
    while True:
        print("重要度を選択してください。")
        print("1：通常")
        print("2：重要")
        print("3：緊急")
        choice = input("選択：").strip()

        if choice in SEVERITY_SETTINGS:
            return SEVERITY_SETTINGS[choice]

        print("1、2、3のいずれかを入力してください。")


def confirm_notification(title, body, severity_label):
    """送信内容を表示し、yならTrue、nならFalseを返します。"""
    print("\n送信する通知")
    print("--------------------")
    print(f"タイトル：{title}")
    print(f"本文：{body}")
    print(f"重要度：{severity_label}")
    print("--------------------")

    while True:
        answer = input("この内容で送信しますか？（y/n）：").strip().lower()
        if answer == "y":
            return True
        if answer == "n":
            return False
        print("y または n を入力してください。")


def format_japan_datetime(sent_at):
    """日時を「2026年7月10日 21:30:00」の形式に整えます。"""
    return (
        f"{sent_at.year}年{sent_at.month}月{sent_at.day}日 "
        f"{sent_at:%H:%M:%S}"
    )


def create_embed(title, body, severity, sent_at):
    """Discordへ送るEmbedデータを作成します。"""
    sent_at_text = format_japan_datetime(sent_at)
    return {
        "title": title,
        "description": body,
        "color": severity["color"],
        "fields": [
            {
                "name": "重要度",
                "value": severity["label"],
                "inline": True,
            },
            {
                "name": "送信日時",
                "value": sent_at_text,
                "inline": True,
            },
        ],
        "footer": {"text": "Discord API Practice Notification"},
        # Discord側でも正しい時刻情報として扱えるようISO形式も設定します。
        "timestamp": sent_at.isoformat(),
    }


def send_discord_notification(webhook_url, embed, severity_label, sent_at_text):
    """Discord WebhookへEmbed通知を送信します。"""
    payload = {"embeds": [embed]}

    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
    except requests.exceptions.Timeout:
        print("Discord通知の送信がタイムアウトしました。")
        print("通信環境を確認して、時間をおいて再度実行してください。")
        return False
    except requests.exceptions.RequestException as error:
        print("Discord通知の送信中に通信エラーが発生しました。")
        print(f"エラー内容：{error}")
        return False

    # Discordは成功時に204を返すことがあるため、すべての2xxを成功とします。
    if 200 <= response.status_code <= 299:
        print(f"ステータスコード：{response.status_code}")
        print("Discord通知の送信に成功しました")
        print(f"重要度：{severity_label}")
        print(f"送信日時：{sent_at_text}")
        return True

    print("Discord通知の送信に失敗しました。")
    print(f"ステータスコード：{response.status_code}")
    print(f"Discordからのエラー内容：{response.text or 'エラー内容はありません。'}")
    return False


def main():
    """入力からDiscord通知の送信まで、プログラム全体を管理します。"""
    webhook_url = load_webhook_url()
    if not webhook_url:
        return

    try:
        while True:
            title = input_title()
            if title is None:
                print("Discord通知の送信をキャンセルしました。")
                return

            body = input_body()
            if body is None:
                print("Discord通知の送信をキャンセルしました。")
                return

            severity = select_severity()
            if not confirm_notification(title, body, severity["label"]):
                print("通知内容を最初から入力し直します。\n")
                continue

            # 確認後、実際に送信する直前の日本時間を記録します。
            sent_at = datetime.now(ZoneInfo("Asia/Tokyo"))
            sent_at_text = format_japan_datetime(sent_at)
            embed = create_embed(title, body, severity, sent_at)
            send_discord_notification(
                webhook_url, embed, severity["label"], sent_at_text
            )
            return
    except (EOFError, KeyboardInterrupt):
        print("\nDiscord通知の送信をキャンセルしました。")


if __name__ == "__main__":
    main()
