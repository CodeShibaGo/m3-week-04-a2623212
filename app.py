from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv('YOUR_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('YOUR_CHANNEL_SECRET'))
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_response(prompt, role="user"):
    pass



@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 加上openAI的回覆

    if 'ai' in event.message.text:
        print("Here is AI start!")
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是一個精通英文、正體中文、日文的公司秘書"},
            {"role": "user", "content": event.message.text},
        ]
        )

        # text= completion['choices'][0]['message']['content']
        text=completion.choices[0].message.content
    else:
        # 原本的回覆
        text=event.message.text
    line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text)
            )

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)