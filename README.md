# dataknead

An intuitive Python library for processing and converting text-based data formats like JSON and CSV.

Have you ever grudged about writing code like this?

```python
import csv
import json

with open("names.json") as f:
    data = json.loads(f.read())

data = [row["name"] for row in data if "John" in row["name"]]

with open("names.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["name"])
    [writer.writerow([row]) for row in data]
```

Now you can write it like this:

```python
from dataknead import Knead
Knead("names.json").filter(lambda r:"John" in r["name"]).write("names.csv")
```

## Basic example

Let's say you have a small CSV file with cities called `cities.csv`.

```csv
city,country,population
Amsterdam,nl,850000
Rotterdam,nl,635000
Venice,it,265000
```

And you want to load this csv file and transform it to a json file.

```python
from dataknead import Knead

cities = Knead("cities.csv").write("cities.json")
```

You'll now have a json file called `cities.json` that looks like this:

```json
[
    {
        "city" : "Amsterdam",
        "country" : "nl",
        "population" : 850000
    },
    ...
]
```

Maybe you just want the city names and write them to a CSV filed called `city-names.csv`.

```python
from dataknead import Knead

Knead("cities.csv").map("city").write("city-names.csv")
```

That will give you this list
```csv
Amsterdam
Rotterdam
Venice
```

Now you want to extract only the cities that are located in Italy, and write that back to a new csv file called `cities-italy.csv`:

```python
from dataknead import Knead

Knead("cities.csv").filter(lambda r:r["country"] == "it").write("cities-italy.csv")
````

This gives you this:

```csv
city,country,population
Venice,it,265000
```

Notice the header that you get for free because you have a list with dicts.

## Advanced example
Check out [the advanced example](https://github.com/hay/dataknead/blob/master/tests/advanced_example.py)

## Performance
Performance drawbacks should be neglible. See [this small performance test](https://github.com/hay/dataknead/blob/master/tests/compare.py).

## Caveats
* `dataknead` only supports CSV and JSON out-of-the-box.