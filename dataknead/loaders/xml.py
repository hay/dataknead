from dataknead.baseloader import BaseLoader
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