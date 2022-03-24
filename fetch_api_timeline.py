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

# Check to ensure we didn't exceed the API request limit for every 2 min
def reached_request_limit():
    global num_requests
    if num_requests >= 96:
        print(f"Made {num_requests} requests. Sleep for 2 min.")
        num_requests = 0
        
        return True
    else:
        return False

def make_and_verify_request(get_url):
    r = requests.get(get_url, 
		headers={"X-Riot-Token": API_KEY})
    
    global num_requests
    num_requests += 1

    # Verify
    if r.status_code == requests.codes.ok:
        return r.json()

    else:
        print(f"Something happened with the request {get_url}")
        print(f"Error code: {r.status_code}")
        print(f"Response body: {r.json}")
        return ""

# get champion name + position played columns
def get_position(match_id):
    if reached_request_limit():
        time.sleep(120)
        print("Resuming from get_position")
    url = 'https://' + REGION_URL + MATCH_INFORMATION_ENDPOINT + match_id
    
    game_data = make_and_verify_request(url)

    # fill cols with champion name + position
    champion = []
    position_played = []
    for player in game_data["info"]["participants"]:
        champion.append(player['championName'])
        position_played.append(player['individualPosition'])
    
    return champion, position_played

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

def fetch_game_data(match_id):
    # to not overwhelm the API
    if reached_request_limit():
        time.sleep(120)
        print("resume from fetch_game_data")

    get_url = 'https://' + REGION_URL + MATCH_INFORMATION_ENDPOINT + match_id + '/timeline'
    data = make_and_verify_request(get_url) # use requests.get()
    
    # if request failed
    if data == "":
        exit()

    champion, position_played = get_position(match_id)
    
    ten_min_gold = get_ten_min_gold(data['info']['frames'])
    
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

# fetch_game_data('NA1_4253447957')
# print (get_position('NA1_4253447957'))

def populate_timeline_data():
    data = []
    for index, summoner in enumerate(summoner_list):
        global num_requests

        if reached_request_limit():
            time.sleep(120)
            print("Resume from get_timeline.")

        print(f"Adding {summoner}'s data!")

        if reached_request_limit():
            time.sleep(120)
            print("Resuming from get_timeline.")
        puuid = get_puuid(summoner)
        num_requests += 1
        matches = get_matches(puuid)
        num_requests += 1
        for match in matches:
            data.extend(fetch_game_data(match))

        # to not exceed Riot Games' API request rate limit
        # needs 16 min and 40 seconds to finish
        print(f"Finished {index+1}/{len(summoner_list)}")

    with open('lane_opponent.json', 'w') as s:
        s.write(json.dumps(data, indent = 4))

populate_timeline_data()
