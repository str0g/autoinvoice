AutoInvoice
====================

Dependencies
--------------------

Check ```setup.py``` script

Known issues
--------------------
- Current version of litex.regon does not fetch well short regon numbers so tests
depending on it my crash.
- Linux compatible only unless someone provide port.

Development
--------------------

### Resource for tests
Resources for tests should be used to build proper application configuration.
```
tests/data/
├── configs
│   ├── apiregon2.ini
│   ├── apiregon.ini
│   ├── config.ini
│   ├── path_to_number.ini
│   ├── pdflatex_subprocess.ini
│   ├── read_json.ini
│   ├── retail.ini
│   └── zbp2d.ini
├── dbases
│   ├── dbase.db
│   ├── dbase.sql
│   └── dbase_table.sql
├── items
│   ├── items1.json
│   ├── items2.json
│   ├── items3.json
│   ├── items4.json
│   ├── items5.json
│   ├── items6.json
│   └── items7.json
├── sample1.xml
├── sample2.xml
└── templates
    ├── companies_only.tex
    ├── qrcode.tex
    ├── read_json.tex
    ├── retail.tex
    ├── template_path_to_number.tex
    └── text-5261040828.tex
```

### Storing new test data for later dbase usage
sqlite3 dbase  
>``.output dbase.sql``  
>``.dump``  
or  
>``.du``

### Restoring database
`sqlite3 dbase.db < dbase.sql`

### Preparing input for build record
Input expects python str other ways' application may not work correctly and tests are
going to fail.
So It's very important to check encoding and data type returned by chosen data
provider.

Usage
===========

 Configuration
-----------
Configuration file should be located in ~/.autoinvoice/config.ini

- default configuration options can be found in `configs.py:get_configuration`
- each plugin my have its own special options which can be defined in `config.ini`

Shell alias
-----------
It's very handy to create alias like

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
Application configuration is being design to provide configuration for plugins if
needed. To get more information check tests/data

### Retail
It's possible to get client record with phone number or email but database
needs to be open w `sqlitebrowser` or other tool to inject data.
- sample with direct sql operation
```
sqlite3 dbase.db "insert into customers
(phone_number, email, customername, state, address, postcode, city, refere, extra_note)
values
('+48189807150','jan.brzechwa@wieszcze.pl','Jan Brzechwa','Winnicki','ul. Brzechwy 42','66-666','Żmerynka','Jan Brzechwa','WZM22')"
```


### Offline usage
It's possible to use application with our network. User can see warning in few places
but invoice is going to be generated as expected as long as client record is in database.

### Company register

- apiregon2 for Polish government companies database.
- apiregon for Polish government companies database(legacy will be dropped soon).

### Automatic Invoice Numbering

- ```path_to_number``` is going to create unique number from catalog structure ```01/202007``` \
```├── 202007```\
```│   ├── 01_some_description\```

### Items reader

- ```read_json``` - if autoinvoice parameter ```-i some_file.json``` has been used
provided plugin is going to generate proper invoice,
fields like count, taxes, amounts, total, additionally thru this file is possible
to pass payment deadline and change
  invoice dates (refer to templates in tests/data).

### Qrcodes for payment transactions

- ```zbp2d``` - compatible with [Polish Banks standards](https://zbp.pl/public/repozytorium/dla_bankow/rady_i_komitety/bankowosc_elektroczniczna/rada_bankowosc_elektr/zadania/2013.12.03_-_Rekomendacja_-_Standard_2D.pdf)
and require additional configuration section.

### Character replacer

- ```tex``` - makes special characters plain before filling tex template

### Builder

- ```pdflatex_subprocess``` - creates pdf file as final result