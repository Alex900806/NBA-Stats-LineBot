import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import os

# 設置 Matplotlib 使用中文字體（微軟正黑體）
plt.rcParams['font.family'] = 'Heiti TC'  # 指定中文字體
plt.rcParams['axes.unicode_minus'] = False  # 解決負號無法正確顯示的問題

# 讀取 CSV 檔案
df = pd.read_csv('data/bestPlayer.csv')

# 將 DataFrame 轉換為圖片
fig, ax = plt.subplots(figsize=(15, 10), dpi=200)  # 調整圖片大小和解析度
ax.axis('tight')
ax.axis('off')
table = ax.table(cellText=df.values, colLabels=df.columns, loc='center')

# 調整表格字型大小
table.auto_set_font_size(False)
table.set_fontsize(8)  # 設置字型大小為 10

# 設置第二列單元格寬度
col_width = 0.12  # 自訂寬度
for i in range(len(df)+1):  # 迭代行
    cell = table[(i, 1)]  # 取得第二列每一行的單元格
    cell.set_width(col_width)

# 將所有單元格中的文字置中
for cell in table.get_celld().values():
    cell.set_text_props(ha='center', va='center')  # 設置水平和垂直對齊方式均為置中


# 將圖片存入 BytesIO 對象中
buffer = BytesIO()
plt.savefig(buffer, format='png')
buffer.seek(0)

# 將圖片保存到 photos 資料夾中
filename = 'image.png'
filepath = os.path.join("photos", filename)
with open(filepath, 'wb') as f:
    f.write(buffer.getvalue())

