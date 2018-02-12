import sys, os
from time import time
from statistics import mean
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dataknead import Knead

data = Knead("data/entity.json").data()
Knead(data).write("data/entity.json", indent = 4)
print(Knead(data).query("response/Q2092563/image/full"))

claims = []
for claim in Knead(data).query("response/Q2092563/claims/"):
    claims.append({ k:v for k,v in claim.items() if isinstance(v, str)})

Knead(claims).write("data/entity.csv")

def mapfn(row):
    row["property_descriptions"] = row["property_descriptions"].upper()
    return row

def filterfn(row):
    return "located" in row["property_labels"]

Knead("data/entity.csv").map(mapfn).write("data/entity-mapped.csv")
Knead("data/entity.csv").filter(filterfn).write("data/entity-filtered.csv")