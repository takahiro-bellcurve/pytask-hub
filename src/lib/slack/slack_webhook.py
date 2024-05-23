import json

import requests


class SlackWebhook():
    def __init__(self, webhook_url: str, channel: str, username: str):
        self.webhook_url = webhook_url
        self.channel = channel
        self.username = username

    def post(self, message: str, has_error: bool = False):
        color = "#00FF33"
        if has_error:
            color = "#FF0000"

        data = {
            "attachments": [
                {
                    "fallback": "Required plain-text summary of the attachment.",
                    "color": color,
                    "text": message,
                    "mrkdwn_in": ["text", "pretext"]
                }
            ],
            "channel": self.channel,
            "username": self.username
        }

        return requests.post(self.webhook_url, data=json.dumps(data))
