import requests
import json

headers = { 'x-api-key': 'Qjgiccvq.mU1HJOjUEjCKGOofTFBUv4gmZftIuSuK' }
response = requests.get('https://api-eu.murlocmate.com/realm/', headers=headers)
response = response.json()

with open('realms.txt', 'a') as outfile:
        json.dump(response, outfile)
