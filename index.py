from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
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

# 處理 Line Bot 接收到的文字訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    sortRule = event.message.text

    if sortRule:
        # 執行你的程式並獲取排序後的結果
        get_nba_player_stats(sort_columns=[sortRule])
        
        # 設置 Matplotlib 使用中文字體
        plt.rcParams['font.family'] = 'Heiti TC'  # 指定中文字體
        plt.rcParams['axes.unicode_minus'] = False  # 解決負號無法正確顯示的問題

        # 讀取 CSV 檔案
        df = pd.read_csv('data/bestPlayer.csv')
        
        # 將 DataFrame 轉換為圖片
        fig, ax = plt.subplots(figsize=(12, 8), dpi=400)  # 調整圖片大小和解析度
        ax.axis('tight')
        ax.axis('off')
        ax.table(cellText=df.values, colLabels=df.columns, loc='center')

        # 將圖片存入 BytesIO 對象中
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # 將圖片保存到 photos 資料夾中
        filename = 'image.png'
        filepath = os.path.join("photos", filename)
        with open(filepath, 'wb') as f:
            f.write(buffer.getvalue())

        # 發送圖片給用戶
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="這是您要的數據資料"),
            ImageSendMessage(
                original_content_url='https://github.com/Alex900806/NBA-Status-LineBot/blob/main/photos/image.png',
                preview_image_url='https://github.com/Alex900806/NBA-Status-LineBot/blob/main/photos/image.png'
            )
        )
  
       
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)
