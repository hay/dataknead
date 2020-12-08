from dataknead.baseloader import BaseLoader
import json

class JsonLoader(BaseLoader):
    EXTENSIONS = ["json"]

    @staticmethod
    def read(f):
        data = f.read()
        return json.loads(data)

    @staticmethod
    def write(f, data, **kwargs):
        jsondata = json.dumps(data, **kwargs)
        f.write(jsondata)