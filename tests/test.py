import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dataknead import print_json, read_json, write_json, DictQuery

data = read_json("data/entity.json")
dq = DictQuery(data)

print_json(dq.get("response/Q2461755/image/full"))
for claim in dq.get("response/Q2461755/claims/"):
    print(claim)
    d = DictQuery(claim.get("values", None))
    print(d.get("image/full"))