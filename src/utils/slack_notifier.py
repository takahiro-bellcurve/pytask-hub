import json
import requests


class SlackNotifier:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_message(self, text, channel="#general", username="Notifier", icon_emoji=None, attachments=None, blocks=None):
        payload = {
            "channel": channel,
            "username": username,
            "text": text,
            "icon_emoji": icon_emoji,
            "attachments": attachments,
            "blocks": blocks
        }
        # 空の属性を削除
        payload = {k: v for k, v in payload.items() if v is not None}

        response = requests.post(self.webhook_url, data=json.dumps(
            payload), headers={'Content-Type': 'application/json'})
        return response.ok

    def send_success_message(self, task_name, channel="#general"):
        text = f":white_check_mark: タスク '{task_name}' が正常に完了しました。"
        return self.send_message(text, channel)

    def send_failure_message(self, task_name, error_message, channel="#general"):
        text = f":x: タスク '{task_name}' に失敗しました。\nエラー: {error_message}"
        return self.send_message(text, channel)
