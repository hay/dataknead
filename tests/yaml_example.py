from dataknead import Knead, BaseLoader
import yaml

class YamlLoader(BaseLoader):
    EXTENSION = "yaml"

    @staticmethod
    def read(f):
        return yaml.safe_load(f)

    @staticmethod
    def write(f, data, pretty = True):
        yamldata = yaml.dump(data)
        f.write(yamldata)

Knead.loaders.append(YamlLoader)

Knead("input/example.yaml").write("output/example.json", indent = 4)