import pandas as pd
from nba_api.stats.endpoints import leaguestandings
import threading

# 定義全域變數 state 和 state_lock
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


# 定義一個函式來執行 get_standings()，並將其返回值存儲到全域變數 state 中
def get_standings_async():
    global state
    with state_lock:
        state = get_standings()
