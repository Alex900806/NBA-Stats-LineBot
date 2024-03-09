import pandas as pd
from nba_api.live.nba.endpoints import scoreboard, boxscore

def get_nba_player_stats(sort_columns=['得分']):
    # 當天所有比賽的所有資料
    gamesAll = scoreboard.ScoreBoard().games
    # 將資料轉成列表，每一個元素是字典
    gameData = gamesAll.get_dict()

    # 找出當天所有比賽的 gameId(list)
    gameIdSet = []
    for game in gameData:
        gameIdSet.append(game['gameId'])

    # 今日所有比賽的資料
    allGameStatics = []

    # 找出該比賽所有球員的數據資料(list)
    # (team Tricode, name, position, points, reboundsOffensive, reboundsDefensive, reboundsTotal, assists, steals, blocks, fieldGoalsMade, fieldGoalsPercentage, threePointersMade, threePointersPercentage, freeThrowsMade, freeThrowsPercentage, foulsPersonal, turnovers, plusMinusPoints, minutesCalculated)
    gameStaticsAll = []

    # 用 gameId 來從 boxscore 找出該比賽的資料
    for gameId in gameIdSet:
        # 當天每場比賽的資料
        box = boxscore.BoxScore(gameId).game
        for player in box.get_dict()['homeTeam']['players']:
            # 創建主隊單一球員數據資料(dict)
            playerStatus = {}
            playerStatus['球隊名稱'] = box.get_dict()['homeTeam']['teamTricode']
            playerStatus['名稱'] = player['name']
            playerStatus['位置'] = player.get('position', 'Bench')
            playerStatus['得分'] = player['statistics']['points']
            playerStatus['進攻籃板'] = player['statistics']['reboundsOffensive']
            playerStatus['防守籃板'] = player['statistics']['reboundsDefensive']
            playerStatus['籃板'] = player['statistics']['reboundsTotal']
            playerStatus['助攻'] = player['statistics']['assists']
            playerStatus['抄截'] = player['statistics']['steals']
            playerStatus['火鍋'] = player['statistics']['blocks']
            playerStatus['投籃進球數'] = player['statistics']['fieldGoalsMade']
            playerStatus['投籃命中率'] = str(int(player['statistics']['fieldGoalsPercentage']*100))+ "%"
            playerStatus['三分進球數'] = player['statistics']['threePointersMade']
            playerStatus['三分命中率'] = str(int(player['statistics']['threePointersPercentage']*100))+ "%"
            playerStatus['罰球進球數'] = player['statistics']['freeThrowsMade']
            playerStatus['罰球命中率'] = str(int(player['statistics']['freeThrowsPercentage']*100))+ "%"
            playerStatus['犯規'] = player['statistics']['foulsPersonal']
            playerStatus['失誤'] = player['statistics']['turnovers']
            playerStatus['正負值'] = int(player['statistics']['plusMinusPoints'])
            playerStatus['上場時間'] = player['statistics']['minutesCalculated'][2:4]
            gameStaticsAll.append(playerStatus)

        for player in box.get_dict()['awayTeam']['players']:
            # 創建客隊單一球員數據資料(dict)
            playerStatus = {}
            playerStatus['球隊名稱'] = box.get_dict()['awayTeam']['teamTricode']
            playerStatus['名稱'] = player['name']
            playerStatus['位置'] = player.get('position', 'Bench')
            playerStatus['得分'] = player['statistics']['points']
            playerStatus['進攻籃板'] = player['statistics']['reboundsOffensive']
            playerStatus['防守籃板'] = player['statistics']['reboundsDefensive']
            playerStatus['籃板'] = player['statistics']['reboundsTotal']
            playerStatus['助攻'] = player['statistics']['assists']
            playerStatus['抄截'] = player['statistics']['steals']
            playerStatus['火鍋'] = player['statistics']['blocks']
            playerStatus['投籃進球數'] = player['statistics']['fieldGoalsMade']
            playerStatus['投籃命中率'] = str(int(player['statistics']['fieldGoalsPercentage']*100))+ "%"
            playerStatus['三分進球數'] = player['statistics']['threePointersMade']
            playerStatus['三分命中率'] = str(int(player['statistics']['threePointersPercentage']*100))+ "%"
            playerStatus['罰球進球數'] = player['statistics']['freeThrowsMade']
            playerStatus['罰球命中率'] = str(int(player['statistics']['freeThrowsPercentage']*100))+ "%"
            playerStatus['犯規'] = player['statistics']['foulsPersonal']
            playerStatus['失誤'] = player['statistics']['turnovers']
            playerStatus['正負值'] = int(player['statistics']['plusMinusPoints'])
            playerStatus['上場時間'] = player['statistics']['minutesCalculated'][2:4]
            gameStaticsAll.append(playerStatus)
        
        allGameStatics.append(gameStaticsAll)


    for game in allGameStatics:
        gameStaticsAll_DF = pd.DataFrame(game)
        allGameStatics_DF = pd.concat([gameStaticsAll_DF])
    
    allGameStatics_DF = allGameStatics_DF.sort_values(sort_columns, ascending=False).head(10)
    allGameStatics_DF.to_csv('data/bestPlayer.csv', index=False)
    
    return "Completed"
