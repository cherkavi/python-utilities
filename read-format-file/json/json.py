import json
from pprint import pprint

data = json.load(open('example.json'))

pprint(data)

print(data["maps"][0]["id"])