import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter

## new imports, hope trigger methods
from slackclient import SlackClient
import json
from flask import make_response

env_path = Path('.') / '.env'
load_dotenv(dotenv_path = env_path)

app = Flask(__name__) # necessary to run flask app

slack_event_adapter = SlackEventAdapter(
    os.environ['SIGING_SECRECT'], 
    '/slack/events', 
    app) # vai lidar com os diversos eventos enviados a nois pelo slack_api

client  = slack.WebClient(token = os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call('auth.test')['user_id']

count_reactions = {}

# The endpoint Slack will load your menu options from https://github.com/slackapi/python-message-menu-example/blob/master/example.py
@app.route("/slack/message_options", methods=["POST"])
def message_options():
    # Parse the request payload
    form_json = json.loads(request.form["payload"])


    # Dictionary of menu options which will be sent as JSON
    menu_options = {
        "options": [
            {
                "text": "Cappuccino",
                "value": "cappuccino"
            },
            {
                "text": "Latte",
                "value": "latte"
            }
        ]
    }

    # Load options dict as JSON and respond to Slack
    return Response(json.dumps(menu_options), mimetype='application/json')

# The endpoint Slack will send the user's menu selection to
@app.route("/slack/message_actions", methods=["POST"])
def message_actions():

    # Parse the request payload
    form_json = json.loads(request.form["payload"])
    channel_id = form_json.get('item', {}).get('channel')

    # Check to see what the user's selection was and update the message accordingly
    selection = form_json["actions"][0]["selected_options"][0]["value"]

    if selection == "cappuccino":
        message_text = "cappuccino"
    else:
        message_text = "latte"

    response = client.api_call(
      "chat.update",
      channel=form_json["channel"]["id"],
      ts=form_json["message_ts"],
      text="One {}, right coming up! :coffee:".format(message_text),
      attachments=[] # empty `attachments` to clear the existing massage attachments
    )

    # Send an HTTP 200 response with empty body so Slack knows we're done here
    return make_response("", 200)

# A Dictionary of message attachment options
attachments_json = [
    {
        "fallback": "Upgrade your Slack client to use messages like these.",
        "color": "#3AA3E3",
        "attachment_type": "default",
        "callback_id": "menu_options_2319",
        "actions": [
            {
                "name": "bev_list",
                "text": "Pick a beverage...",
                "type": "select",
                "data_source": "external"
            }
        ]
    }
]

# Send a message with the above attachment, asking the user if they want coffee
client.api_call(
  "chat.postMessage",
  channel="#test_create",
  text="Would you like some coffee? :coffee:",
  attachments=attachments_json
)

# @app.client.reactions_get:
# def emoji_message(reactions):
#     message_full = reactions.get('message', {})
#     # channel = reactions.get('channel')
#     # user_id = message_full.get('user')
#     # text = message_full.get('text')
#     # emoji = message_full.get('reaction', {})
#     # emoji_usado = emoji.get('nome')

#     print(message_full)

#     # if BOT_ID != user_id:
#     #     client.chat_postMessage(channel = channel, text = f'{text} {emoji_usado}')


@slack_event_adapter.on('reaction_added')
def reaction(payload):

    event = payload.get('event', {})
    emoji = event.get('reaction')
    message = event.get('item', {}).get('type')
    channel_id = event.get('item', {}).get('channel')
    user_id = event.get('user')

    print(event)

    if BOT_ID != user_id:
        client.chat_postMessage(channel = channel_id, text = f':{emoji}: {message}')

    return Response(), 200

# @app.route('/contar-reacao', methods = ['POST'])
# def contar_reacao():
#     data = request.form
#     user_id = data.get('user_id')
#     channel_id = data.get('channel_id')
#     print(data)

#     client.chat_postMessage(channel=channel_id, text=f"Message: command feito")

#     return Response(), 200


@slack_event_adapter.on('message')
def message(payload):
    #print(payload)
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

    if BOT_ID != user_id:
        client.chat_postMessage(channel = channel_id, text = 'f{}')


if __name__ == "__main__":
        app.run(debug=True, port = 5004, use_reloader=False)