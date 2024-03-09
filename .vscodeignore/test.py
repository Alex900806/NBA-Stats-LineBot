from nba_api.live.nba.endpoints import scoreboard, boxscore
# # 當天所有比賽的所有資料
# gamesAll = scoreboard.ScoreBoard().games
#     # 將資料轉成列表，每一個元素是字典
# gameData = gamesAll.get_dict()

#     # 找出當天所有比賽的 gameId(list)
gameIdSet = ['1', '2', '3', '4', '5']
# for game in gameData:
#     gameIdSet.append(game['gameId'])

    # 用 gameId 來從 boxscore 找出該比賽的資料
gamePlayAlready = True
try:
    box = boxscore.BoxScore(gameId).game
except Exception as e:
    gamePlayAlready = False

if gamePlayAlready == True:
    for gameId in gameIdSet:
        print(gameId)
