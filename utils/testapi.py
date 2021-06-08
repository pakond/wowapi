import requests
import json
from requests.auth import HTTPBasicAuth
import pprint

my_headers = ''

def get_token():
    query = { 'grant_type': 'client_credentials' }
    response = requests.post(
        "https://eu.battle.net/oauth/token",
        params=query,
        auth=HTTPBasicAuth('94f8968fb33c4ba7a2b70c52f11ef232','32hTr9BKNlGJ7Vi8VWnV5nUhH6b2gVCx')
    )
    token = response.json()['access_token']
    global my_headers
    my_headers = {'Authorization': 'Bearer ' + token}

def make_request(url, query):
    if my_headers == '':
        get_token()
    
    response = requests.get(url, headers=my_headers, params=query)

    return response

query = { 'region': 'eu', 'namespace': 'profile-' + 'eu', 'locale': 'en_US' }
responseachievements = make_request('https://' + 'eu' + '.api.blizzard.com/profile/wow/character/' + 'dun-modr' + '/' + 'sora' + '/achievements', query)

if responseachievements.status_code == 200:
        responseachievements = responseachievements.json()
        with open('test.txt', 'a') as outfile:
            json.dump(responseachievements, outfile)


