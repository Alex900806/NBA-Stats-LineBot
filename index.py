# LineBot Flask 套件
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# 本專案需要的套件
from findBestPlayer import get_nba_player_stats
from standings import handle_standings_request
import settings
import pandas as pd
import os

# 創建 Flask 應用程式
app = Flask(__name__)

# 連接 LineBot 的兩個金鑰
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)

received_player_name = None


# 定義路由 "/callback" 來處理 LINE Messaging API 的 POST 請求
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]  # 從請求標頭中取得簽名
    body = request.get_data(as_text=True)  # 取得請求內容
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)  # 驗證簽名並處理請求
    except InvalidSignatureError:
        abort(400)  # 簽名無效時回傳 400 錯誤
    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    textSendByUser = event.message.text  # 獲取使用者傳遞的訊息

    if textSendByUser == "使用指南":
        message = "我能每天提供最佳球員數據 🏀\n\n您可以從三種預設的排序方式快速使用，也可以透過「自定義輸入」來選擇喜歡的排序方式\n如：輸入「得分」，就會依照得分來排序今日得分前10名的球員\n\n能輸入的關鍵字有：\n得分、籃板、進攻籃板、防守籃板、助攻、抄截、火鍋、投籃進球數、投籃命中率、三分進球數、三分命中率、罰球進球數、罰球命中率、失誤、犯規、正負值、上場時間\n\n與 NBA Stats 一起快速看數據吧！"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))

    elif textSendByUser == "聯盟戰績":
        message = handle_standings_request()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))

    elif textSendByUser == "球員可視化數據":
        message = "請提供想查看的球員名字(英文全名)"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))
        received_player_name = ""

    elif received_player_name is not None:
        # # 根據球員名字生成可視化數據
        # visualization_image = generate_player_visualization(received_player_name)

        # # 將生成的圖片傳送給用戶
        # line_bot_api.reply_message(
        #     event.reply_token,
        #     ImageSendMessage(
        #         original_content_url=visualization_image_url,
        #         preview_image_url=visualization_image_url,
        #     ),
        # )
        message = textSendByUser
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))

    else:
        sortRule = textSendByUser.split(" ")  # 獲取排序規則
        state = get_nba_player_stats(
            sort_columns=sortRule
        )  # 根據排序規則取得 NBA 球員數據

        if state == "Completed":
            df = pd.read_csv("data/bestPlayer.csv")  # 讀取 CSV 檔案

            if df is not None:
                message = ""  # 初始化訊息
                for index, row in df.iterrows():
                    message += f"名稱: {row['名稱']} ({row['球隊名稱']})\n"
                    message += f"位置: {row['位置']}\n"
                    message += f"得分: {row['得分']}\n"
                    message += f"籃板（進攻/防守）: {row['籃板']}（{row['進攻籃板']} / {row['防守籃板']}）\n"
                    message += f"助攻: {row['助攻']}\n"
                    message += f"抄截: {row['抄截']}\n"
                    message += f"火鍋: {row['火鍋']}\n"
                    message += f"投籃進球數/命中率: {row['投籃進球數']} / {row['投籃命中率']}\n"
                    message += f"三分進球數/命中率: {row['三分進球數']} / {row['三分命中率']}\n"
                    message += f"罰球進球數/命中率: {row['罰球進球數']} / {row['罰球命中率']}\n"
                    message += f"失誤: {row['失誤']}\n"
                    message += f"犯規: {row['犯規']}\n"
                    message += f"正負值: {row['正負值']}\n"
                    message += f"上場時間: {row['上場時間']}分鐘\n"
                    message += "----------------------------\n"
                message = message[:-29]
                # 回覆訊息給使用者
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text=message)
                )

        elif state == "Failed":
            message = "比賽尚未全部結束喔 請稍等~"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))

        elif state == "Sort Error":
            message = "無效輸入 請重新輸入"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))


# main function
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))
    app.run(host="0.0.0.0", port=port)
