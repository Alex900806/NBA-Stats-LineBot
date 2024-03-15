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
            teamInfo["戰績"] = str(standings[12]) + "-" + str(standings[13])
            eastStandings.append(teamInfo)

        elif standings[5] == "West":
            teamInfo["球隊名稱"] = str(standings[3]) + " " + str(standings[4])
            teamInfo["戰績"] = str(standings[12]) + "-" + str(standings[13])
            westStandings.append(teamInfo)

    eastStandings_DF = pd.DataFrame(eastStandings).sort_values("戰績", ascending=False)
    eastStandings_DF.to_csv("data/eastStandings.csv", index=False)
    westStandings_DF = pd.DataFrame(westStandings).sort_values("戰績", ascending=False)
    westStandings_DF.to_csv("data/westStandings.csv", index=False)


def get_standings_async():
    global state
    standings = get_standings()
    with state_lock:
        state = standings
        return state


def handle_standings_request():
    global state
    t = threading.Thread(target=get_standings_async)
    t.start()
    t.join(timeout=10)  # 等待子執行緒完成，最多等待10秒
    message = "現在戰績狀況如下：\n"
    East_df = pd.read_csv("data/eastStandings.csv")
    if not East_df.empty:
        message += "----------東區戰績----------\n"
        for index, row in East_df.iterrows():
            rank = f"{index+1}.".ljust(3)  # 將排名左對齊並填充空格至長度3
            team = row["球隊名稱"].ljust(22)  # 將球隊名稱左對齊並填充空格至長度20
            record = row["戰績"]  # 戰績保持原樣
            message += f"{rank} {team} {record}\n"
        West_df = pd.read_csv("data/westStandings.csv")
    if not West_df.empty:
        message += "\n----------西區戰績----------\n"
        for index, row in West_df.iterrows():
            rank = f"{index+1}.".ljust(3)  # 將排名左對齊並填充空格至長度3
            team = row["球隊名稱"].ljust(22)  # 將球隊名稱左對齊並填充空格至長度20
            record = row["戰績"]  # 戰績保持原樣
            message += f"{rank} {team} {record}\n"
    return message


# print(handle_standings_request())
