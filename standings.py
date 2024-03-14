import threading
import pandas as pd
from nba_api.stats.endpoints import leaguestandings

state = None
state_lock = threading.Lock()


def get_standings():
    standings_dict = leaguestandings.LeagueStandings().get_dict()
    # 東西區戰績資料
    eastStandings = []
    westStandings = []

    for standings in standings_dict["resultSets"][0]["rowSet"]:
        # 各球隊戰績資料
        teamInfo = {}
        if standings[5] == "East":
            teamInfo["球隊名稱"] = str(standings[3]) + " " + str(standings[4])
            teamInfo["戰績"] = (
                str(standings[12])
                + "-"
                + str(standings[13])
                + " ("
                + (str(standings[14])[1:])
                + ")"
            )
            teamInfo["最近10場"] = standings[19]
            if standings[35] > 0:
                teamInfo["近期狀態"] = "W" + str(standings[35])
            else:
                teamInfo["近期狀態"] = "L" + str(standings[35])[1:]
            eastStandings.append(teamInfo)

        elif standings[5] == "West":
            teamInfo["球隊名稱"] = str(standings[3]) + " " + str(standings[4])
            teamInfo["戰績"] = (
                str(standings[12])
                + "-"
                + str(standings[13])
                + " ("
                + (str(standings[14])[1:])
                + ")"
            )
            teamInfo["最近10場"] = standings[19]
            if standings[35] > 0:
                teamInfo["近期狀態"] = "W" + str(standings[35])
            else:
                teamInfo["近期狀態"] = "L" + str(standings[35])[1:]
            westStandings.append(teamInfo)

    eastStandings_DF = pd.DataFrame(eastStandings).sort_values("戰績", ascending=False)
    eastStandings_DF.to_csv("data/eastStandings.csv", index=False)
    westStandings_DF = pd.DataFrame(westStandings).sort_values("戰績", ascending=False)
    westStandings_DF.to_csv("data/westStandings.csv", index=False)

    return "OK"


def get_standings_async():
    global state
    with state_lock:
        state = get_standings()


def handle_standings_request():
    global state
    t = threading.Thread(target=get_standings_async)
    t.start()
    t.join()  # 等待子執行緒完成
    if state == "OK":
        message = ""
        East_df = pd.read_csv("data/eastStandings.csv")
        if not East_df.empty:
            message += "東區戰績\n"
            for index, row in East_df.iterrows():
                message += f"{index+1}. {row['球隊名稱']} {row['戰績']}\n"
        West_df = pd.read_csv("data/westStandings.csv")
        if not West_df.empty:
            message += "西區戰績\n"
            for index, row in West_df.iterrows():
                message += f"{index+1}. {row['球隊名稱']} {row['戰績']}\n"
        return message
    else:
        return "處理失敗 請重新輸入"
