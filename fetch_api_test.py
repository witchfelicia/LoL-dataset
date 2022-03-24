from webbrowser import get
import requests
from dotenv import load_dotenv
import json
import os
import time
from lookup import id_to_name
from helper import fill_json
from summoners import summoner_list
from summoners import check_names_are_still_valid

load_dotenv()

API_URL = 'na1.api.riotgames.com/lol/'
API_KEY = os.getenv("LEAGUE_API_KEY")
REGION_URL = 'americas.api.riotgames.com/lol/'
MATCH_ID_ENDPOINT = 'match/v5/matches/by-puuid/'
MATCH_INFORMATION_ENDPOINT = 'match/v5/matches/'
SUMMONER_BY_NAME = 'summoner/v4/summoners/by-name/'
num_requests = 0

# returns puuid (str)
def get_puuid(summoner_name):
	get_url = 'https://' + API_URL + SUMMONER_BY_NAME
	r = requests.get(get_url + summoner_name, 
				headers={"X-Riot-Token": API_KEY})

	# response
	data = r.json()
	global num_requests
	num_requests += 1

	return data['puuid']


"""
get 20 match ids for each summoner
	params:
		puuid: uniquely identifies summoner
	returns:
		a list of ids of the last 20 ranks games played
"""
def get_matches(puuid):

	get_url = 'https://' + REGION_URL + MATCH_ID_ENDPOINT
	match_type = {'type':'ranked', 'start':'0', 'count':'20'} 
		
	r = requests.get(get_url + puuid + '/ids', 
				headers={"X-Riot-Token": API_KEY},
				params=match_type)

	data = r.json()

	global num_requests
	num_requests += 1

	return data


"""
get details of each match
	params:
		match ID: uniquely identifies a game
	returns:
		a dictionary that contains picks, bans, wins, kda, and gold earned
"""

def get_match_info(match_id):
	get_url = 'https://' + REGION_URL + MATCH_INFORMATION_ENDPOINT
	
	r = requests.get(get_url + match_id,
	 headers={"X-Riot-Token": API_KEY})

	game_data = r.json()

	global num_requests
	num_requests += 1

	rows = []

	# to keep track of 10 players in 1 game
	index = 0
	# populate each row with a player's data
	for player in game_data["info"]["participants"]:
		row = {}
		# Ids
		row["matches"] = match_id
		row["picks"] = player["championName"]

		# there are 2 teams
		if index < 5:
			champion_id = game_data["info"]["teams"][0]["bans"][index]["championId"]
			row["bans"] = id_to_name(champion_id)
		else:
			# mod index so index of 2nd team starts at 0 too
			champion_id = game_data["info"]["teams"][1]["bans"][index%5]["championId"]
			row["bans"] = id_to_name(champion_id)

		row["kills"] = player["kills"]
		row["deaths"] = player["deaths"]
		row["assists"] = player["assists"]
		row["gold"] = player["goldEarned"]
		row["challenges"] = fill_json(player["challenges"])
		row["win"] = player["win"]

		# todo: add a JSON column
		rows.append(row)
		index += 1
		
	return rows

# print(get_match_info('NA1_4226412134'))

"""
generate 5000 rows of game data from:
	25 (summoners) x 20 (of their ranked games) x 10 (for the # of players per game)
	returns: writes to the "lots_and_lots_of_data.json"
"""
def populate_dataset(list_of_summoners):
	if not check_names_are_still_valid(list_of_summoners):
		quit()

	data = []
	for index, summoner in enumerate(list_of_summoners):
		print(f"Adding {summoner}'s data!")
		puuid = get_puuid(summoner)
		matches = get_matches(puuid)
		for match in matches:
			data.extend(get_match_info(match))

		# to not exceed Riot Games' API request rate limit
		# needs 16 min and 40 seconds to finish
		print(f"Finished {index+1}/{len(list_of_summoners)}")
		global num_requests
		print(f"Made {num_requests} requests.")

		# to not overwhelm the API
		if(index%3==2):
			print(f"Sleep for 2 min.")
			time.sleep(120)
		
	with open('lots_and_lots_of_data.json', 'w') as s:
		s.write(json.dumps(data, indent = 4))


# populate_dataset(summoner_list)