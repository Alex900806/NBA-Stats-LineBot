import os 
# 獲取當前應用程序的根目錄
base_dir = os.path.dirname(os.path.abspath(__file__))

        # 完整的圖片路徑
image_path = os.path.join(base_dir, 'photos', 'image.png')

print(image_path)
