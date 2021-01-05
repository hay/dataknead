import json
import logging
from io import StringIO
from pathlib import Path
from .loaders.csv import CsvLoader
from .loaders.excel import ExcelLoader
from .loaders.json import JsonLoader
from .loaders.text import TextLoader
from .loaders.toml import TomlLoader
from .loaders.xml import XmlLoader

logger = logging.getLogger(__name__)

DEFAULT_LOADERS = [
    CsvLoader,
    ExcelLoader,
    JsonLoader,
    TextLoader,
    TomlLoader,
    XmlLoader
]

# FIXME: this can be done more elegant
def add_loader(loaders, loader):
    extensions = loader.EXTENSIONS
    logger.debug(f"Adding loader {loader} for extensions {extensions}")

    for extension in extensions:
        if extension in loaders:
            raise LoaderError(f"There is already a loader for extension '{extension}'")
        else:
            loaders[extension] = loader

    return loaders

class KneadException(Exception):
    pass

class LoaderError(Exception):
    pass

class Knead:
    _data = None
    _loaders = {}

    for loader in DEFAULT_LOADERS:
        add_loader(_loaders, loader)

    def __init__(self, inp, parse_as = None, read_as = None, is_data = False, **kwargs):
        """
        Creates a new ``Knead`` instance.

        By default it is assumed that ``inp`` is a path to a file if it's a string.
        The file extension will be used to determine the correct loader (e.g. ``.csv``
        will get the :py:class:`CsvLoader <dataknead.csv.CsvLoader>`).

        ::

            Knead("cities.csv")

        If ``inp`` is not a string it is assumed to be a data structure (e.g. a list or dict).

        ::

            Knead([1, 2, 3])

        ``parse_as`` is used when you're feeding ``Knead`` a string that is not a file
        path, like the results of a HTTP call. In that case you need to specify the
        loader yourself as a file extension (e.g. ``csv``, ``json``, etc.)

        ::

            json = "[1,2,3]"
            Knead(json, parse_as = "json")

        ``read_as`` is used when you're giving a path to a file that doesn't have a
        valid extension, and doesn't have an extension at all. The same mechanism as ``parse_as``
        is at work here: give it a file extension.

        ::

            Knead("query", read_as = "csv")

        ``is_data`` is used if you want to feed ``Knead`` a string as data, and it shouldn't
        be parsed at all

        ::

            Knead("a line of text", is_data = True)

        Any additional parameters will be passed on to the loader

        ::

            Knead("cities.csv", has_header = True)
        """

        logger.debug(f"Input: {inp}")

        if parse_as:
            # Process string like file
            if not isinstance(inp, str):
                raise TypeError(f"Input needs to be string, not {type(inp).__name__}")

            loader = self._get_loader(parse_as)
            f = StringIO(inp)
            self._data = loader.read(f, **kwargs)
        elif isinstance(inp, str) and not is_data:
            # Either a path or a stringified data file
            if not read_as:
                read_as = Path(inp).suffix[1:]

            loader = self._get_loader(read_as)

            with open(inp) as f:
                self._data = loader.read(f, **kwargs)
        else:
            # We assume this is parsed data, assign it
            self._data = inp

    def __repr__(self):
        return json.dumps(self.data(), indent = 4)

    def __str__(self):
        return json.dumps(self.data(), indent = 4)

    def _get_loader(self, extension):
        logger.debug(f"Trying to find loader for extension '{extension}'")

        if extension in self._loaders:
            logger.debug(f"Found loader for '{extension}'")
            return self._loaders[extension]
        else:
            raise KneadException(f"Could not find loader for extension '{extension}'")

    def add_loader(self, loader):
        """
        Adds a custom loader. See the `YAML loader <https://github.com/hay/dataknead/blob/master/tests/yaml_example.py>`_ for an example.
        """
        add_loader(self._loaders, loader)

    def apply(self, fn):
        """
        This applies a function to the loaded data.
        """
        self._data = fn(self.data())
        return self

    def data(self, check_instance = None):
        """
        Returns the loaded data.

        ::

            Knead("cities.csv").data() # Will return the parsed contents of cities.csv

        To check if the data is in a specific type use ``check_instance``,
        which will raise an exception if it's not correct

        ::

            Knead([1,2,3]).data(check_instance = dict) # Will raise an error, it's a list
        """
        datatype = type(self._data)

        if check_instance and not isinstance(self._data, check_instance):
            dtype = datatype.__name__
            preftype = check_instance.__name__

            raise Exception(f"Data of type {dtype} can not be processed, needs to be {preftype}")
        else:
            return self._data

    def filter(self, fn):
        """
        Applies a function on every item and removes it if it returns ``False``.
        This only works when your data is a ``list``.

        ::

            Knead([1,10,100]).filter(lambda v: v > 9).data() # Returns 10 and 100
        """
        data = [row for row in self.data(check_instance = list) if fn(row)]
        return Knead(data)

    def keys(self):
        """
        Returns the keys of the internal data
        """
        return Knead(list(self.data().keys()))

    def map(self, iteratee):
        """
        Applies a function on every item and replaces it with the return value.

        ::

            Knead([1, 4, 9]).map(lambda x:x * x).data() # [1, 16, 81]

        If you have a list with dicts, you can give a string to return the
        values of a specific key

        ::

            Knead("cities.csv").map("city").write("city-names.csv")

            # Is the same as

            Knead("cities.csv").map(lambda c:c["city"]).write("city-names.csv")

        To return multiple keys with values, you can use a tuple:

        ::

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
        """

        data = self.data(check_instance = list)

        # If 'iteratee' is a function, map over the data
        if callable(iteratee):
            data = [iteratee(row) for row in data]
        # Shortcut, like 'pluck'
        elif isinstance(iteratee, str):
            data = [row[iteratee] for row in data]
        # Another shortcut, for multiple keys
        elif isinstance(iteratee, tuple):
            data = [ { key:row[key] for key in iteratee } for row in data ]
        else:
            raise TypeError("Iteratee should be of type dict or function")

        return Knead(data)

    def values(self):
        """
        Returns the values of the data
        """
        return Knead(list(self.data().values()))

    def write(self, path, write_as = None, **kwargs):
        """
        Writes the data to a file. Type is implied by file extension.

        ::

            Knead("cities.csv").write("cities.json")

        To force the type to something else, pass the format to `write_as`.

        ::

            Knead("cities.csv").map("city").write("cities.txt", write_as="csv")

        Any additional parameters will be passed on to the loader:

        ::

            Knead("cities.csv").write("cities.json", indent = 4)
            Knead("cities.csv").map("city").write("ciites.csv", fieldnames=["city"])
        """

        logger.debug(f"write(): {path}")

        if not write_as:
            write_as = Path(path).suffix[1:]

        loader = self._get_loader(write_as)

        with open(path, "w") as f:
            loader.write(f, self.data(), **kwargs)
            logger.debug(f"Wrote the data to {path}")