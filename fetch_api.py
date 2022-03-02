import requests
from dotenv import load_dotenv

API_URL = 'na1.api.riotgames.com/lol/'
MATCH_ID_ENDPOINT = 'match/v5/matches/by-puuid/{puuid}/ids'
MATCH_INFORMATION_ENDPOINT = 'match/v5/matches/{matchId}'
GAME_TIMELINE_ENDPOINT = 'match/v5/matches/{matchId}/timeline'
SUMMONER_ENDPOINT = 'summoner/v4/summoners/by-puuid/{encryptedPUUID}'

# put LEAGUE_API_KEY somewhere?
load_dotenv()

get_url = 
r = requests.get()

# response?
r.text

# get 20 games from 5 summoners and see what we get?
# find: champ pick