from dotenv import load_dotenv

# 連接 LineBot 的金鑰
load_dotenv(encoding="utf-8")
CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')