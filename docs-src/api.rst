.. _api:

API documentation
=================

Knead
-----
.. autoclass:: dataknead.Knead
   :members:
   :undoc-members:
   :special-members: __init__

Loaders
-------
These loaders are available by default. Note that you never need to access these directly,
they are merely documented here for reference purposes and as an example if you want to
write your own loader.

CsvLoader
^^^^^^^^^
.. autoclass:: dataknead.loaders.csv.CsvLoader

ExcelLoader
^^^^^^^^^^^
.. autoclass:: dataknead.loaders.excel.ExcelLoader

JsonLoader
^^^^^^^^^^
.. autoclass:: dataknead.loaders.json.JsonLoader

TextLoader
^^^^^^^^^^
.. autoclass:: dataknead.loaders.text.TextLoader

TomlLoader
^^^^^^^^^^
.. autoclass:: dataknead.loaders.toml.TomlLoader

XmlLoader
^^^^^^^^^
.. autoclass:: dataknead.loaders.xml.XmlLoader