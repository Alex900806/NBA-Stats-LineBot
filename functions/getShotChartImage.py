import os
import sys

# 將項目根目錄添加到 sys.path，不然找不到 utils
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from utils.getShotChartPath import getShotChartPath
from utils.getImageLink import getImageLink


def getShotChartImage(player_name):
    file_path = getShotChartPath(player_name)

    if file_path == "請輸入正確球員姓名":
        print("getShotChartImage() 請輸入正確球員姓名")
        return {"status": 500, "message": file_path}
    else:
        image_link = getImageLink(file_path)
        if image_link["status"] == 500:
            print("getShotChartImage() 處理投籃熱度圖片失敗")
            return {"status": 500, "message": "處理投籃熱度圖片失敗 請重試"}
        else:
            print("getShotChartImage() 執行完成")
            return {
                "status": 200,
                "message": image_link["message"],
                "id": image_link["id"],
                "name": image_link["name"],
            }


# test
if __name__ == "__main__":
    res = getShotChartImage("Kawhi Leonard")
    print(res)
