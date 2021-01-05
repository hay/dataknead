from dataknead import Knead, BaseLoader
import yaml

class YamlLoader(BaseLoader):
    EXTENSIONS = ["yaml"]

    @staticmethod
    def read(f, **kwargs):
        return yaml.safe_load(f, **kwargs)

    @staticmethod
    def write(f, data):
        yamldata = yaml.dump(data)
        f.write(yamldata)

Knead.add_loader(Knead, YamlLoader)

Knead("input/example.yaml").write("output/yaml-example.json", indent = 4)