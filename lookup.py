import requests

get_url = 'http://ddragon.leagueoflegends.com/cdn/12.5.1/data/en_US/champion.json'
r = requests.get(get_url)

champion_list = r.json()

# param: int uniquely identifying champion
# returns champion name when given an id
def id_to_name(id):
    id = str(id)
    for champion_name, champion_data in champion_list['data'].items():
        if (id == champion_data['key']):
            return champion_name