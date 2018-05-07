from _context import dataknead
from dataknead import Knead, BaseLoader
import xmltodict

class XmlLoader(BaseLoader):
    EXTENSION = "xml"

    @staticmethod
    def read(f):
        return xmltodict.parse(f.read())

    @staticmethod
    def write(f, data, pretty = True):
        xmldata = xmltodict.unparse(data, pretty = pretty)
        f.write(xmldata)

Knead.loaders.append(XmlLoader)

def parse(data):
    books = data["catalog"]["book"]
    data["catalog"]["book"] = [b for b in books if b["author"] == "O'Brien, Tim"]
    return data

Knead("input/books.xml").apply(parse).write("output/obrien-books.xml")