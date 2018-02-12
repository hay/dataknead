import sys, os
from time import time
from statistics import mean
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dataknead import Knead

entity = Knead("input/entity.json")
entity.write("output/entity.json", indent = 4)
print(entity.query("response/Q2092563/image/full"))

def get_claimstring(claim):
    return { k:v for k,v in claim.items() if isinstance(v, str)}

def get_claimvalue(claim):
    return claim["values"][0]["value"]

claims = entity.query("response/Q2092563/claims/")
claims.write("output/claims.json")
claims.map(get_claimstring).write("output/entity.csv")
claims.map(get_claimvalue).write("output/entity-values.csv")

Knead("output/entity.csv")\
    .filter(lambda row:"located" in row["property_labels"])\
    .write("output/entity-filtered.csv")

def mapfn(row):
    row["property_descriptions"] = row["property_descriptions"].upper()
    return row

Knead("output/entity.csv").map(mapfn).write("output/entity-mapped.csv")