import json

def print_json(data, indent = 4):
    print(json.dumps(data, indent = indent))

def read_json(path):
    with open(path) as f:
        return json.loads(f.read())

def write_json(path, data, indent = None):
    with open(path, "w") as f:
        f.write(json.dumps(data, indent))

class DictQuery(dict):
    def get(self, path, default = None):
        keys = path.split("/")
        val = default

        for key in keys:
            if val:
                if not key:
                    break
                elif isinstance(val, list):
                    return default
                else:
                    val = val.get(key, default)
            else:
                val = dict.get(self, key, default)

            if not val:
                break;

        return val