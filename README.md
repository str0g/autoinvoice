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
├── config
├── config_apiregon
├── config_path_to_number
├── config_qrcode_zbp2d
├── config_read_json
├── dbase.db
├── dbase.sql
├── dbase_table.sql
├── items1.json
├── items2.json
├── items3.json
├── items4.json
├── sample1.xml
├── sample2.xml
├── template1.tex
├── template_path_to_number.tex
├── template_qrcode.tex
├── template_read_json.tex
└── text-5261040828.tex
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
