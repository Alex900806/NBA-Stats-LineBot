from dotenv import load_dotenv
import os

# 加載 .env 文件中的環境變數
load_dotenv()

# 獲取環境變數的值
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

# 確認環境變數是否被正確加載
print(LINE_CHANNEL_ACCESS_TOKEN)
print(LINE_CHANNEL_SECRET)