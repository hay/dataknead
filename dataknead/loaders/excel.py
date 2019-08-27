from dataknead.baseloader import BaseLoader

class ExcelLoader(BaseLoader):
    EXTENSIONS = ["xls", "xlsx"]

    @staticmethod
    def read(f, **kwargs):
        # We import pandas here because it's faster when *not* converting Excel :)
        import pandas

        df =  pandas.read_excel(f.name, sheet_name = None, **kwargs)

        # If we have one single sheet, just print that, otherwise convert
        # to a dict with the sheet names as keys
        if len(df) == 1:
            key = list(df)[0]
            return df[key].to_dict("records")
        else:
            return { key:df[key].to_dict("records") for key in df }

    @staticmethod
    def write(f, data):
        import pandas

        df = pandas.DataFrame(data)
        df.to_excel(f.name)