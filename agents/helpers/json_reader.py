import json

with open(file='../../midputs/verified_formalised_puzzles.json') as json_file:
    json_contents = json.load(fp=json_file)
for json_key, json_value in json_contents.items():
    print(json_key)
    print(json_value)
    v=0