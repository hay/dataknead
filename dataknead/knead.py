import json
import logging
from io import StringIO
from pathlib import Path
from .loaders.csv import CsvLoader
from .loaders.excel import ExcelLoader
from .loaders.json import JsonLoader
from .loaders.text import TextLoader
from .loaders.xml import XmlLoader

logger = logging.getLogger(__name__)

DEFAULT_LOADERS = [
    CsvLoader,
    ExcelLoader,
    JsonLoader,
    TextLoader,
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
        add_loader(self._loaders, loader)

    def apply(self, fn):
        self._data = fn(self.data())
        return self


    def data(self, check_instance = None):
        datatype = type(self._data)

        if check_instance and not isinstance(self._data, check_instance):
            dtype = datatype.__name__
            preftype = check_instance.__name__

            raise Exception(f"Data of type {dtype} can not be processed, needs to be {preftype}")
        else:
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
        # Shortcut, like 'pluck'
        elif isinstance(iteratee, str):
            data = [row[iteratee] for row in data]
        # Another shortcut, for mulitple keys
        elif isinstance(iteratee, tuple):
            data = [ { key:row[key] for key in iteratee } for row in data ]
        else:
            raise TypeError("Iteratee should be of type dict or function")

        return Knead(data)

    def values(self):
        return Knead(list(self.data().values()))

    def write(self, path, write_as = None, **kwargs):
        logger.debug(f"write(): {path}")

        if not write_as:
            write_as = Path(path).suffix[1:]

        loader = self._get_loader(write_as)

        with open(path, "w") as f:
            loader.write(f, self.data(), **kwargs)
            logger.debug(f"Wrote the data to {path}")