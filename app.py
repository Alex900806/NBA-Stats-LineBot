# LineBot Flask 套件
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# 本專案需要的套件
from findBestPlayer import get_nba_player_stats
import pandas as pd
import os

# 創建 Flask 應用程式
app = Flask(__name__)

# 連接 LineBot 的金鑰
line_bot_api = LineBotApi("eePfeX1FNoCtfl48u4HebyFSazpfZALB6fWOGdsCqArij7PZ+ywF/TEb5swwWjU+PFUpg7UqcfM3SJahDVyXf3SSZumO1UU2aQpRyG2h5tcT7/+sjeWNghomNc0mcQsJAAFXQWFcckWGxgqHXfNQIAdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("179e63fc2b3635b3fb11b814354ca98d")

# 定義路由 "/callback" 來處理 LINE Messaging API 的 POST 請求
@app.route("/callback", methods=['POST'])
def callback():
    # 從請求標頭中取得簽名
    signature = request.headers['X-Line-Signature']
    # 取得請求內容
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        # 驗證簽名並處理請求
        handler.handle(body, signature)
    except InvalidSignatureError:
        # 簽名無效時回傳 400 錯誤
        abort(400)
    # 回傳 'OK' 表示處理成功
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 從使用者傳遞的訊息中取得排序規則
    sortRule = event.message.text
    sortRule = sortRule.split(" ")  # 根據空格切分排序規則
    if sortRule:
        # 根據排序規則取得 NBA 球員數據
        state = get_nba_player_stats(sort_columns=sortRule)
        
        if state == "Completed":
            # 讀取 CSV 檔案
            df = pd.read_csv('data/bestPlayer.csv')
            if df is not None:
                # 初始化訊息
                message = ""
                # 將每個球員的數據添加到訊息中
                for index, row in df.iterrows():
                    # 格式化球員數據
                    message += f"名稱: {row['名稱']} ({row['球隊名稱']})\n"
                    message += f"位置: {row['位置']}\n"
                    message += f"得分: {row['得分']}\n"
                    message += f"進攻/防守籃板: {row['進攻籃板']} / {row['防守籃板']}\n"
                    message += f"籃板: {row['籃板']}\n"
                    message += f"助攻: {row['助攻']}\n"
                    message += f"抄截: {row['抄截']}\n"
                    message += f"火鍋: {row['火鍋']}\n"
                    message += f"投籃進球數/命中率: {row['投籃進球數']} / {row['投籃命中率']}\n"
                    message += f"三分進球數/命中率: {row['三分進球數']} / {row['三分命中率']}\n"
                    message += f"罰球進球數/命中率: {row['罰球進球數']} / {row['罰球命中率']}\n"
                    message += f"犯規: {row['犯規']}\n"
                    message += f"失誤: {row['失誤']}\n"
                    message += f"正負值: {row['正負值']}\n"
                    message += f"上場時間: {row['上場時間']}分鐘\n"
                    message += "------------------------\n"

                # 回覆訊息給使用者
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))
        else:
            message = "今天比賽還沒結束喔 再等一下吧~"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))



if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)