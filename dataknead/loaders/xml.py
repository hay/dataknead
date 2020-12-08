from dataknead.baseloader import BaseLoader
import xmltodict

class XmlLoader(BaseLoader):
    EXTENSIONS = ["xml"]

    @staticmethod
    def read(f):
        return xmltodict.parse(f.read())

    @staticmethod
    def write(f, data, **kwargs):
        xmldata = xmltodict.unparse(data, **kwargs)
        f.write(xmldata)