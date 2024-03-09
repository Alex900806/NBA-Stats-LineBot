import pandas as pd

df = pd.read_csv('data/bestPlayer.csv')

if df is not None:
    # 初始化訊息
    message = ""
    # 將每個球員的數據添加到訊息中
    for index, row in df.iterrows():
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

print(message)