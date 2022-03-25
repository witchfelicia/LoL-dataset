from tabnanny import check
import requests
import os
import json

from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("LEAGUE_API_KEY")
API_URL = 'na1.api.riotgames.com/lol/'
SUMMONER_BY_NAME = 'summoner/v4/summoners/by-name/'

# 25 summoners, half are plat, half are diamond
summoner_list = ['Aixopluc','kwittens', 'NotWontonSoup', 'comfy%20gf', 'Mitaki', 'HowDoYouKite',
				'yk%20who%20it%20is', 'douyu%207180846', 'YesHahaVeryGood', 'Swizurk', 'dg%20kat',
				'%C3%A1scetic', 'dont%20forget', 'SPORTINWIL', 'CreepSteel',
				'Danz0509', 'KEGGYTH%C3%89KEG', 'miny0ung', 'no%20service', 'Crow%20Kingg',
				'lf%20duo%20yes', 'Talaine', 'My%20Throne', 'Kindredgarten', 'GB%20Kun%C3%A2i']

"""
players often change their names so we want to check and update them periodically """
def check_names_are_still_valid(s_list):
    get_url = 'https://' + API_URL + SUMMONER_BY_NAME

    for summoner_name in s_list:
        r = requests.get(get_url + summoner_name, 
                    headers={"X-Riot-Token": API_KEY})
        # response
        data = r.json()

        if(data.get("status")):
            print(f"Summoner {summoner_name} changed their name!")
            print(data)
            print("Go update!")
            return False
    
    print("All names are still valid! (:")
    return True

# TODO: take summoner names and convert them all to puuid and store them as a list in another file
# 
def as_puuid():
    listtt = []
    for summoner_name in summoner_list:
        get_url = 'https://' + API_URL + SUMMONER_BY_NAME

        r = requests.get(get_url + summoner_name, 
                    headers={"X-Riot-Token": API_KEY})
        # response
        data = r.json()
        listtt.append(data['puuid'])

    print(listtt)
 
as_puuid()
