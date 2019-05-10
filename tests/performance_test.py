from dataknead import Knead

import json, csv
from timeit import timeit

def vanilla():
    with open("input/entity.json") as f:
        data = json.loads(f.read())

    sitelinks = data["entities"]["Q184843"]["sitelinks"].values()
    titles = [v["title"] for v in sitelinks if v["title"] != "Blade Runner"]

    with open("output/sitelinks-other-title.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["title"])
        [writer.writerow([row]) for row in titles]

def dataknead_short():
    sitelinks = Knead("input/entity.json").query("entities/Q184843/sitelinks")
    titles = sitelinks.values().map("title").filter(lambda t:t != "Blade Runner")
    titles.write("output/sitelinks-other-title.csv", fieldnames=["title"])

def dataknead_newlines():
    Knead("input/entity.json")\
        .query("entities/Q184843/sitelinks")\
        .values()\
        .map("title")\
        .filter(lambda t:t != "Blade Runner")\
        .write("output/sitelinks-other-title.csv", fieldnames=["title"])

if __name__ == "__main__":
    print("vanilla", timeit(vanilla, number = 1000))
    print("dataknead", timeit(dataknead_short, number = 1000))