from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from findBestPlayer import get_nba_player_stats
import pandas as pd

# 讀取 CSV 檔案
df = pd.read_csv('data/bestPlayer.csv')

# 初始化訊息
message = ""

# 將每個球員的數據添加到訊息中
for index, row in df.iterrows():
    message += "球隊名稱: " + row['球隊名稱'] + "\n"  # 添加球員名稱
    for col in df.columns[1:]:  # 從第二列開始迭代，因為第一列是名稱
        message += f"{col}: {row[col]}\n"  # 添加球員的其他數據列
    message += "\n"  # 添加一個換行符，用於分隔不同球員的數據

# 打印訊息
print(type(message))

