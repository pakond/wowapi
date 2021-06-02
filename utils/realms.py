import requests
import json

headers = { 'x-api-key': '8khn8Ka0.Ls7YAi8CCCMM8skteHeLbgyYuOPaOvDx' }
response = requests.get('http://172.105.85.125/api/realm/', headers=headers)
response = response.json()

with open('realms-eu.txt', 'a') as outfile:
        json.dump(response, outfile)
