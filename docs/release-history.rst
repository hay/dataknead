Release history
===============

0.4
---
* Upgraded dependencies, ``dataknead`` now requires Python 3.6.1 or higher
* Added a TOML loader.
* Completely rewrote the Excel loader so we can remove the depedency on ``pandas``. Removed support for the legacy ``xls`` format, only ``xlsx`` is supported. This fixes #14.

0.3
---
* Breaking change: removed the ``query`` method: the focus of ``dataknead`` is on conversion. Using ``apply`` you can easily use a tool like ``jq`` to query.

0.2
---
* Adding tuple shortcut to ``map`` (#2)
* Adding support for ``txt`` files ((#4)
* Adding support for loader constructor argument passing, and adding a ``has_header`` option to ``CsvLoader`` (#5)

0.1
---
Initial release