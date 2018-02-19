# dataknead

An intuitive Python 3 library for processing and converting text-based data formats like JSON and CSV.

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

Nice huh?

## Advanced example
Check out [the advanced example](https://github.com/hay/dataknead/blob/master/tests/advanced_example.py).

## API

### *class* `dataknead.Knead(`*inp, parse_as = None, read_as = None, is_data = False*`)`
If `inp` is a string, a filepath is implied and the extension is used to get the correct loader.
```python
Knead("cities.csv")
```

To overwrite this behaviour (for a file that doesn't have the correct extension), use the `read_as` argument.
```python
Knead("cities", read_as="csv")
```

If `inp` is not a string, data is implied.
```python
Knead([1,2,3])
```

To force a string to be used as data instead of a file path, set `is_data` to `True`.
```python
Knead("http://www.github.com", is_data = True)
```

To force parsing of a string to data (e.g., from a JSON HTTP request), set `parse_as` to the correct format.
```python
Knead('{"error" : 404}', parse_as="json")
```

### `apply(`*fn*`)`
Runs all data through a function.
```python
Knead(["a", "b", "c"]).apply(lambda x:"".join(x)).print() # 'abc'
```

### `data(`*check_instance = None*`)`
Returns the parsed data.
```python
data = Knead("cities.csv").data()
```

To raise an exception for an invalid instance, pass that to `check_instance`
```python
data = Knead("cities.csv").data(check_instance = dict)
```

### `filter(`*fn*`)`
Run a function over the data and only keep the elements that return `True` in that functon.
```python
Knead("cities.csv").filter(lambda city:city["country"] == "it").write("cities-italy.csv")

# Or do this
def is_italian(city):
    return city["country"]  == "it"

Knead("cities.csv").filter(is_italian).write("cities-italy.csv")
```

### `keys()`
Returns the keys of the data.

### `map(`*fn*`)`
Run a function over all elements in the data.
```python
Knead("cities.csv").map(lambda city:city["city"].upper()).write("cities-uppercased.json")
```

To return one key in every item, you can pass a string as a shortcut:
```python
Knead("cities.csv").map("city").write("city-names.csv")
# Is the same as
Knead("cities.csv").map(lambda c:c["city"]).write("city-names.csv")
```

### `print()`
Prints the current data, formatted using `json.dumps`. These two lines are equivalent:
```python
print(Knead("cities.csv"))
Knead("cities.csv").print()
```

### `query(`*path*`)`
Queries a `dict` by using a path, separated by slashes.

```python
Knead({
    "image" : {
        "full" : {
            "src" : "http://github.com/logo.png"
        }
    }
}).query("image/full/src").print() # 'http://github.com/logo.png'
```

### `values()`
Returns values of the data.

### `write(`*path, write_as = None*`)`
Writes the data to a file. Type is implied by file extension.
```python
Knead("cities.csv").write("cities.json")
```

To force the type to something else, pass the format to `write_as`.
```python
Knead("cities.csv").map("city").write("cities.txt", write_as="csv")
```

Some of the loaders have extra options you can pass to `write`:
```Python
Knead("cities.csv").write("cities.json", indent = 4)
Knead("cities.csv").map("city").write("ciites.csv", fieldnames=["city"])
```

## Extending dataknead
You can write your own loaders to read and write other formats than the default ones. For an example take a look at the [advanced example](https://github.com/hay/dataknead/blob/master/tests/advanced_example.py).

## Performance
Performance drawbacks should be negligible. See [this small performance test](https://github.com/hay/dataknead/blob/master/tests/performance_test.py).

## Remarks
* Note that `dataknead` is Python 3-only.

## Credits
Written by [Hay Kranen](https://www.haykranen.nl).

## License
Licensed under the [MIT license](https://opensource.org/licenses/MIT).