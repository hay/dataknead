import json
from .baseloader import BaseLoader

class JsonLoader(BaseLoader):
    EXTENSION = "json"

    @staticmethod
    def read(f):
        data = f.read()
        return json.loads(data)

    @staticmethod
    def write(f, data, indent = None):
        jsondata = json.dumps(data, indent = indent)
        f.write(jsondata)