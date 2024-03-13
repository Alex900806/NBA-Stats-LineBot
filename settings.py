from dotenv import load_dotenv
import os

# 連接 LineBot 的金鑰
load_dotenv(encoding="utf-8")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')