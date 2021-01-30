AutoInvoice
====================

Dependencies
--------------------

Check ```setup.py``` script

Known issues
--------------------
- Current version of litex.regon does not fetch well short regon numbers so tests depending on it my crash.
- Linux compatible only unless someone provide port.

Development
--------------------

### Resource for tests
Resources for tests should be used to build proper application configuration.
```
tests/data/
|____dbase_table.sql
|____configs
| |____pdflatex_subprocess.json
| |____zbp2d.json
| |____read_json.json
| |____path_to_number.json
| |____config.json
|____config
|____dbase.db
|____text-5261040828.tex
|____config_apiregon
|____templates
| |____qrcode.tex
| |____read_json.tex
| |____companies_only.tex
|____sample2.xml
|____template_path_to_number.tex
|____items2.json
|____dbase.sql
|____items3.json
|____items4.json
|____sample1.xml
|____items1.json
```

### Storing new test data for later dbase usage
sqlite3 dbase  
>``.output dbase.sql``  
>``.dump``  
or  
>``.du``

### Restoring database
sqlite3 dbase.db < dbase.sql

### prepering input for build record
Input expects python str other ways application may not work correctly and tests are going to fail.
So its very important to check encoding and data type returned by chosen data provider.

Usage
===========

 Configuration
-----------
Configuration file should be located in ~/.autoinvoice/config

Shell alias
-----------
Its very handy to create alias like

``alias autoinvoices="python3 -m autoinvoice"``

Alias for different profile then default\
``alias autoinvoices-hardcoded="python3 -m autoinvoice -t <path_template_for_hardcoded_client> -g <hardcoded_client>"``

Plugins
-----------
Plugins folders starts with mod_*\
Every folder has similar pattern
```
├── mod_*
│   ├── __init__.py
│   ├── manager.py
│   ├── plugins
│   │   ├── iface.py
│   │   ├── __init__.py
│   │   ├── some_implementation.py
```
Application configuration is being design to provide configuration for plugins if needed. To get more information check tests/data

### Company register

- apiregon2 for Polish government companies database.
- apiregon for Polish government companies database(legacy will be dropped soon).

### Automatic Invoice Numbering

- ```path_to_number``` is going to create unique number from catalog structure ```01/202007``` \
```├── 202007```\
```│   ├── 01_some_description\```

### Items reader

- ```read_json``` - if autoinvoice parameter ```-i some_file.json``` will be provided plugin is going to generate proper invoice,
count taxes and other amounts (refer to templates in tests/data).

### Qrcodes for payment transactions

- ```zbp2d``` - compatible with [Polish Banks standards](https://zbp.pl/public/repozytorium/dla_bankow/rady_i_komitety/bankowosc_elektroczniczna/rada_bankowosc_elektr/zadania/2013.12.03_-_Rekomendacja_-_Standard_2D.pdf)
and require additional configuration section.

### Character replacer

- ```tex``` - makes special characters plain before filling tex template

### Builder

- ```pdflatex_subprocess``` - creates pdf file as final result