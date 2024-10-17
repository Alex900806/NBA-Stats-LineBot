import os


def deleteImageFromDemo(image_name):
    # demo 目錄在當前文件所在的上一層資料夾中
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    demo_directory = os.path.join(project_root, "demo")

    # 拼接完整的圖片路徑，添加 .png 擴展名
    image_path = os.path.join(demo_directory, f"{image_name}.png")

    # 判斷圖片是否存在，存在則刪除
    if os.path.exists(image_path):
        try:
            os.remove(image_path)
            print("deleteImageFromDemo() 執行完成")
            return True
        except Exception as e:
            print("deleteImageFromDemo() 執行失敗 " + str(e))
            return False
    else:
        print("deleteImageFromDemo() 無法找到檔案")
        return False


# 測試函數
if __name__ == "__main__":
    deleteImageFromDemo("Kawhi_Leonard_shot_chart")
