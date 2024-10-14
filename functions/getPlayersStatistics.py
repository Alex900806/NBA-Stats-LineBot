import pandas as pd
from nba_api.live.nba.endpoints import scoreboard, boxscore


def getPlayersStatistics(sort_columns=["得分"]):
    all_games_data = scoreboard.ScoreBoard().games.get_dict()  # 當天所有比賽的資料
    game_id_array = [data["gameId"] for data in all_games_data]  # 當天所有比賽的 gameId

    # 確認比賽是否全數開打
    try:
        game_data = getGameData(game_id_array)
        all_games_started = True
    except:
        all_games_started = False

    if all_games_started:
        try:
            statistics = getGameStatistics(game_data, sort_columns)
            statistics.to_csv("data/playersStatistics.csv", index=False)
            return "Successful"

        except:
            return "數據處理錯誤 請稍候再試"

    elif not all_games_started:
        return "尚有比賽仍未開打 請稍候再試"


def createPlayerData(player, team_data):
    return {
        "球隊名稱": team_data["teamTricode"],
        "名稱": player["name"],
        "位置": player.get("position", "Bench"),
        "得分": player["statistics"]["points"],
        "進攻籃板": player["statistics"]["reboundsOffensive"],
        "防守籃板": player["statistics"]["reboundsDefensive"],
        "籃板": player["statistics"]["reboundsTotal"],
        "助攻": player["statistics"]["assists"],
        "抄截": player["statistics"]["steals"],
        "火鍋": player["statistics"]["blocks"],
        "投籃進球數": player["statistics"]["fieldGoalsMade"],
        "投籃命中率": f"{int(player['statistics']['fieldGoalsPercentage'] * 100)}%",
        "三分進球數": player["statistics"]["threePointersMade"],
        "三分命中率": f"{int(player['statistics']['threePointersPercentage'] * 100)}%",
        "罰球進球數": player["statistics"]["freeThrowsMade"],
        "罰球命中率": f"{int(player['statistics']['freeThrowsPercentage'] * 100)}%",
        "犯規": player["statistics"]["foulsPersonal"],
        "失誤": player["statistics"]["turnovers"],
        "正負值": int(player["statistics"]["plusMinusPoints"]),
        "上場時間": player["statistics"]["minutesCalculated"][2:4],
    }


def getGameData(game_id_array):
    game_data = []
    for game_id in game_id_array:
        single_game_data = boxscore.BoxScore(game_id).game.get_dict()
        game_data.append(single_game_data)

    return game_data


def getGameStatistics(game_data, sort_columns):
    all_game_statics = []

    for data in game_data:
        one_game_statics = []
        for player in data["homeTeam"]["players"]:
            player_data = createPlayerData(player, data["homeTeam"])
            one_game_statics.append(player_data)

        for player in data["awayTeam"]["players"]:
            player_data = createPlayerData(player, data["awayTeam"])
            one_game_statics.append(player_data)

        all_game_statics.append(one_game_statics)

    all_game_statics_df = pd.concat(
        [pd.DataFrame(game_statics) for game_statics in all_game_statics]
    )

    if not all_game_statics_df.empty:
        return all_game_statics_df.sort_values(by=sort_columns, ascending=False).head(
            10
        )
    else:
        raise ValueError("無效輸入 請重新輸入")


# test
if __name__ == "__main__":
    print(getPlayersStatistics())
