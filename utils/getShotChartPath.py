from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
import matplotlib.pyplot as plt

from utils.shotChartTools import drawShotChart, getShotData



def getShotChartPath(player_name):
    playerInfo = getPlayerInfo(player_name)
    if playerInfo == "Unknown Player":
        return "ERROR"
    else:
        shot_data = getShotData(playerInfo[0], playerInfo[2], playerInfo[1])
        shot_data.head()
        chart2 = drawShotChart(shot_data, player_name, playerInfo[1], RA=False)
        filename = f"{"_".join(player_name.split(" "))}_shot_chart.png"
        file_path = f"shot_data/{filename}"
        chart2.savefig(file_path)
        plt.close(chart2)
        
        return file_path

def getPlayerInfo(playerName):
    playerId = None
    for item in players.get_players():
        if item["full_name"] == playerName:
            playerId = item["id"]
            break

    if playerId is not None:
        playerCarrerStats_dict = playercareerstats.PlayerCareerStats(
            player_id=str(playerId), per_mode36="PerGame"
        ).get_dict()
        currentSeason = playerCarrerStats_dict["resultSets"][0]["rowSet"][-1]
        playerStats = [
            playerId,  # 球員Id
            # currentSeason[26],  # 得分
            # currentSeason[21],  # 助攻
            # currentSeason[20],  # 籃板
            # currentSeason[8],  # 上場時間
            # currentSeason[24],  # 失誤
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
