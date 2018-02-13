from context import dataknead
from dataknead import Knead
import csv
import json

def vanilla():
    with open("input/names.json") as f:
        data = json.loads(f.read())

    data = [row["name"] for row in data if "John" in row["name"]]

    with open("output/names-vanilla.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["name"])
        [writer.writerow([row]) for row in data]

def knead():
    Knead("input/names.json").filter(lambda r:"John" in r["name"]).write("output/names-knead.csv")

if __name__ == "__main__":
    vanilla()
    knead()