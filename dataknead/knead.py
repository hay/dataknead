import csv, json
from pathlib import Path

class Knead:
    SUPPORTED_TYPES = ("csv", "json")
    _type = None
    _data = None

    def __init__(self, inp, filetype = None, is_data = False):
        if isinstance(inp, str) and not is_data:
            # We assume this is a path, load the data
            # If we have a filetype forced, use that, otherwise get it from
            # the file extension
            if filetype:
                self._type = filetype
            else:
                self._type = self._get_filetype(inp)

            self._load(inp)
        else:
            # We assume this is data, assign it
            self._type = type(inp).__name__
            self._data = inp

    def _get_filetype(self, path):
        filetype = Path(path).suffix[1:]

        if filetype not in self.SUPPORTED_TYPES:
            raise Exception("Unsupported file type: %s" % filetype)
        else:
            return filetype

    def _load(self, pathstr):
        with open(pathstr) as f:
            if self._type == "json":
                self._data = json.loads(f.read())
            elif self._type == "csv":
                reader = csv.DictReader(f)
                self._data = [row for row in reader]

    def _write_csv(self, path, fieldnames = None):
        data = self.data()

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

    def map(self, fn):
        data = [fn(row) for row in self.data(check_instance = list)]
        return Knead(data)

    def query(self, path, default = None):
        keys = path.split("/")
        val = default

        for key in keys:
            if val:
                if not key or isinstance(val, list):
                    break
                else:
                    val = val.get(key, default)
            else:
                val = self.data().get(key, default)

            if not val:
                break;

        return Knead(val, is_data = True)

    def write(self, path, filetype = None, indent = None, fieldnames = None):
        if not filetype:
            filetype = self._get_filetype(path)

        if filetype == "json":
            self._write_json(path, indent)
        elif filetype == "csv":
            self._write_csv(path, fieldnames)
