# -*- coding: utf-8 -*-

import slack

import mylib

config = mylib.get_config()
# https://api.slack.com/apps OAuth & Permissions
client = slack.WebClient(config["slack"]["token"])
response = client.chat_postMessage(
    channel='#random',
    text="Hello world!")
print(response)
