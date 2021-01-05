from dataknead import Knead
import csv
import json

def vanilla():
    data = []

    with open("input/cities.csv") as f:
        reader = csv.DictReader(f)

        for row in reader:
            data.append(row)

    with open("output/lead-cities-vanilla.json", "w") as f:
        json.dump(data, f)

def knead():
    Knead("input/cities.csv").write("output/lead-cities-knead.json")

if __name__ == "__main__":
    vanilla()
    knead()