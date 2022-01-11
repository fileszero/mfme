from linebot import (
 LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import mylib

config = mylib.get_config()

ACCESS_TOKEN = config["LINE"]["token"]
SECRET = config["LINE"]["channel_secret"]

line_bot_api = LineBotApi(ACCESS_TOKEN)
line_bot_api.broadcast(TextSendMessage(text='Hello World!'))