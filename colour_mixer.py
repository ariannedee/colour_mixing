import csv
import functools
import json
import math
import sys

import requests

# Todo: Use one of the following below depending on if you want to search by Hex or RGB
target_colour = "123456"
# target_colour = {'r': 152, 'g': 204, 'b': 51}

if isinstance(target_colour, str):
    target_colour_hex = {
        'r': target_colour[0:2],
        'g': target_colour[2:4],
        'b': target_colour[4:6]
    }
    target_colour_dict = {key: int(value, 16) for key, value in target_colour_hex.items()}
elif isinstance(target_colour, dict):
    target_colour_dict = target_colour
else:
    sys.exit('Target colour format not supported')


URL = 'https://paintengine.goldenpaints.com/api/colormatch_tag'

data = {
    'cie76MatchingBound': 1,
    'paletteTag': "Modern_Theory",
    'targetColor': target_colour_dict
}
response = requests.post(URL, json=json.dumps(data), verify=False)

if response.status_code != 200:
    sys.exit(f'Request failed with code: {response.status_code}')

data = json.loads(response.text)
solution = data['solution']['parts']
solution_amounts = [int(paint['quantity'] * 100) for paint in solution]
gcd = functools.reduce(math.gcd, solution_amounts)

solution_paints = {}
for paint in solution:
    solution_paints[paint['paintId']] = int(int(paint['quantity'] * 100) / gcd)

paints = []
with open('paints.csv', 'r') as file:
    reader = csv.DictReader(file)
    all_paints = {paint['id']: paint['name'] for paint in reader}

for paint_id, amount in solution_paints.items():
    paints.append({
        'name': all_paints[paint_id],
        'amount': amount
    })

print(paints)
