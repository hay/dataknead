Command line utility (``knead``)
================================

``dataknead`` includes the ``knead`` command line utility you can use for simple conversion of data formats.

::

    knead cities.csv cities.json

Will transform a filed called ``cities.csv`` to a file called ``cities.json`` and is equivalent to this piece of Python code

::

    Knead("cities.csv").write("cities.json")

``knead`` can also be used as a quick way of viewing the contents of a file, just give it an input file

::

    knead cities.csv

This is equivalant to

::

    print(Knead("cities.csv").data())

You can also specify the input and output formats, when those are not available in the file extension, or if you want to overwrite them. This is useful in combination with the ``--stdin`` option, which allows you to take data from stdin and directly transform output from a HTTP API to something else.

For example, this API request gives you back a JSON summary of the article for Amsterdam on the English Wikipedia.

::

    curl https://en.wikipedia.org/api/rest_v1/page/summary/Amsterdam

Piping that into dataknead using ``--stdin`` and ``-if json`` gives you a nicely formatted file

::

    curl https://en.wikipedia.org/api/rest_v1/page/summary/Amsterdam | knead --stdin -if json

All options
-----------
You'll see this when running ``knead -h``

::

    usage: knead [-h] [-v] [--input-format INPUT_FORMAT]
                 [--output-format OUTPUT_FORMAT] [--stdin]
                 [input] [output]

    Fluently process and convert data formats like JSON and CSV

    positional arguments:
      input                 Input file
      output                Output file

    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         Show debug information
      --input-format INPUT_FORMAT, -if INPUT_FORMAT
                            Input format
      --output-format OUTPUT_FORMAT, -of OUTPUT_FORMAT
                            Output format
      --stdin               Take data from stdin (requires --input-format)