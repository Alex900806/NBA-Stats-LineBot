import asyncio
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players

import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

from imgurpython import ImgurClient
import settings


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
    # print("完成 get_player_info")
    if playerInfo == "Unknown Player":
        return "ERROR"
    else:
        # 等待 get_shot_data 函數完成，並獲得結果
        shot_data = await get_shot_data(playerInfo[0], playerInfo[2], playerInfo[1])
        # print("完成 get_shot_data")
        chart2 = shot_chart(shot_data, playerName, playerInfo[1], RA=False)
        filename = f"{playerName}_shot_chart.png"
        file_path = f"shot_data/{filename}"
        chart2.savefig(file_path)
        plt.close(chart2)
        # print("完成 get_shot_picture")
        return file_path


def shot_chart(
    df: pd.DataFrame,
    name: str,
    season=True,
    RA=True,
    extent=(-250, 250, 422.5, -47.5),
    gridsize=25,
    cmap="Reds",
):
    fig = plt.figure(figsize=(3.6, 3.6), facecolor="white", edgecolor="white", dpi=100)
    ax = fig.add_axes([0, 0, 1, 1], facecolor="white")

    # Plot hexbin of shots
    if RA == True:
        x = df.LOC_X
        y = df.LOC_Y + 60
        # Annotate player name and season
        plt.text(-240, 430, f"{name}", fontsize=21, color="black")
        season = f"NBA {season[0][:4]}-{season[-1][-2:]}"
        plt.text(-250, -20, season, fontsize=8, color="black")
    else:
        cond = ~(
            (-45 < df.LOC_X) & (df.LOC_X < 45) & (-40 < df.LOC_Y) & (df.LOC_Y < 45)
        )
        x = df.LOC_X[cond]
        y = df.LOC_Y[cond] + 60
        # Annotate player name and season
        plt.text(-240, 430, f"{name}", fontsize=21, color="black")
        plt.text(-240, 400, "(Remove Restricted Area)", fontsize=10, color="red")
        season = f"NBA {season[0][:4]}-{season[-1][-2:]}"
        plt.text(-250, -20, season, fontsize=8, color="black")

    hexbin = ax.hexbin(
        x,
        y,
        cmap=cmap,
        bins="log",
        gridsize=25,
        mincnt=2,
        extent=(-250, 250, 422.5, -47.5),
    )

    # Draw court
    ax = create_court(ax, "black")

    return fig


def create_court(ax: mpl.axes, color="white"):
    # 底角三分線
    ax.plot([-220, -220], [0, 140], linewidth=2, color=color)
    ax.plot([220, 220], [0, 140], linewidth=2, color=color)
    # 圓弧三分線（圓心、半徑、高度、起始角度、終點角度）
    ax.add_artist(
        mpl.patches.Arc(
            (0, 140),
            440,
            315,
            theta1=0,
            theta2=180,
            facecolor="none",
            edgecolor=color,
            lw=2,
        )
    )
    # 禁區部分（框框）
    ax.plot([-80, -80], [0, 190], linewidth=2, color=color)
    ax.plot([80, 80], [0, 190], linewidth=2, color=color)
    ax.plot([-60, -60], [0, 190], linewidth=2, color=color)
    ax.plot([60, 60], [0, 190], linewidth=2, color=color)
    ax.plot([-80, 80], [190, 190], linewidth=2, color=color)

    # 中距離圓弧
    ax.add_artist(
        mpl.patches.Circle((0, 190), 60, facecolor="none", edgecolor=color, lw=2)
    )

    # 邊線
    ax.plot([-250, 250], [0, 0], linewidth=4, color="black")

    # 籃框
    ax.add_artist(
        mpl.patches.Circle((0, 60), 15, facecolor="none", edgecolor=color, lw=2)
    )
    # 籃板
    ax.plot([-30, 30], [40, 40], linewidth=2, color=color)

    # 省略刻度
    ax.set_xticks([])
    ax.set_yticks([])

    # 軸的邊界
    ax.set_xlim(-250, 250)
    ax.set_ylim(0, 470)
    return ax


async def get_shot_data(id: int, team_ids: int, seasons: str):
    from nba_api.stats.endpoints import shotchartdetail

    df = pd.DataFrame()
    shot_data = shotchartdetail.ShotChartDetail(
        team_id=team_ids,
        player_id=id,
        context_measure_simple="PTS",
        season_nullable=seasons,
    )
    df = pd.concat([df, shot_data.get_data_frames()[0]])

    return df


async def upload_picture(
    client_data, album, img_path, name="shot-chart", title="shot-chart"
):
    config = {
        "album": album,
        "name": name,
        "title": title,
        "description": "shot-chart",
    }

    image = client_data.upload_from_path(img_path, config=config, anon=False)
    return image


async def upload(local_img_file):
    client_id = settings.CLIENT_ID
    client_secret = settings.CLIENT_SECRET
    access_token = settings.ACCESS_TOKEN
    refresh_token = settings.REFRESH_TOKEN
    album = settings.ALBUM
    local_img_file = local_img_file

    client = ImgurClient(client_id, client_secret, access_token, refresh_token)
    image = await upload_picture(client, album, local_img_file)
    # print("完成 upload_picture")
    # print("完成 upload")
    return image["link"]


async def main(playerName):
    file_path = await get_shot_picture(playerName)
    link = await upload(file_path)
    return link


# 測試
# result = asyncio.run(handle_request("Stephen Curry"))
# print(result)
