import os
import time
import requests
import json

class SlackBot:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://slack.com/api"

    def get_reactions(self, channel, timestamp):
        url = f"{self.base_url}/reactions.get"
        params = {
            "token": self.token,
            "channel": channel,
            "timestamp": timestamp
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        return None

    def listen_for_reactions(self, channel):
        latest_ts = None
        while True:
            reactions = self.get_reactions(channel, latest_ts)
            if reactions and reactions["message"]["ts"] != latest_ts:
                latest_ts = reactions["message"]["ts"]
                message_text = reactions["message"]["text"]
                reaction = reactions["reaction"]
                print(f"New reaction on message: {message_text} - Reaction: {reaction}")
            time.sleep(1)

if __name__ == "__main__":
    bot = SlackBot(os.environ["SLACK_BOT_TOKEN"])
    bot.listen_for_reactions("General")

## In this version of the code, the text of the message that got a reaction is logged along with the reaction itself.
### This should give you an idea of how to access the message metadata in the Slack API.
## You can use this information to identify the specific message that got a reaction, and take any necessary actions in response.