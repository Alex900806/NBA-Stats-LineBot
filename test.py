from nba_api.live.nba.endpoints import scoreboard, boxscore

# box = boxscore.BoxScore('0022300906').game
# for player in box.get_dict()['homeTeam']['players']:
#         # # 創建主隊單一球員數據資料(dict)
#     print(player)

# 當天所有比賽的所有資料
gamesAll = scoreboard.ScoreBoard().games
    # 將資料轉成列表，每一個元素是字典
gameData = gamesAll.get_dict()

    # 找出當天所有比賽的 gameId(list)
gameIdSet = []
for game in gameData:
    gameIdSet.append(game['gameId'])

print(gameIdSet)