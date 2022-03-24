import requests
import os
import json
import time

from fetch_api_test import get_matches, get_puuid
from fetch_api_test import get_matches
from summoners import summoner_list

from dotenv import load_dotenv
load_dotenv()

REGION_URL = 'americas.api.riotgames.com/lol/'
MATCH_INFORMATION_ENDPOINT = 'match/v5/matches/'
API_KEY = os.getenv("LEAGUE_API_KEY")

num_requests = 0

def reached_request_limit():
    global num_requests
    if num_requests >= 96:
        num_requests = 0
        print("Made 100 requests. Sleep for 2 min.")
        return True
    else:
        return False

# get champion name + position played columns
def fetch_position(match_id):
    if reached_request_limit():
        time.sleep(120)
        print("Resuming from fetch position")
    url = 'https://' + REGION_URL + MATCH_INFORMATION_ENDPOINT
    r2 = requests.get(url + match_id,
	 headers={"X-Riot-Token": API_KEY})
    global num_requests
    num_requests += 1
    
    game_data = r2.json()

    # fill cols with champion name + position
    champion = []
    position_played = []
    for player in game_data["info"]["participants"]:
        champion.append(player['championName'])
        position_played.append(player['individualPosition'])
    
    return champion, position_played

def get_game_data(match_id):
    # to not overwhelm the API
    if reached_request_limit():
        time.sleep(120)
        print("resume from get_game_data")

    get_url = 'https://' + REGION_URL + MATCH_INFORMATION_ENDPOINT
    r = requests.get(get_url + match_id + '/timeline', 
				headers={"X-Riot-Token": API_KEY})

    # TODO: verify request
    if r.status_code == requests.codes.ok:
        print(f"Request {get_url + match_id + '/timeline'} was successful!")
    else:
        print(f"Something happened with the request {get_url + match_id + '/timeline'}")
        print(f"Error code: {r.status_code}")
        print(f"Response body: {r.json}")
    
    data = r.json()

    global num_requests
    num_requests += 1

    champion, position_played = fetch_position(match_id)
    
    ten_min_gold = []
    for index in range(1,11):
        # TODO: better method of indexing data using data.get()
        print(data['info']['frames'][10]['participantFrames'][str(index)])
        ten_min_gold.append(data['info']['frames'][10]['participantFrames'][str(index)]['totalGold'])
    
    team = ["blue"] * 5
    for num in range(0, 5):
        team.append("red")
    opponent_ten_min_gold = [0] * 10 
    
    for index in range(0,5):
        for jndex in range(5,10):
            if position_played[index] == position_played[jndex]: 
                opponent_ten_min_gold[index] = ten_min_gold[jndex]
                opponent_ten_min_gold[jndex] = ten_min_gold[index]
                break;
    return({
        "champion": champion,
        "positionPlayed": position_played,
        "tenMinGold": ten_min_gold,
        "tenMinLaneOpponentGold": opponent_ten_min_gold,
        "team": team
    })

# get_game_data('NA1_4226412134')

def get_timeline_data():
    data = []
    for index, summoner in enumerate(summoner_list):
        global num_requests

        if reached_request_limit():
            time.sleep(120)
            print("_______________________")
            print("Resume from get_timeline.")

        print(f"Adding {summoner}'s data!")
        puuid = get_puuid(summoner)
        num_requests += 1
        matches = get_matches(puuid)
        num_requests += 1
        for match in matches:
            data.extend(get_game_data(match))

        # to not exceed Riot Games' API request rate limit
        # needs 16 min and 40 seconds to finish
        print(f"Finished {index+1}/{len(summoner_list)}")

    with open('lane_opponent.json', 'w') as s:
        s.write(json.dumps(data, indent = 4))

get_timeline_data()
