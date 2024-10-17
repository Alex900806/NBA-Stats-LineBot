import os
import sys
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
import matplotlib
import matplotlib.pyplot as plt

# 將項目根目錄添加到 sys.path，不然找不到 utils
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from utils.shotChartTools import drawShotChart, getShotData

matplotlib.use("Agg")  # 設定非互動式後端，避免 GUI 問題


def getShotChartPath(player_name):
    playerInfo = getPlayerInfo(player_name)
    if playerInfo == "Unknown Player":
        return "請輸入正確球員姓名"
    else:
        shot_data = getShotData(playerInfo[0], playerInfo[2], playerInfo[1])
        chart = drawShotChart(
            df=shot_data, name=player_name, season=playerInfo[1], RA=False
        )
        filename = f"{'_'.join(player_name.split(' '))}_shot_chart.png"
        folder_path = "demo"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_path = f"{folder_path}/{filename}"
        chart.savefig(file_path)
        plt.close(chart)
        return file_path


def getPlayerInfo(player_name):
    playerId = None
    for item in players.get_players():
        if item["full_name"].lower() == player_name.lower():
            playerId = item["id"]
            break

    if playerId is not None:
        playerCareerStats_dict = playercareerstats.PlayerCareerStats(
            player_id=str(playerId), per_mode36="PerGame"
        ).get_dict()
        currentSeason = playerCareerStats_dict["resultSets"][0]["rowSet"][-1]
        playerStats = [
            playerId,  # 球員Id
            currentSeason[1],  # seasonId
            currentSeason[3],  # teamId
        ]
        return playerStats
    else:
        return "Unknown Player"


# test
if __name__ == "__main__":
    res = getShotChartPath("Kawhi Leonard")
    print(res)
