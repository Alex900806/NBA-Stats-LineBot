from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
from shot import shot_chart, get_shot_data
import matplotlib.pyplot as plt


def get_player_info(playerName):
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
            currentSeason[26],  # 得分
            currentSeason[21],  # 助攻
            currentSeason[20],  # 籃板
            currentSeason[8],  # 上場時間
            currentSeason[24],  # 失誤
            currentSeason[1],  # seasonId
            currentSeason[3],  # teamId
        ]
        return playerStats
    else:
        return "Unknown Player"


def get_shot_picture_async(playerName):
    playerInfo = get_player_info(playerName)
    if playerInfo == "Unknown Player":
        return "ERROR"
    else:
        shot_data = get_shot_data(playerInfo[0], playerInfo[7], playerInfo[6])
        shot_data.head()
        chart2 = shot_chart(shot_data, playerName, playerInfo[6], RA=False)
        filename = f"{playerName}_shot_chart.png"
        file_path = f"shot_data/{filename}"
        chart2.savefig(file_path)
        plt.close(chart2)
        return file_path


def handle_get_shot_picture(playerName, event):
    t = threading.Thread(target=handle_get_shot_picture_async, args=(playerName, event))
    t.start()
    t.join(timeout=5)


def handle_get_shot_picture_async(playerName):
    file_path = get_shot_picture_async(playerName)
    if file_path == "ERROR":
        message = "找不到此球員的數據資料"
    else:
        message = file_path
    return message


# 測試用
# res = get_shot_picture("Kawhi Leonard")
# print(res)
# print(type(res)) str
