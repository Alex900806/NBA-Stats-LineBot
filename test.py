import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import os

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

