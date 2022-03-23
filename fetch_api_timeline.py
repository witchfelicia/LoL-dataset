import requests
import os
import json

from dotenv import load_dotenv
load_dotenv()

REGION_URL = 'americas.api.riotgames.com/lol/'
MATCH_INFORMATION_ENDPOINT = 'match/v5/matches/'
API_KEY = os.getenv("LEAGUE_API_KEY")

# want: gold at 10 min (600k milliseconds). maybe kills too?
# compared to lane opponent (how do i calc this)

def get_timeline_data(match_id):
    get_url = 'https://' + REGION_URL + MATCH_INFORMATION_ENDPOINT
    r = requests.get(get_url + match_id + '/timeline', 
				headers={"X-Riot-Token": API_KEY})

    data = r.json()
    # print(data.keys())
    # dict_keys(['metadata', 'info'])
    # print(data['info'].keys())
    # dict_keys(['frameInterval', 'frames', 'gameId', 'participants'])
    # print(data['info']['participants'][0]['puuid'])
    # print(data['info']['frameInterval']) # tells us that they take a frame every min
    # print(data['info']['frames'][10].keys())
    # print(data['info']['frames'][10].keys())
    # dict_keys(['events', 'participantFrames', 'timestamp'])
    # print(data['info']['frames'][10]['participantFrames'].keys())
    # participants are in order! <3
    # dict_keys(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])

    # get gold of 1st player at 10min
    # print(data['info']['frames'][10]['participantFrames']['1'].keys())
    # dict_keys(['championStats', 'currentGold', 'damageStats', 'goldPerSecond', 
    # 'jungleMinionsKilled', 'level', 'minionsKilled', 'participantId', 'position', 
    # 'timeEnemySpentControlled', 'totalGold', 'xp'])



    
    url = 'https://' + REGION_URL + MATCH_INFORMATION_ENDPOINT
    r2 = requests.get(url + match_id,
	 headers={"X-Riot-Token": API_KEY})
    
    game_data = r2.json()

    """
    # fill cols with champion name + position
    champion = []
    position_played = []
    for player in game_data["info"]["participants"]:
        champion.append(player['championName'])
        position_played.append(player['individualPosition'])
    
    ten_min_gold = []
    for index in range(1,11):
        ten_min_gold.append(data['info']['frames'][10]['participantFrames'][str(index)]['totalGold'])
    
    # todo: indexing to find who the lane opponent is
    opponent_ten_min_gold = [0] * 10 
    
    for index in range(0,5):
        print()
        for jndex in range(5,10):
            if position_played[index] == position_played[jndex]: 
                print(f"The {position_played[index]} on other team is {champion[jndex]}! They earned {ten_min_gold[jndex]}")
                opponent_ten_min_gold[index] = ten_min_gold[jndex]
                opponent_ten_min_gold[jndex] = ten_min_gold[index]
                break;
    
    
    dataset = {
        "champion": champion,
        "positionPlayed": position_played,
        "10MinGold": ten_min_gold,
        "laneOpponentGold": opponent_ten_min_gold
    }
    """

    with open('lane_opponent.json', 'w') as s:
        s.write(json.dumps(dataset, indent = 4))
    

get_timeline_data('NA1_4226412134')
