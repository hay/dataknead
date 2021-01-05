dataknead
=========
**Fluent conversion between data formats like JSON, XML and CSV**

Ever sighed when you wrote code to convert CSV to JSON for the thousandth time?

::

    import csv
    import json

    data = []

    with open("cities.csv") as f:
        reader = csv.DictReader(f)

        for row in reader:
            data.append(row)

    with open("cities.json", "w") as f:
        json.dump(data, f)

Stop sighing and use ``dataknead``:

::

    from dataknead import Knead
    Knead("cities.csv").write("cities.json")

Or make it even easier on the command line:

::

    knead cities.csv cities.json

``dataknead`` has inbuilt loaders for CSV, Excel, JSON, TOML and XML and you can easily write your own.

Philosophy
----------
``dataknead`` is intended for easy conversion between common data formats and basic manipulation. It's not a replacement for more complex libraries like ``pandas`` or ``numpy``, but instead can be a useful addition to those libraries.

The API is as minimal as possible and `fluent <https://en.wikipedia.org/wiki/Fluent_interface>`_.

The loaders for the different file formats are built upon existing and well-tested libraries like `xmltodict <https://github.com/martinblech/xmltodict>`_ and `openpyxl <https://openpyxl.readthedocs.io/en/stable/index.html>`_.

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

For a full list of all available options see the :ref:`API documentation <api>`.

Advanced example
----------------
Check out `the advanced example <https://github.com/hay/dataknead/blob/master/tests/advanced_example.py>`_. This also shows you how to do more complex data manipulation using external libraries like `jq <https://stedolan.github.io/jq/>`_.

More documentation
------------------
.. toctree::
   :maxdepth: 1

   api
   cli
   extending
   dev-info
   release-history
   Source on Github <https://github.com/hay/dataknead>

Credits
-------
``dataknead`` is written by `Hay Kranen <https://haykranen.nl/>`_.

Source
------
Source can be found on `Github <https://github.com/hay/dataknead>`_.

License
-------
Licensed under the `MIT license <https://opensource.org/licenses/MIT>`_.