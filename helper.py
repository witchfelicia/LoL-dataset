def fill_json(player):

    # creating JSON 
    objectives = {}

    objectives["deathsByEnemyChamps"] = player.get("deathsByEnemyChamps", "0") # 0 is default value if key is missing
    objectives["hadAfkTeammate"] = player.get("hadAfkTeammate", "0")
    objectives["kda"] = player.get("kda", "0")
    objectives["laningPhaseGoldExpAdvantage"] = player.get("laningPhaseGoldExpAdvantage", "0")
    objectives["maxLevelLeadLaneOpponent"] = player.get("maxLevelLeadLaneOpponent", "0")
    objectives["teamDamagePercentage"] = player.get("teamDamagePercentage", "0")
    objectives["visionScoreAdvantageLaneOpponent"] = player.get("visionScoreAdvantageLaneOpponent", "0")

    return objectives

# get column data of players' gold at 10 min
def get_ten_min_gold(game_data):
    gold_columns = []
    player_status = {}

    # game duration > 10 min
    if len(game_data) > 9:
        player_status = game_data[10]['participantFrames']
    else:
        player_status = game_data[-1]['participantFrames']
        print(f"game ended before 10 min. Last event was recorded at: {game_data[-1]['timestamp']} milliseconds.")
    
    # collect gold earned at 10 min
    for each in player_status.values():
        gold_columns.append(each['totalGold'])

    return gold_columns