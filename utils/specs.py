import requests
import json

headers = { 'x-api-key': 'MOuCL3aV.w0n7kKzjgQnwyWRn8uvmlKgNijF7Gwbn' }
response = requests.get('http://212.71.245.14/api/spec/', headers=headers)
response = response.json()

with open('specs.txt', 'a') as outfile:
        json.dump(response, outfile)

# for item in response:
#     response = requests.get('http://212.71.245.14/api/spec/' + str(item['id']), headers=headers)
#     response = response.json()

#     with open('specs.txt', 'a') as outfile:
#         json.dump(response, outfile)