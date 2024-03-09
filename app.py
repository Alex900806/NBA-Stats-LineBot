from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)
from findBestPlayer import get_nba_player_stats
import pandas as pd
import os

app = Flask(__name__)

line_bot_api = LineBotApi('eePfeX1FNoCtfl48u4HebyFSazpfZALB6fWOGdsCqArij7PZ+ywF/TEb5swwWjU+PFUpg7UqcfM3SJahDVyXf3SSZumO1UU2aQpRyG2h5tcT7/+sjeWNghomNc0mcQsJAAFXQWFcckWGxgqHXfNQIAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('179e63fc2b3635b3fb11b814354ca98d')

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

    if sortRule:
        # # 執行你的程式並獲取排序後的結果
        # get_nba_player_stats(sort_columns=[sortRule])
        
        # # 讀取 CSV 檔案
        # df = pd.read_csv('data/bestPlayer.csv')
        
        # # 將結果轉換為文字訊息
        # message = "你好"
        # # for row in df.iterrows():
        # #     message += f'{row['名稱']} - {row[sortRule]}\n'
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=sortRule)
        )

# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     message = TextSendMessage(text=event.message.text)
#     line_bot_api.reply_message(event.reply_token, message)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)