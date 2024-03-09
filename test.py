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

text = df.to_string(index=False)
print(type(text))

# 遍歷DataFrame的每一行，並將數據組成所需的格式
# reply_message = ""
# for index, row in df.iterrows():
#     team_info = f"球隊名稱：{row['球隊名稱']}\n名稱：{row['名稱']}\n位置：{row['位置']}\n得分：{row['得分']}\n進攻籃板：{row['進攻籃板']}\n防守籃板：{row['防守籃板']}\n籃板：{row['籃板']}\n助攻：{row['助攻']}\n抄截：{row['抄截']}\n火鍋：{row['火鍋']}\n投籃進球數：{row['投籃進球數']}\n投籃命中率：{row['投籃命中率']}\n三分進球數：{row['三分進球數']}\n三分命中率：{row['三分命中率']}\n罰球進球數：{row['罰球進球數']}\n罰球命中率：{row['罰球命中率']}\n犯規：{row['犯規']}\n失誤：{row['失誤']}\n正負值：{row['正負值']}\n上場時間：{row['上場時間']}\n\n"
#     reply_message += team_info

# print(reply_message.strip())


