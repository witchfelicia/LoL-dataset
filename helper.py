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
