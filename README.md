# Getting Summoner Game Data from Riot API
Hello, this is just my notes on the process of querying Riot's API, written mainly for myself (because i will forget how I did it)

Hopefully it helps you too <3
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

