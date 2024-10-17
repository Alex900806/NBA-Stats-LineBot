import os
import sys

# 將項目根目錄添加到 sys.path，不然找不到 utils
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

import utils.config as config
from imgurpython import ImgurClient


def getImageLink(img_path):
    client_id = config.CLIENT_ID
    client_secret = config.CLIENT_SECRET
    access_token = config.ACCESS_TOKEN
    refresh_token = config.REFRESH_TOKEN
    album = config.ALBUM

    try:
        client = ImgurClient(client_id, client_secret, access_token, refresh_token)
        image = uploadImage(
            client,
            album,
            img_path,
            name=img_path.split(".")[0][5:],
            title=img_path.split(".")[0][5:],
        )
    except Exception as e:
        print("Get Image Link Error\n" + str(e))
        return {"status": 500, "message": "處理投籃熱度圖片失敗 請重試"}

    return {
        "status": 200,
        "message": image["link"],
        "id": image["id"],
        "name": image["name"],
    }


def uploadImage(client_data, album, img_path, name, title):
    config = {
        "album": album,
        "name": name,
        "title": title,
        "description": f"{title} (upload automated)",
    }

    try:
        image = client_data.upload_from_path(img_path, config=config, anon=False)
        return image
    except Exception as e:
        print("Upload Image Error\n" + str(e))
        return False


# 測試用
if __name__ == "__main__":
    link = getImageLink("demo/Kawhi_Leonard_shot_chart_demo.png")
    print(link)
