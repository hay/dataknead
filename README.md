# dataknead

An intuitive Python library for processing and converting text-based data formats like JSON and CSV.

## Example
Let's say you have a small CSV file with cities called `cities.csv`.

```csv
city,country,population
Amsterdam,nl,850000
Rotterdam,nl,635000
Venice,it,265000
```

And you want to load this csv file and transform it to a json file.

```pytyhon
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

Now you want to extract only the cities that are located in Italy, and write that back to a new csv file called `cities-italy.csv`:

```python
from dataknead import Knead

Knead("cities.csv").filter(lambda r:r["country"] == "it").write("cities-italy.csv")
````

This gives you this

```csv
city,country,population
Venice,it,265000
```

## Caveats
* `dataknead` only supports CSV and JSON
* The only format writable to CSV and JSON is a `dict` or a `list` with `dict` structures. If you only have a list, use `map` to add a key to it, like this:

```python
Knead([1,2,3]).map(lambda i:{ "number" : i }).write("numbers.csv")
```