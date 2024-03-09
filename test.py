from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from findBestPlayer import get_nba_player_stats
import matplotlib.pyplot as plt
from io import BytesIO
import pandas as pd
import os

get_nba_player_stats()

# 讀取 CSV 檔案
df = pd.read_csv('data/bestPlayer.csv')

# 遍歷DataFrame的每一行，並將數據組成所需的格式
reply_message = ""
for index, row in df.iterrows():
    team_info = f"球隊名稱：{row['球隊名稱']}\n名稱：{row['名稱']}\n位置：{row['位置']}\n得分：{row['得分']}\n進攻籃板：{row['進攻籃板']}\n防守籃板：{row['防守籃板']}\n籃板：{row['籃板']}\n助攻：{row['助攻']}\n抄截：{row['抄截']}\n火鍋：{row['火鍋']}\n投籃進球數：{row['投籃進球數']}\n投籃命中率：{row['投籃命中率']}\n三分進球數：{row['三分進球數']}\n三分命中率：{row['三分命中率']}\n罰球進球數：{row['罰球進球數']}\n罰球命中率：{row['罰球命中率']}\n犯規：{row['犯規']}\n失誤：{row['失誤']}\n正負值：{row['正負值']}\n上場時間：{row['上場時間']}\n\n"
    reply_message += team_info

print(reply_message.strip())

# # 將 DataFrame 轉換為圖片
# fig, ax = plt.subplots(figsize=(15, 10), dpi=200)  # 調整圖片大小和解析度
# ax.axis('tight')
# ax.axis('off')
# table = ax.table(cellText=df.values, colLabels=df.columns, loc='center')

# # 調整表格字型大小
# table.auto_set_font_size(False)
# table.set_fontsize(8)  # 設置字型大小為 10

# # 設置第二列單元格寬度
# col_width = 0.12  # 自訂寬度
# for i in range(len(df)+1):  # 迭代行
#     cell = table[(i, 1)]  # 取得第二列每一行的單元格
#     cell.set_width(col_width)

# # 將所有單元格中的文字置中
# for cell in table.get_celld().values():
#     cell.set_text_props(ha='center', va='center')  # 設置水平和垂直對齊方式均為置中


# # 將圖片存入 BytesIO 對象中
# buffer = BytesIO()
# plt.savefig(buffer, format='png')
# buffer.seek(0)

# # 將圖片保存到 photos 資料夾中
# filename = 'image.png'
# filepath = os.path.join("photos", filename)
# with open(filepath, 'wb') as f:
#     f.write(buffer.getvalue())

