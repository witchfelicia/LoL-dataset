from webbrowser import get
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

# fetches 1 game from 1 summoner as a test
peter = 'meth%20damon'
wonton = 'NotWontonSoup'

# returns puuid (str)
def get_puuid(summoner_name):
	get_url = 'https://' + API_URL + SUMMONER_BY_NAME
	r = requests.get(get_url + summoner_name, 
				headers={"X-Riot-Token": API_KEY})

	# response
	data = r.json()
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
	return data

# get 20 games from 5 summoners and see what we get?
# find: champ pick

"""
get details of each match
	params:
		match ID: uniquely identifies a game
	returns:
		pick, ban, and win rates of champs
"""
def get_match_info(match_id):
	get_url = 'https://' + REGION_URL + MATCH_INFORMATION_ENDPOINT
	
	r = requests.get(get_url + match_id,
	 headers={"X-Riot-Token": API_KEY})

	game_data = r.json()

	# print(game_data["info"]["teams"][0]["bans"][0]["championId"])
	
	# an example banned champion: 
	# print(game_data["info"]["teams"][0]["bans"][0]["championId"])
	
	bans = []
	for team in game_data["info"]["teams"]: 
		for ban in team["bans"]:
			bans.append(ban["championId"])
	print(bans)

	winners = []

	for players in game_data["info"]["participants"]:
		winners.append(players["win"])
	print(winners)

	"""print(game_data["info"]["participants"][0]["assists"])
	print(game_data["info"]["participants"][0]["championId"])"""

	picks = []
	for players in game_data["info"]["participants"]:
		picks.append(players["championName"])
	print(picks)

	kills = []
	for players in game_data["info"]["participants"]:
		kills.append(players["kills"])
	print(kills)

	deaths = []
	for players in game_data["info"]["participants"]:
		deaths.append(players["deaths"])
	print(deaths)

	assists = []
	for players in game_data["info"]["participants"]:
		assists.append(players["assists"])
	print(assists)

	
	stats = {}
	# what are we returning?
	stats = {
		"picks": picks,
		"bans": bans,
		"wins": winners,
		"kills": kills,
		"deaths": deaths,
		"assists": assists
	}

	
	"""
	with open('wontons_data.json', 'w') as s:
		s.write(json.dumps(stats, indent = 4))
	"""
	"""
	skillshots = []
	for players in game_data["info"]["participants"]:
		skillshots.append(players["challenges"]["skillshotsDodged"])

	print(skillshots)
	"""

# peter's match info
# get_match_info('NA1_4226412134')
# wonton
# get_match_info('NA1_4236804806')

def test(match_id):
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
		print("picks: ", player["championName"])

		# there are 2 teams
		if index < 5:
			row["bans"] = game_data["info"]["teams"][0]["bans"][index]["championId"]
		else:
			# mod index so index of 2nd team starts at 0 too
			row["bans"] = game_data["info"]["teams"][1]["bans"][index%5]["championId"]

		row["kills"] = player["kills"]
		row["deaths"] = player["deaths"]
		row["assists"] = player["assists"]
		row["win"] = player["win"]
		rows.append(row)
		index += 1
	
	"""with open('peter_data_2.json', 'w') as s:
		s.write(json.dumps(rows, indent = 4))
	print(rows)"""
	return rows

data = []
data.extend(test('NA1_4226412134'))
data.extend(test('NA1_4226345907'))

with open('lots_of_data.json', 'w') as s:
		s.write(json.dumps(data, indent = 4))
# test
# print(get_puuid(peter))
# '-oXMqiG7Iz4jfAcbhR09AeP44KvBCtL9cEejVh-adG5LlQ0PEQFLJSwJV0Xk7upjLNKm5l3fygLhWA'

#test
# print(get_matches('-oXMqiG7Iz4jfAcbhR09AeP44KvBCtL9cEejVh-adG5LlQ0PEQFLJSwJV0Xk7upjLNKm5l3fygLhWA'))
# ['NA1_4226412134', 'NA1_4226345907', 'NA1_4218138569', 'NA1_4218105594', 'NA1_4211723295', 'NA1_4211687221', 'NA1_4211653877', 'NA1_4209587154', 'NA1_4209487127', 'NA1_4209475699', 'NA1_4208089388', 'NA1_4208092029', 'NA1_4207995324', 'NA1_4200313716', 'NA1_4200273950', 'NA1_4200232990', 'NA1_4200174394', 'NA1_4199167723', 'NA1_4199144987', 'NA1_4199171572']
