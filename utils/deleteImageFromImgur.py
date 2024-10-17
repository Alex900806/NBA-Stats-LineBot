import os
import sys

# 將項目根目錄添加到 sys.path，不然找不到 utils
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

import utils.config as config
from imgurpython import ImgurClient


def deleteImageFromImgur(image_id):
    try:
        client_id = config.CLIENT_ID
        client_secret = config.CLIENT_SECRET
        access_token = config.ACCESS_TOKEN
        refresh_token = config.REFRESH_TOKEN

        client = ImgurClient(client_id, client_secret, access_token, refresh_token)
        response = client.delete_image(image_id)

        print("deleteImageFromImgur() 執行完成")
        return response

    except Exception as e:
        print("deleteImageFromImgur() 執行失敗")
        print("Delete Image Error\n" + str(e))
        return False


if __name__ == "__main__":
    res = deleteImageFromImgur("ydSjq4O")
    print(res)  # True or Error message
