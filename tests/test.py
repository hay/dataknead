import sys, os
from time import time
from statistics import mean
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dataknead import Knead
from itertools import chain

# Read json file
entity = Knead("input/entity.json")

# Write back to a json file, indented
entity.write("output/entity.json", indent = 4)

# Print the description using query()
print(entity.query("entities/Q184843/descriptions/en/value"))

entity\
    .query("entities/Q184843/sitelinks")\
    .transform(lambda d:list(d.values()))\
    .map(lambda d:[d["site"], d["title"]])\
    .write("output/sitelinks.csv")

# Get claims
claims = entity.query("entities/Q184843/claims")

# Write claims, indented with 4 spaces
claims.write("output/claims.json", indent = 4)

def propvalue(claim):
    claim = Knead(claim)

    return {
        "id" : claim.query("mainsnak/datavalue/value/id").data(),
        "property" : claim.query("mainsnak/property").data()
    }

def transform(claims):
    values = chain.from_iterable(claims.values())
    return [propvalue(c) for c in list(values)]

# Flatten claims and write to csv
claims.transform(transform).write("output/claims.csv")

"""
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
"""