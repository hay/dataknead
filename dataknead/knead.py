import csv, json
from pathlib import Path
from io import StringIO

class Knead:
    SUPPORTED_TYPES = ("csv", "json")
    _filetype = None
    _data = None

    def __init__(self, inp, filetype = None, is_data = False, process_as = False):
        if process_as:
            # Process string like file
            if not isinstance(inp, str):
                raise TypeError("Input needs to be string, not %s" % type(inp).__name__)

            self._filetype = process_as
            f = StringIO(inp)
            self._load(f)
        elif isinstance(inp, str) and not is_data:
            # We assume this is a path, load the data
            # If we have a filetype forced, use that, otherwise get it from
            # the file extension
            if filetype:
                self._filetype = filetype
            else:
                self._filetype = self._get_filetype(inp)

            with open(inp) as f:
                self._load(f)
        else:
            # We assume this is data, assign it
            self._data = inp

    def __str__(self):
        return json.dumps(self.data(), indent = 4)

    def _get_filetype(self, path):
        filetype = Path(path).suffix[1:]

        if filetype not in self.SUPPORTED_TYPES:
            raise Exception("Unsupported file type: %s" % filetype)
        else:
            return filetype

    def _load(self, f):
        if self._filetype == "json":
            self._data = json.loads(f.read())
        elif self._filetype == "csv":
            self._load_csv(f)

        f.close()

    def _load_csv(self, f):
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

        self._data = [row for row in reader]

    def _write_csv(self, path, fieldnames = None):
        data = self.data()

        if all([isinstance(i, dict) for i in data]):
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
        elif all([isinstance(i, list) for i in data]):
            # A list with lists
            with open(path, "w") as f:
                writer = csv.writer(f)

                if fieldnames:
                    writer.writerow(fieldnames)

                [writer.writerow(row) for row in data]
        elif isinstance(data, list):
            # Just one single column
            with open(path, "w") as f:
                writer = csv.writer(f)

                if fieldnames:
                    writer.writerow(fieldnames)

                [writer.writerow([row]) for row in data]
        elif isinstance(data, dict):
            # Only a header and one row
            with open(path, "w") as f:
                writer = csv.writer(f)
                writer.writerow(data.keys())
                writer.writerow(data.values())
        else:
            raise TypeError("Can't write type '%s' to csv" % type(data).__name__)

    def _write_json(self, path, indent = None):
        with open(path, "w") as f:
            jsondata = json.dumps(self.data(), indent = indent)
            f.write(jsondata)

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

    def write(self, path, filetype = None, indent = None, fieldnames = None):
        if not filetype:
            filetype = self._get_filetype(path)

        if filetype == "json":
            self._write_json(path, indent = indent)
        elif filetype == "csv":
            self._write_csv(path, fieldnames = fieldnames)
