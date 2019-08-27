from dataknead import Knead, BaseLoader
import yaml
import logging

logging.basicConfig(level=logging.DEBUG)


class YamlLoader(BaseLoader):
    EXTENSIONS = ["yaml"]

    @staticmethod
    def read(f):
        return yaml.safe_load(f)

    @staticmethod
    def write(f, data, pretty = True):
        yamldata = yaml.dump(data)
        f.write(yamldata)

Knead.add_loader(Knead, YamlLoader)

Knead("input/example.yaml").write("output/example.json", indent = 4)