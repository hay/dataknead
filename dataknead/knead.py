import csv, json
from pathlib import Path
from io import StringIO

class JsonLoader:
    EXTENSION = "json"

    @staticmethod
    def read(f):
        data = f.read()
        return json.loads(data)

    @staticmethod
    def save(f, data, indent = None):
        jsondata = json.dumps(data, indent = indent)
        f.write(jsondata)

class CsvLoader:
    EXTENSION = "csv"

    @staticmethod
    def read(f):
        # Check if we have a header, and then use DictReader, otherwise
        # just read as regular csv
        sniffer = csv.Sniffer()

        try:
            has_header = sniffer.has_header(f.read(2048))
        except:
            # No delimiter, assume this is just a list of newline-separated values
            has_header = False

        f.seek(0)

        if has_header:
            reader = csv.DictReader(f)
        else:
            reader = csv.reader(f)

        return [row for row in reader]

    @staticmethod
    def save(f, data, fieldnames = None):
        if all([isinstance(i, dict) for i in data]):
            # First extract all the fieldnames from the list
            if not fieldnames:
                fieldnames = set()
                for item in data:
                    [fieldnames.add(key) for key in item.keys()]

            # Then open the CSV file and write
            writer = csv.DictWriter(f, fieldnames = fieldnames)
            writer.writeheader()
            [writer.writerow(row) for row in data]
        elif all([isinstance(i, list) for i in data]):
            # A list with lists
            writer = csv.writer(f)

            if fieldnames:
                writer.writerow(fieldnames)

            [writer.writerow(row) for row in data]
        elif isinstance(data, list):
            # Just one single column
            writer = csv.writer(f)

            if fieldnames:
                writer.writerow(fieldnames)

            [writer.writerow([row]) for row in data]
        elif isinstance(data, dict):
            # Only a header and one row
            writer = csv.writer(f)
            writer.writerow(data.keys())
            writer.writerow(data.values())
        else:
            raise TypeError("Can't write type '%s' to csv" % type(data).__name__)

class Knead:
    LOADERS = [JsonLoader, CsvLoader]

    _data = None

    def __init__(self, inp, parse_as = None, read_as = None, is_data = False):
        if parse_as:
            # Process string like file
            if not isinstance(inp, str):
                raise TypeError("Input needs to be string, not %s" % type(inp).__name__)

            loader = self._get_loader(parse_as)
            f = StringIO(inp)
            self._data = loader.read(f)
        elif isinstance(inp, str) and not is_data:
            # Either a path or a stringified data file
            if not read_as:
                read_as = Path(inp).suffix[1:]

            loader = self._get_loader(read_as)

            with open(inp) as f:
                self._data = loader.read(f)
        else:
            # We assume this is parsed data, assign it
            self._data = inp

    def __str__(self):
        return json.dumps(self.data(), indent = 4)

    def _get_loader(self, extension):
        for loader in self.LOADERS:
            if loader.EXTENSION == extension:
                return loader

        raise Error("Could not find loader for type '%s'" % extension)


    def data(self, check_instance = None):
        datatype = type(self._data)

        if check_instance and not isinstance(self._data, check_instance):
            raise Exception(
                "Data of type %s can not be processed, needs to be %s" %
                ( datatype.__name__, check_instance.__name__)
            )

        return self._data

    def filter(self, fn):
        data = [row for row in self.data(check_instance = list) if fn(row)]
        return Knead(data)

    def keys(self):
        return Knead(list(self.data().keys()))

    def map(self, iteratee):
        data = self.data(check_instance = list)

        # If 'iteratee' is a function, map over the data
        if callable(iteratee):
            data = [iteratee(row) for row in data]
        elif isinstance(iteratee, str):
            # Shortcut, like 'pluck'
            data = [row[iteratee] for row in data]
        else:
            raise TypeError("Iteratee should be of type dict or function")

        return Knead(data)

    def print(self):
        print(self)

    def query(self, path, default = None):
        data = self.data(check_instance = dict)
        keys = path.split("/")
        val = data.get(keys.pop(0), default)

        for key in keys:
            if isinstance(val, dict):
                val = val.get(key, default)
            else:
                val = default
                break

        return Knead(val, is_data = True)

    def transform(self, fn):
        """
        Runs a function over the data
        """
        self._data = fn(self.data())
        return self

    def values(self):
        return Knead(list(self.data().values()))

    def write(self, path, write_as = None, **kwargs):
        if not write_as:
            write_as = Path(path).suffix[1:]

        loader = self._get_loader(write_as)

        with open(path, "w") as f:
            loader.save(f, self.data(), **kwargs)