from webbrowser import get
from lookup import id_to_name
import requests
from dotenv import load_dotenv
import json
import os

load_dotenv()

API_URL = 'na1.api.riotgames.com/lol/'
API_KEY = os.getenv("LEAGUE_API_KEY")
REGION_URL = 'americas.api.riotgames.com/lol/'
MATCH_ID_ENDPOINT = 'match/v5/matches/by-puuid/'
MATCH_INFORMATION_ENDPOINT = 'match/v5/matches/'
SUMMONER_BY_NAME = 'summoner/v4/summoners/by-name/'

summoner_list = ['kwittens', 'NotWontonSoup', 'comfy%20gf', 'Mitaki', 'HowDoYouKite']

# returns puuid (str)
def get_puuid(summoner_name):
	get_url = 'https://' + API_URL + SUMMONER_BY_NAME
	r = requests.get(get_url + summoner_name, 
				headers={"X-Riot-Token": API_KEY})

	# response
	data = r.json()
	return data['puuid']

"""
get 10 match ids for each summoner
	params:
		puuid: uniquely identifies summoner
	returns:
		a list of ids of the last 10 ranks games played
"""
def get_matches(puuid):

	get_url = 'https://' + REGION_URL + MATCH_ID_ENDPOINT
	match_type = {'type':'ranked', 'start':'0', 'count':'10'} 
		
	r = requests.get(get_url + puuid + '/ids', 
				headers={"X-Riot-Token": API_KEY},
				params=match_type)

	data = r.json()
	return data

"""
get details of each match
	params:
		match ID: uniquely identifies a game
	returns:
		a dictionary that contains picks, bans, wins, and kda
"""

def get_match_info(match_id):
	get_url = 'https://' + REGION_URL + MATCH_INFORMATION_ENDPOINT
	
	r = requests.get(get_url + match_id,
	 headers={"X-Riot-Token": API_KEY})

	game_data = r.json()

	rows = []

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
		row["win"] = player["win"]
		rows.append(row)
		index += 1
	
	return rows

"""
# possible columns to add:

skillshots = []
for players in game_data["info"]["participants"]:
skillshots.append(players["challenges"]["skillshotsDodged"])

print(skillshots)
"""

"""
generate 500 rows of game data from:
	5 (summoners) x 10 (of their ranked games) x 10 (for the # of players per game)
	returns: writes to the "lots_of_data.json"
"""
def populate_dataset(list_of_summoners):
	data = []

	for summoner in list_of_summoners:
		print("Adding %s's data!", summoner)
		puuid = get_puuid(summoner)
		matches = get_matches(puuid)
		for match in matches:
			data.extend(get_match_info(match))

	with open('lots_of_data.json', 'w') as s:
		s.write(json.dumps(data, indent = 4))


populate_dataset(summoner_list)