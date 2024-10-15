import os
import sys
import pandas as pd
from requests.exceptions import ReadTimeout
from nba_api.stats.endpoints import leaguestandings

# 將項目根目錄添加到 sys.path，不然找不到 utils
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from utils.getTeamAbbreviationById import idToNameTable


def getLeagueStandings():
    try:
        standings = leaguestandings.LeagueStandings(timeout=60).get_dict()
    except ReadTimeout:
        return "伺服器忙線中 請稍候再試"
    except Exception as e:
        print(f"發生錯誤：{str(e)}")
        return "發生未知錯誤 請稍候再試"

    standings_data = {"East": [], "West": []}

    for standings in standings["resultSets"][0]["rowSet"]:
        team_id = standings[2]
        team_abbreviation = idToNameTable.get(team_id)
        team_info = {
            "球隊名稱": team_abbreviation,
            "戰績": f"{standings[12]}-{standings[13]}",
        }

        conference = standings[5]
        standings_data[conference].append(team_info)

    # 處理並格式化訊息
    message = ""
    for conference_name, data in standings_data.items():
        if data:
            df = pd.DataFrame(data).sort_values("戰績", ascending=False)
            message += formatMessage(df, conference_name)

    return message


def formatMessage(df, conference_name):
    message = f"---{conference_name} Conference---\n"
    for index, row in df.iterrows():
        rank = f"{index+1}.".ljust(3)
        team = row["球隊名稱"].ljust(3)
        record = row["戰績"].rjust(5)
        message += f"{rank} {team}  {record}\n"
    message += "\n"

    return message


# test
if __name__ == "__main__":
    print(getLeagueStandings())
