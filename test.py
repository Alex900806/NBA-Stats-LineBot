import pandas as pd

# 讀取 CSV 檔案
df = pd.read_csv('data/bestPlayer.csv')

# print(df.to_html())
        
# 將結果轉換為文字訊息
message = ""
for index, row in df.iterrows():
    message += f'{index}: {row[1]}, {row[2]}\n'


print(message)

