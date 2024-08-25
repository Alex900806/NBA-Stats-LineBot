from imgurpython import ImgurClient
import utils.config as config


def getImageLink(img_path):
    client_id = config.CLIENT_ID
    client_secret = config.CLIENT_SECRET
    access_token = config.ACCESS_TOKEN
    refresh_token = config.REFRESH_TOKEN
    album = config.ALBUM

    try:
        client = ImgurClient(client_id, client_secret, access_token, refresh_token)
        image = uploadImage(
            client, album, img_path, name=img_path[10:], title=img_path[10:]
        )
    except Exception as e:
        return str(e)

    return image["link"]


def uploadImage(client_data, album, img_path, name, title):
    config = {
        "album": album,
        "name": name,
        "title": title,
        "description": "shot chart uploaded by automated",
    }

    try:

        image = client_data.upload_from_path(img_path, config=config, anon=False)
    except Exception as e:
        return str(e)

    return image


# 測試用
if __name__ == "__main__":
    link = getImageLink("shot_data/Kawhi_Leonard_shot_chart.png")
    print(link)  # str
