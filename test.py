def get_nba_player_stats(sort_columns=['得分']):
    print(sort_columns)

# sortRule = "得分 助攻 籃板"
sortRule = "助攻 籃板"
sortRule = sortRule.split(" ")

get_nba_player_stats(sort_columns=[sortRule])



