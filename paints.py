"""
Get the set of paints that Golden uses and save to paints.txt
Needed to map paintId to name
"""
import csv
import json

import requests


URL = 'https://paintengine.goldenpaints.com/api/paints'

response = requests.get(URL, verify=False)

paints = json.loads(response.text)['paints']
paints_data = []
for paint in paints:
    paints_data.append({
        'id': paint['paintId'],
        'name': paint['name'],
    })

with open('paints.csv', 'w') as file:
    writer = csv.DictWriter(file, ['id', 'name'])
    writer.writeheader()
    writer.writerows(paints_data)
