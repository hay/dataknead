# For this example you need to install the pandas, openpyxl, xlwt and xlrd libraries
from _context import dataknead
from dataknead import Knead, BaseLoader
import pandas

class ExcelLoader(BaseLoader):
    EXTENSION = ("xls", "xlsx")

    @staticmethod
    def read(f, **kwargs):
        df =  pandas.read_excel(f.name, **kwargs)
        return df.to_dict("records")

    @staticmethod
    def write(f, data):
        df = pandas.DataFrame(data)
        df.to_excel(f.name)

Knead.loaders.append(ExcelLoader)

Knead("input/cities.xlsx").print()
Knead("input/cities.csv").write("output/cities.xls")