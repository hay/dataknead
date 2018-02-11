import csv, json

# Maybe rewrite this to a chained thing, bit like jQuery?
# knead("data.json").print(indent = 4)
# data = knead("data.json").read()
# knead(data).write("data.json")
# knead(data).write("data.csv")
# knead(data).query("/something")
# knead("data.csv").map(mapfn).write("data-out.csv")

def print_json(data, indent = 4):
    print(json.dumps(data, indent = indent))

def read_json(path):
    with open(path) as f:
        return json.loads(f.read())

def write_json(path, data, indent = None):
    with open(path, "w") as f:
        f.write(json.dumps(data, indent = indent))

def map_csv(inpath, outpath, mapfn):
    """
    map() for a CSV file

    :param inpath: Path to the input CSV file
    :param outpath: Path to the output CSV file
    :param mapfn: Function that does a mutation and returns the row
    """
    reader = csv.DictReader(open(inpath))
    writer = csv.DictWriter(open(outpath, "w"), reader.fieldnames)
    writer.writeheader()
    [writer.writerow(mapfn(row)) for row in reader]

def write_csvdict(path, data, fieldnames = None):
    """
    Writes a JSON array with objects to a CSV file.

    :param path: Path to the CSV file you want to write
    :param data: List with dicts that you want to write
    :param fieldnames: Tuple of fieldnames if you don't want to use the automatic detectino
    """

    # First extract all the fieldnames from the list
    if not fieldnames:
        fieldnames = set()
        for item in data:
            [fieldnames.add(key) for key in item.keys()]

    # Then open the CSV file and write
    with open(path, "w") as f:
        writer = csv.DictWriter(f, fieldnames = fieldnames)
        writer.writeheader()
        [writer.writerow(row) for row in data]

class DictQuery(dict):
    def get(self, path, default = None):
        keys = path.split("/")
        val = default

        for key in keys:
            if val:
                if not key:
                    break
                elif isinstance(val, list):
                    return default
                else:
                    val = val.get(key, default)
            else:
                val = dict.get(self, key, default)

            if not val:
                break;

        return val