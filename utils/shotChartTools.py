from nba_api.stats.endpoints import shotchartdetail
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd


def getShotData(id: int, team_ids: int, seasons: str):

    df = pd.DataFrame()
    shot_data = shotchartdetail.ShotChartDetail(
        team_id=team_ids,
        player_id=id,
        context_measure_simple="PTS",
        season_nullable=seasons,
    )
    df = pd.concat([df, shot_data.get_data_frames()[0]])

    return df


def drawShotChart(
    df: pd.DataFrame,
    name: str,
    season=True,
    RA=True,
    extent=(-250, 250, -47.5, 422.5),  # 修改 extent 使 ymin < ymax
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
        gridsize=gridsize,
        mincnt=2,
        extent=extent,  # 確保 ymin 小於 ymax
    )

    ax = drawCourt(ax, "black")

    return fig


def drawCourt(ax: mpl.axes, color="white"):
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
