from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from findBestPlayer import get_nba_player_stats
import matplotlib.pyplot as plt
from io import BytesIO
import pandas as pd
import os

app = Flask(__name__)

line_bot_api = LineBotApi('eePfeX1FNoCtfl48u4HebyFSazpfZALB6fWOGdsCqArij7PZ+ywF/TEb5swwWjU+PFUpg7UqcfM3SJahDVyXf3SSZumO1UU2aQpRyG2h5tcT7/+sjeWNghomNc0mcQsJAAFXQWFcckWGxgqHXfNQIAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('179e63fc2b3635b3fb11b814354ca98d')


# 設置 Line Bot 的 Webhook 路由，用於接收 Line Bot 的訊息
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    # 驗證 Line Bot 的簽名
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    sortRule = event.message.text
    # 執行你的程式並獲取排序後的結果
    get_nba_player_stats(sort_columns=[sortRule])

    # 讀取 CSV 檔案
    df = pd.read_csv('data/bestPlayer.csv')

    # 遍歷DataFrame的每一行，並將數據組成所需的格式
    reply_message = ""
    for row in df.iterrows():
        team_info = f"球隊名稱：{row['球隊名稱']}\n名稱：{row['名稱']}\n位置：{row['位置']}\n得分：{row['得分']}\n進攻籃板：{row['進攻籃板']}\n防守籃板：{row['防守籃板']}\n籃板：{row['籃板']}\n助攻：{row['助攻']}\n抄截：{row['抄截']}\n火鍋：{row['火鍋']}\n投籃進球數：{row['投籃進球數']}\n投籃命中率：{row['投籃命中率']}\n三分進球數：{row['三分進球數']}\n三分命中率：{row['三分命中率']}\n罰球進球數：{row['罰球進球數']}\n罰球命中率：{row['罰球命中率']}\n犯規：{row['犯規']}\n失誤：{row['失誤']}\n正負值：{row['正負值']}\n上場時間：{row['上場時間']}\n\n"
        reply_message += team_info
    
    # 回覆處理後的訊息
    message = TextSendMessage(text=reply_message)  # 使用strip()方法移除最後的空行
    line_bot_api.reply_message(event.reply_token, message)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)