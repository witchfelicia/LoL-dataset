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
GAME_TIMELINE_ENDPOINT = 'match/v5/matches/{matchId}/timeline'
SUMMONER_ENDPOINT = 'summoner/v4/summoners/by-puuid/{encryptedPUUID}'
SUMMONER_BY_NAME = 'summoner/v4/summoners/by-name/'

peter = 'meth%20damon'

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
		a list of 20 ids of the last 20 games played
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
	
	stats = {} # json as a list of json
	bans = []
	for team in game_data["info"]["teams"]: 
		for ban in team["bans"]:
			bans.append(ban["championId"])
	print(bans)

	winners = []
	#first_team_won = game_data["info"]["teams"][0]

	for players in game_data["info"]["participants"]:
		winners.append(players["win"])
	print(winners)

	"""print(game_data["info"]["participants"][0]["assists"])
	print(game_data["info"]["participants"][0]["championId"])"""

	picks = []
	for players in game_data["info"]["participants"]:
		picks.append(players["championId"])
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



	stats =
	# what are we returning?
	for i in range(0,10):




	"""
	for team in game_data["info"]["teams"]:
		print(team)

	"""

	"""
	info = str(r.json()["info"])
	# print(game_data["info"]["participants"][0]["baronKills"]) # make some of stuff columns
	f = open("peter_data", "w+")
	f.write(info)
	f.close()
	"""

get_match_info('NA1_4226412134')

# test
# print(get_puuid(peter))
# '-oXMqiG7Iz4jfAcbhR09AeP44KvBCtL9cEejVh-adG5LlQ0PEQFLJSwJV0Xk7upjLNKm5l3fygLhWA'

#test
# print(get_matches('-oXMqiG7Iz4jfAcbhR09AeP44KvBCtL9cEejVh-adG5LlQ0PEQFLJSwJV0Xk7upjLNKm5l3fygLhWA'))
# ['NA1_4226412134', 'NA1_4226345907', 'NA1_4218138569', 'NA1_4218105594', 'NA1_4211723295', 'NA1_4211687221', 'NA1_4211653877', 'NA1_4209587154', 'NA1_4209487127', 'NA1_4209475699', 'NA1_4208089388', 'NA1_4208092029', 'NA1_4207995324', 'NA1_4200313716', 'NA1_4200273950', 'NA1_4200232990', 'NA1_4200174394', 'NA1_4199167723', 'NA1_4199144987', 'NA1_4199171572']
