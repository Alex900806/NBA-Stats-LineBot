from imgurpython import ImgurClient
import settings


def upload_picture(client_data, album, img_path, name="shot-chart", title="shot-chart"):
    config = {
        "album": album,
        "name": name,
        "title": title,
        "description": "shot-chart",
    }

    image = client_data.upload_from_path(img_path, config=config, anon=False)
    return image


def upload(local_img_file):
    client_id = settings.CLIENT_ID
    client_secret = settings.CLIENT_SECRET
    access_token = settings.ACCESS_TOKEN
    refresh_token = settings.REFRESH_TOKEN
    album = settings.ALBUM
    local_img_file = local_img_file

    client = ImgurClient(client_id, client_secret, access_token, refresh_token)
    image = upload_picture(client, album, local_img_file)

    return image["link"]


# 測試用
# link = upload("shot_data/test.png")
# print(link)
# print(type(link)) string
