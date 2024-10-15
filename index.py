# LineBot Flask 套件
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage

# 本專案需要的套件
import os
import warnings
import requests
import pandas as pd
from functions.getGuideMessage import getGuideMessage
from functions.getLeagueStandings import getLeagueStandings
from functions.getPlayersStatistics import getPlayersStatistics
import utils.config as config

# 忽略特定的棄用警告
warnings.filterwarnings("ignore", category=DeprecationWarning)

app = Flask(__name__)

# 連接 LineBot 的兩個金鑰
line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(config.LINE_CHANNEL_SECRET)


# Loading Animation
def send_loading_animation(user_id):
    url = "https://api.line.me/v2/bot/chat/loading/start"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config.LINE_CHANNEL_ACCESS_TOKEN}",
    }
    data = {"chatId": user_id, "loadingSeconds": 60}
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 202:
        print("載入動畫顯示成功")
    else:
        print(f"載入動畫失敗: {response.status_code}, {response.text}")


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
    user_id = event.source.user_id  # 獲取使用者識別碼
    send_loading_animation(user_id)

    if textSendByUser == "使用指南":
        message = getGuideMessage()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))

    elif textSendByUser == "聯盟戰績":
        message = getLeagueStandings()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))

    elif textSendByUser[0:3] == "可視化":
        # basic
        playerName = textSendByUser[3:].strip()

        if playerName == "Kawhi Leonard":
            image_message = ImageSendMessage(
                original_content_url="https://i.imgur.com/NSyGDBU.png",
                preview_image_url="https://i.imgur.com/NSyGDBU.png",
            )
            line_bot_api.reply_message(event.reply_token, image_message)
        else:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="請輸入正確球員名字")
            )

        # developing...

        # playerName = textSendByUser[4:]
        # loop = asyncio.get_event_loop()
        # link = loop.run_until_complete(main(playerName))

        # if link != "Failed":
        #     image_message = ImageSendMessage(
        #         original_content_url=link,
        #         preview_image_url=link,
        #     )
        #     line_bot_api.reply_message(event.reply_token, image_message)
        # else:
        #     message = "搜尋失敗 請重新輸入"
        #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))

    else:
        sortRule = textSendByUser.split(" ")  # 獲取排序規則
        state = getPlayersStatistics(sort_columns=sortRule)

        if state == "Successful":
            df = pd.read_csv("data/playersStatistics.csv")

            if df is not None:
                messages = []
                for index, row in df.iterrows():
                    message = (
                        f"名稱: {row['名稱']} ({row['球隊名稱']})\n"
                        f"位置: {row['位置']}\n"
                        f"得分: {row['得分']}\n"
                        f"籃板（進攻/防守）: {row['籃板']}（{row['進攻籃板']} / {row['防守籃板']}）\n"
                        f"助攻: {row['助攻']}\n"
                        f"抄截: {row['抄截']}\n"
                        f"火鍋: {row['火鍋']}\n"
                        f"投籃進球數/命中率: {row['投籃進球數']} / {row['投籃命中率']}\n"
                        f"三分進球數/命中率: {row['三分進球數']} / {row['三分命中率']}\n"
                        f"罰球進球數/命中率: {row['罰球進球數']} / {row['罰球命中率']}\n"
                        f"失誤: {row['失誤']}\n"
                        f"犯規: {row['犯規']}\n"
                        f"正負值: {row['正負值']}\n"
                        f"上場時間: {row['上場時間']}分鐘\n"
                        "----------------------------\n"
                    )
                    messages.append(message)

                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="".join(messages).rstrip(" -")),
                )
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=state))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
