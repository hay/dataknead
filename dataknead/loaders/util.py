from enum import Enum

# This assumes a list with dicts, loop over all dicts, and get the unique
# keys
def get_fieldnames(data):
    fieldnames = set()

    for item in data:
        [fieldnames.add(key) for key in item.keys()]

    return list(fieldnames)

class SnifferType(Enum):
    list_with_dicts = 1
    list_with_lists = 2
    single_list = 3
    single_dict = 4

# Sniff the format of a data and return a SnifferType type
def sniff_type(data):
    if all([isinstance(i, dict) for i in data]):
        # List with dictionaries saved as a file with a header
        return SnifferType.list_with_dicts
    elif all([isinstance(i, list) for i in data]):
        # A list with lists
        return SnifferType.list_with_lists
    elif isinstance(data, list):
        # Just one single column
        return SnifferType.single_list
    elif isinstance(data, dict):
        # Only a header and one row
        return SnifferType.single_dict
    else:
        raise Exception("Could not sniff the type of this data")