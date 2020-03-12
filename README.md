AutoInvoice
====================

Dependecies
--------------------

> py3-lxml for litex.regon
> litex.regon for soap communication

Known issue
--------------------
Current version of litex.regon does not fetch well regon number so tests depending on it my crash.

Linux compatible only unless someone provide port.

Development
--------------------

### Resource for tests
tests/
├── config
├── config_apiregon
├── dbase.db
├── dbase.sql
├── dbase_table.sql
├── template1.tex
└── text-5261040828.tex


### Storing new test data for later dbase usage
sqlite3 dbase
>>> .output dbase.sql
>>> .dump

or

>>> .du

### Restoring database
sqlite3 dbase.db < dbase.sql

### prepering input for build record
Input expects python str other ways application may not work correctly and tests are going to fail.
So its very important to check encoding and data type returned by chosen data provider.

Usage
--------------------

### Configuration
Configuration file should be located in ~/.autoinvoice/config

### shell alias
Its very handy to create alias like

``alias autoinvoices="python3 -m autoinvoice"``

``alias autoinvoices-hardcoded="python3 -m autoinvoice -t <path_template_for_hardcoded_client> -g <hardcoded_client>"``
