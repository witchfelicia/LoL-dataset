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

# combine JSON {a: [1, 2]} + {a: [3, 4]} -> {a: [1, 2, 3, 4]}

def concat_json(json_obj_1, json_obj_2):
    if json_obj_1 == {}:
        # swap if first one empty
        return json_obj_2
    # copied from Stackoverflow -> https://stackoverflow.com/a/66060526

    hold_json_obj = {}
    # We'll loop through every item in the json_obj_1 dictionary
    for item_1 in json_obj_1:
        # We'll also loop through every item in the json_obj_2 dictionary
        for item_2 in json_obj_2:
            # Now let's compare whether they are the same KEYS (not values)
            if item_1 == item_2:
                # if they match, we create a list to store the array
                hold_array = []
                hold_array.extend(json_obj_1[item_1])
                hold_array.extend(json_obj_2[item_1])
                
                # finally putting the array to our hold_json_obj
                hold_json_obj[item_1] = hold_array
            else:
                # if they don't match, check if the key already exists in the
                # hold_json_obj because we might be iterating json_obj_2 for the second time.
                if item_2 not in hold_json_obj:
                    #add the ummatched array to hold_json_obj
                    hold_json_obj[item_2] = json_obj_2[item_2]
    
    return hold_json_obj