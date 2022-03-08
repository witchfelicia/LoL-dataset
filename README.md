# Getting Summoner Game Data from Riot API
Hello, this is just my notes on the process of querying Riot's API, written mainly for myself (because i will forget how I did it)

Hopefully it helps you too <3

## Endpoints
That I used for this project are:
1. PLATFORM_API_URL = 'na1.api.riotgames.com/lol/'
    - the beginning of the API endpoint used to query summoner name
2. REGION_API_URL = 'americas.api.riotgames.com/lol/'
    - the beginning of the API endpoint for querying match data
3. MATCH_ID_ENDPOINT = 'match/v5/matches/by-puuid/{puuid}/ids'
    - continuation of endpoint that returns a list of match IDs from summoner name
4. MATCH_INFORMATION_ENDPOINT = 'match/v5/matches/{matchId}'
5. SUMMONER_BY_NAME = 'summoner/v4/summoners/by-name/'

After you get your personal [API key](https://developer.riotgames.com/), you can generate HTTP request strings from the links I included above to try out [Riot's Developer API](https://developer.riotgames.com/apis).
Trust me, it's fun!

## Requests
I use the Python library [Requests](https://docs.python-requests.org/en/latest/user/quickstart/#make-a-request) to simplify the process of generating a HTTP request 

### Authentication
Get your personal [API key](https://developer.riotgames.com/) from Riot, which is available for 24 hrs and you can make 20 requests every 1 second.

#### Private key
To keep your key private, store it in your `.env` file to a variable. This is what I have
.env
```
LEAGUE_API_KEY = 'blablabla'
```

Make a `.gitignore` for your `.env`

#### Load key
To load your private key in main, I used the package [dotenv](https://github.com/theskumar/python-dotenv).

fetch_api.py
```python
from dotenv import load_dotenv
import os

load_dotenv()

# check if u got it (:
print(os.getenv("LEAGUE_API_KEY"))
```

#### Authentication via Header
To make your GET request, we'll save your API in the header (as this is the cleaner method)

After building your URL for whichever endpoint you're requesting data from, do

fetch_api.py
```python
API_KEY = os.getenv("LEAGUE_API_KEY")

get_url = 'https://na1.api.riotgames.com/' + '...'
r = requests.get(get_url, headers={"X-Riot-Token": API_KEY})
```

## Response
Using my friend's League summoner name to make a request to the [summoner data endpoint](https://developer.riotgames.com/apis#summoner-v4/GET_getBySummonerName), this is the response:
```json
{'id': 'I9ZAB52JjapKUMzmld3N8yOov5DSBLHewLkVrHWamYEOgr4', 'accountId': 'wiTZRja9FYdgOI2ZZ_CkmxLKQg2CdgjCegCtXb99sf93Pg', 'puuid': '-oXMqiG7Iz4jfAcbhR09AeP44KvBCtL9cEejVh-adG5LlQ0PEQFLJSwJV0Xk7upjLNKm5l3fygLhWA', 'name': 'Meth Damon', 'profileIconId': 3810, 'revisionDate': 1645866430000, 'summonerLevel': 241}
```

We're interested in getting the `puuid`, and since a JSON object is similar to a dictionary, we can use
```python
data = r.json()
print(data['puuid'])
```

full code to do this (excluding the http req)
```python
peter = 'meth%20damon'

# returns puuid (str)
def get_puuid(summoner_name):
	get_url = 'https://' + API_URL + SUMMONER_BY_NAME
	r = requests.get(get_url + summoner_name, headers={"X-Riot-Token": API_KEY})

	# response
	data = r.json()
	return data['puuid']

print(get_puuid(peter))
```
## Methods
### get_puuid 
	param: string of a summoner name
	returns a unique puuid that identifies a summoner (string)
Notes:
- Summoner names must be parsed for special characters beforehand. For example, 'Meth Damon'-> 'meth%20damon', 'áscetic' -> %C3%A1scetic
- I test and obtain the unique summoner name strings using the [Riot API](https://developer.riotgames.com/apis#summoner-v4/GET_getBySummonerName) and copying the names since I'm not familiar with unique character encoding

### id_to_name()
Converts champion ID to the name 
	param: int uniquely identifying champion
	returns champion name when given an id

### get_matches()
	params:
		puuid: uniquely identifies summoner
	returns:
		a list of ids of the last 20 ranked games played

### get_match_info()
	params:
		match ID: uniquely identifies a game
	returns:
		a dictionary that contains picks, bans, wins, and kda
This dictionary will represent a row later in our dataset (:

### populate_dataset()

generates 5000 rows of game data from:
25 (summoners) x 20 (of their ranked games) x 10 (for the # of players per game)

returns: writes to the "lots_and_lots_of_data.json"

Note: 
- We will use the `matches` and `picks` columns to uniquely identify a row of data to account for duplicates.
- We convert the "lots_and_lots_of_data.json" file in Colab using Pandas' [to_csv()](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html) 