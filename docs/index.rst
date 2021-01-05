.. dataknead documentation master file, created by
   sphinx-quickstart on Tue Jan  5 16:30:47 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

dataknead
=========
**Effortless conversion between data formats like JSON, XML and CSV**

.. toctree::
   :hidden:

Have you ever sighed when writing code like this?

::

    import csv
    import json

    with open("names.json") as f:
        data = json.loads(f.read())

    data = [row["name"] for row in data if "John" in row["name"]]

    with open("names.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["name"])
        [writer.writerow([row]) for row in data]

Now you can write it like this:

::

    from dataknead import Knead
    Knead("names.json").filter(lambda r:"John" in r["name"]).write("names.csv")

Or what about simply converting ``json`` to ``csv``? With ``dataknead`` you get the ``knead`` command line utility which makes things easy:

::

    knead names.json names.csv

``dataknead`` has inbuilt loaders for CSV, Excel, JSON and XML and you can easily write your own.

Philosophy
----------
``dataknead`` is intended for easy conversion between common data formats and basic manipulation. It's not a replacement for more complex libraries like ``pandas`` or ``numpy``, but instead can be a useful addition to those libraries.

The API is as minimal as possible and `fluent <https://en.wikipedia.org/wiki/Fluent_interface>`_.

I try to use as many existing and well-tested libraries as possible. For example, the XML loader uses the excellent `xmltodict <https://github.com/martinblech/xmltodict>`_ module.

Installation
------------
Install ``dataknead`` from `PyPi <https://pypi.python.org/pypi/dataknead>`_.

::

    pip install dataknead

Then import

::

    from dataknead import Knead

Basic example & tutorial
------------------------

Let's say you have a small CSV file with cities and their population called ``cities.csv``.

::

    city,country,population
    Amsterdam,nl,850000
    Rotterdam,nl,635000
    Venice,it,265000

And you want to load this csv file and transform it to a json file.

::

    from dataknead import Knead

    Knead("cities.csv").write("cities.json")

You'll now have a json file called ``cities.json`` that looks like this:

::

    [
        {
            "city" : "Amsterdam",
            "country" : "nl",
            "population" : 850000
        },
        ...
    ]

Maybe you just want the city names and write them to a CSV filed called ``city-names.csv``.

::

    from dataknead import Knead

    Knead("cities.csv").map("city").write("city-names.csv")

That will give you this list

::

    Amsterdam
    Rotterdam
    Venice

Now you want to extract only the cities that are located in Italy, and write that back to a new csv file called ``cities-italy.csv``:

::

    from dataknead import Knead

    Knead("cities.csv").filter(lambda r:r["country"] == "it").write("cities-italy.csv")

This gives you this:

::

    city,country,population
    Venice,it,265000

Nice huh?

Advanced example
----------------
Check out `the advanced example <https://github.com/hay/dataknead/blob/master/tests/advanced_example.py>`_. This also shows you how to do more complex data manipulation using external libraries like `jq <https://stedolan.github.io/jq/>`_.

Extending dataknead
-------------------
You can write your own loaders to read and write other formats than the default ones. For an example take a look at the `YAML example <https://github.com/hay/dataknead/blob/master/tests/yaml_example.py>`_.

Other pages
-----------

.. toctree::
   :maxdepth: 1

   cli
   api
   dev-info
   release-history

Credits
=======
``dataknead`` is written by `Hay Kranen <https://haykranen.nl/>`_.

License
-------
Licensed under the `MIT license <https://opensource.org/licenses/MIT>`_.