from dataknead.baseloader import BaseLoader
import toml

class TomlLoader(BaseLoader):
    EXTENSIONS = ["toml"]

    @staticmethod
    def read(f):
        return toml.loads(f.read())

    @staticmethod
    def write(f, data):
        tomldata = toml.dumps(data)
        f.write(tomldata)