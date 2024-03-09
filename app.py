# LineBot Flask 套件
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage


from findBestPlayer import get_nba_player_stats
from dotenv import load_dotenv
import pandas as pd
import os

app = Flask(__name__)
# 加載 .env 文件中的環境變數
load_dotenv()
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

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
    sortRule = event.message.text
    sortRule = sortRule.split(" ")
    if sortRule:
        state = get_nba_player_stats(sort_columns=sortRule)
        if state == "Completed":
            # 讀取 CSV 檔案
            df = pd.read_csv('data/bestPlayer.csv')
            if df is not None:
                # 初始化訊息
                message = ""
                # 將每個球員的數據添加到訊息中
                for index, row in df.iterrows():
                    message += "球隊名稱: " + row['球隊名稱'] + "\n"
                    for col in df.columns[1:]:
                        message += f"{col}: {row[col]}\n"
                        message += "\n"

                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=message)
                )
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)