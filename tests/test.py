import sys, os
from time import time
from statistics import mean
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dataknead import print_json, read_json, write_json, DictQuery, write_csvdict, map_csv

data = read_json("data/entity.json")
write_json("data/entity.json", data, indent = 4)
dq = DictQuery(data)

print_json(dq.get("response/Q2092563/image/full"))

claims = []
for claim in dq.get("response/Q2092563/claims/"):
    claims.append({ k:v for k,v in claim.items() if isinstance(v, str)})

write_csvdict("data/entity.csv", claims)

def mutate(row):
    row["property_descriptions"] = row["property_descriptions"].upper()
    return row

mutate_csv("data/entity.csv", "data/entity-mutated.csv", mutate)