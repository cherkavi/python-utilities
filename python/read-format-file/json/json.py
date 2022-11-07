import json
from pprint import pprint

with open('example.json') as f:
    data = json.load(f)

# for unix don't do this:
# data = json.load(open('example.json'))

pprint(data)

print(data["maps"][0]["id"])
