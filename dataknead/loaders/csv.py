from dataknead.baseloader import BaseLoader
import csv

class CsvLoader(BaseLoader):
    EXTENSIONS = ["csv"]

    @staticmethod
    def read(f, has_header = None):
        # If not forcing the header, sniff if we've got one
        # and then use DictReader, otherwise just read as regular csv
        # csv.Sniffer can fail at times (see #5), so the user can overrule this
        if has_header == None:
            sniffer = csv.Sniffer()

            try:
                has_header = sniffer.has_header(f.read(2048))
            except:
                # No delimiter, assume this is just a list of newline-separated values
                has_header = False

            f.seek(0)

        if has_header:
            reader = csv.DictReader(f)
        else:
            reader = csv.reader(f)

        return [row for row in reader]

    @staticmethod
    def write(f, data, fieldnames = None):
        # First check if we can write this to a file
        if (not isinstance(data, list)) and (not isinstance(data, dict)):
            raise TypeError("Can't write type '%s' to csv" % type(data).__name__)

        # Four ways to write data to a CSV file :)
        if all([isinstance(i, dict) for i in data]):
            # List with dictionaries saved as a file with a header

            # First extract all the fieldnames from the list
            if not fieldnames:
                fieldnames = set()
                for item in data:
                    [fieldnames.add(key) for key in item.keys()]

            # Then open the CSV file and write
            writer = csv.DictWriter(f, fieldnames = fieldnames)
            writer.writeheader()
            [writer.writerow(row) for row in data]
        elif all([isinstance(i, list) for i in data]):
            # A list with lists
            writer = csv.writer(f)

            if fieldnames:
                writer.writerow(fieldnames)

            [writer.writerow(row) for row in data]
        elif isinstance(data, list):
            # Just one single column
            writer = csv.writer(f)

            if fieldnames:
                writer.writerow(fieldnames)

            [writer.writerow([row]) for row in data]
        elif isinstance(data, dict):
            # Only a header and one row
            writer = csv.writer(f)
            writer.writerow(data.keys())
            writer.writerow(data.values())