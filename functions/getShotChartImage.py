import os
import sys

# 將項目根目錄添加到 sys.path，不然找不到 utils
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from utils.getShotChartPath import getShotChartPath
from utils.getImageLink import getImageLink


def getShotChartImage(player_name):
    file_path = getShotChartPath(player_name)
    image_link = getImageLink(file_path)

    return image_link


# test
if __name__ == "__main__":
    res = getShotChartImage("Kawhi Leonard")
    print(res)
