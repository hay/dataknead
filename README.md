# dataknead

A fluid Python library and command line utility for processing and converting between common data formats like JSON and CSV.

Have you ever sighed when writing code like this?

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

Or what about simply converting `json` to `csv`? With `dataknead` you get the `knead` command line utility which makes things easy:

```bash
knead names.json names.csv
```

`dataknead` has inbuilt loaders for CSV, Excel, JSON and XML and you can easily write your own.

## Installation
Install `dataknead` from [PyPi](https://pypi.python.org/pypi/dataknead)

```shell
pip install dataknead
```

Then import

```python
from dataknead import Knead
```

## Basic example and tutorial

Let's say you have a small CSV file with cities and their population called `cities.csv`.

```csv
city,country,population
Amsterdam,nl,850000
Rotterdam,nl,635000
Venice,it,265000
```

And you want to load this csv file and transform it to a json file.

```python
from dataknead import Knead

Knead("cities.csv").write("cities.json")
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
Check out [the advanced example](https://github.com/hay/dataknead/blob/master/tests/advanced_example.py). This also shows you how to do more complex data manipulation using external libraries like [jq](https://stedolan.github.io/jq/).

## Philosophy
`dataknead` is intended for easy conversion between common data formats and basic manipulation. It's not a replacement for more complex libraries like `pandas` or `numpy`, but instead can be a useful addition to those libraries.

The API is as minimal as possible and [fluent](https://en.wikipedia.org/wiki/Fluent_interface).

I try to use as many existing and well-tested libraries as possible. For example, the XML loader uses the excellent [`xmltodict`](https://github.com/martinblech/xmltodict) module.

## Command line utility (`knead`)

`dataknead` includes the `knead` command line utility you can use for simple conversion of data formats.

    knead cities.csv cities.json

Will transform a filed called `cities.csv` to a file called `cities.json` and is equivalent to this piece of Python code

    Knead("cities.csv").write("cities.json")

`knead` can also be used as a quick way of viewing the contents of a file, just give it an input file

    knead cities.csv

This is equivalant to

    print(Knead("cities.csv").data())

You can also specify the input and output formats, when those are not available in the file extension, or if you want to overwrite them. This is useful in combination with the `--stdin` option, which allows you to take data from stdin and directly transform output from a HTTP API to something else.

For example, this API request gives you back a JSON summary of the article for Amsterdam on the English Wikipedia.

    curl https://en.wikipedia.org/api/rest_v1/page/summary/Amsterdam

Piping that into dataknead using --stdin and -if json gives you a nicely formatted file

    curl https://en.wikipedia.org/api/rest_v1/page/summary/Amsterdam | knead --stdin -if json

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

Some loaders might come with extra arguments. E.g. the `csv` loader has an option to force using a header, if it isn't detected automatically

```python
Knead("cities.csv", has_header = True)
```

### `add_loader(*loader*)`
Add a new loader to the `Knead` instance. Read the section on [extending dataknead](#extending-dataknead) on how to write your own loader.

```python
Knead.add_loader(YamlLoader)
```

### `apply(`*fn*`)`
Runs all data through a function.
```python
print(Knead(["a", "b", "c"]).apply(lambda x:"".join(x))) # 'abc'
```

### `data(`*check_instance = None*`)`
Returns the parsed data.
```python
data = Knead("cities.csv").data()
```

To raise an exception for an invalid instance, pass that to `check_instance`.
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

### `map(`*fn* | *str* | *tuple*`)`
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

To return multiple keys with values, you can use a tuple:
```python
Knead("cities.csv").map(("city", "country")).write("city-country-names.csv")

# Is the same as

Knead("cities.csv").map(lambda c:{ "city" : c["city"], "country" : c["country"] }).write("city-country-names.csv")

# Or

def mapcity(city):
    return {
        "city" : city["city"],
        "country" : city["country"]
    }

Knead("cities.csv").map(mapcity).write("city-country-names.csv")

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
You can write your own loaders to read and write other formats than the default ones. For an example take a look at the [YAML example](https://github.com/hay/dataknead/blob/master/tests/yaml_example.py).

## Remarks
* Note that `dataknead` is Python 3-only.

## Credits
Written by [Hay Kranen](https://www.haykranen.nl).

## License
Licensed under the [MIT license](https://opensource.org/licenses/MIT).

## Development information
If you want to work on `dataknead` follow these steps

Clone the repo

    git clone https://github.com/hay/dataknead

And use [Poetry](https://python-poetry.org/) to install dependencies

    poetry install

Or alternatively

    pip install pandas pyyaml xlrd xlwt xmltodict

You might need to install a couple of dependencies beforehand

    pip install wheel

And (depending on your OS) some other deps too. For Debian / Ubuntu try

    apt install build-essential autoconf libtool automake

## Release history

### 0.3
* Breaking change: removed the `query` method: the focus of `dataknead` is on conversion. Using `apply` you can easily use a tool like `jq` to query.

### 0.2
* Adding tuple shortcut to `map` (#2)
* Adding support for `txt` files ((#4)
* Adding support for loader constructor argument passing, and adding a `has_header` option to `CsvLoader` (#5)

### 0.1
Initial release