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
                print(f"New reaction: {reactions['reaction']}")
            time.sleep(1)

if __name__ == "__main__":
    bot = SlackBot(os.environ["SLACK_BOT_TOKEN"])
    bot.listen_for_reactions("general")

# This example uses the requests library to make API calls to Slack, and the os library to get the Slack bot token from an environment variable.
# The listen_for_reactions method continuously listens for new reactions in the specified channel, and the get_reactions method gets the latest reactions for a given message.
# In this example, the bot prints the name of each new reaction as it is received. You can modify the code to suit your needs and add more functionality as required.