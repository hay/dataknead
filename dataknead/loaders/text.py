from dataknead.baseloader import BaseLoader

class TextLoader(BaseLoader):
    EXTENSIONS = ["txt"]

    @staticmethod
    def read(f):
        return f.read().splitlines()

    @staticmethod
    def write(f, data):
        [f.write(line + "\n") for line in data]