from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
from shot import shot_chart, get_shot_data
import matplotlib.pyplot as plt


async def get_player_info(playerName):
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
            currentSeason[1],  # seasonId
            currentSeason[3],  # teamId
        ]
        return playerStats
    else:
        return "Unknown Player"


async def get_shot_picture(playerName):
    playerInfo = await get_player_info(playerName)
    if playerInfo == "Unknown Player":
        return "ERROR"
    else:
        shot_data = get_shot_data(playerInfo[0], playerInfo[2], playerInfo[1])
        shot_data.head()
        chart2 = shot_chart(shot_data, playerName, playerInfo[1], RA=False)
        filename = f"{playerName}_shot_chart.png"
        file_path = f"shot_data/{filename}"
        chart2.savefig(file_path)
        plt.close(chart2)
        return file_path


# 定義 main 函數來處理可視化請求
async def main(playerName):
    file_path = await get_shot_picture(playerName)
    if file_path == "ERROR":
        return "找不到此球員的數據資料"
    else:
        return file_path
