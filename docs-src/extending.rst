.. _extending:

Extending dataknead
-------------------
You can write your own loaders to read and write other formats than the default ones.

Here's an example loader for the ``YAML`` format:

::

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

You would then use this loader like this:

::

    Knead.add_loader(Knead, YamlLoader)

    Knead("input/example.yaml").write("output/yaml-example.json", indent = 4)