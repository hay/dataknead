# dataknead
**Fluent conversion between data formats like JSON, XML and CSV**

[Read the docs](https://hay.github.io/dataknead/)

Ever sighed when you wrote code to convert CSV to JSON for the thousandth time?

```python
import csv
import json

data = []

with open("cities.csv") as f:
    reader = csv.DictReader(f)

    for row in reader:
        data.append(row)

with open("cities.json", "w") as f:
    json.dump(data, f)
```

Stop sighing and use `dataknead`. Fetch it with `pip`:

```bash
$ pip install dataknead
```

And use it like this:

```python
from dataknead import Knead
Knead("cities.csv").write("cities.json")
```

Or make it even easier on the command line:

```bash
knead cities.csv cities.json
```

`dataknead` has inbuilt loaders for CSV, Excel, JSON, TOML and XML and you can easily write your own.

Piqued your interest? [Read the docs!](https://hay.github.io/dataknead/).