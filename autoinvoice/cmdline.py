# -*- coding: utf-8 -*-

#################################################################################
#    Autoinvoice is a program to automate invoicing process                     #
#    Copyright (C) 2019  Łukasz Buśko                                           #
#                                                                               #
#    This program is free software: you can redistribute it and/or modify       #
#    it under the terms of the GNU General Public License as published by       #
#    the Free Software Foundation, either version 3 of the License, or          #
#    (at your option) any later version.                                        #
#                                                                               #
#    This program is distributed in the hope that it will be useful,            #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of             #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              #
#    GNU General Public License for more details.                               #
#                                                                               #
#    You should have received a copy of the GNU General Public License          #
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.      #
#################################################################################

from optparse import OptionParser
from configparser import ConfigParser
from os.path import expanduser

from .driver import Driver

def Configuration(options):
    config = ConfigParser()
    #read default values
    config.read_dict({
            'Common' : {
                        'url' : '',
                        'key' : '',
                        'register' : 'apiregon',
                        },
            'Plugins' : {
                            'invoice_numbering': '',
                            'qrcode_generator': '',
                        },
            'Paths' : {
                        'database' : '~/.autoinvoice/dbase.db',
                        'template' : '/usr/share/polishinvoice/templates/simple.tex'
                        },
            'Refere' : {
                        'taxpayerid' : '',
                        'name' : '',
                        'account_number' : '',
                        },
            'QRCode': {}
            })

    config.read([options.configuration], encoding='utf-8')

    if hasattr(options, 'name'):
        config.set('Refere', 'name', options.name)

    if options.taxpayerid:
        config.set('Refere', 'taxpayerid', options.taxpayerid)

    if options.verbose:
        import sys
        config.write(sys.stdout)

    dbpath = config.get('Paths', 'database')
    if dbpath:
        if dbpath.find('~') != -1:
           config.set('Paths', 'database', expanduser(dbpath))
    template = config.get('Paths', 'template')
    if template:
        if template.find('~') != -1:
            config.set('Paths', 'template', expanduser(template))

    return config

def tax_ref(option, opt_str, value, parser):
    if(not value[0].isnumeric()):
        raise ValueError('taxpayerid must be numeric')
    parser.values.taxpayerid = value[0]
    setattr(parser.values, 'name', value[1])

def Options():
    parser = OptionParser()
    parser.add_option("-g", "--generate", action="append", type="int",
            help="Input Taxpayerid and generate document template, can be used multiple times")
    parser.add_option("-u", "--update", action="append", type="int",
            help="Update records for Taxpayerid, can be used multiple times")
    parser.add_option("-c","--configuration", type="string",
            default="~/.autoinvoice/config",
            help="Configuration file")
    parser.add_option("-d","--database", type="string",
            help="Data base path")
    parser.add_option("-t", "--template", type="string",
            help="File with predefined markers")
    parser.add_option("-o", "--output", type="string",
            help="Output file for filled template")
    parser.add_option("--taxpayerid", action="callback", type="string", nargs=2, callback=tax_ref,
            help="<taxpayerid> \"<name surename>\"")
    parser.add_option("-i", "--items", type="string", help="File with items")
    parser.add_option("-v", "--verbose", action="store_true", default=False, dest="verbose",
            help="Verbouse")

    (options, args) = parser.parse_args()

    if options.generate:
        options.generate = [str(g) for g in options.generate]

    return options


def settattr_from_configuration_group(options, config, group: str):
    if group in config:
        for opt in config[group]:
            setattr(options, opt, config[group][opt])


def main():
    options = Options()

    if options.configuration.find('~') != -1:
        options.configuration = expanduser(options.configuration)

    config = Configuration(options)

    if not options.database:
        options.database = config.get('Paths', 'database')
    elif options.database.find('~') != -1:
        options.database = expanduser(options.database)

    if not options.template:
        options.template = config.get('Paths', 'template')
    elif options.template.find('~') != -1:
        options.template.expanduser(options.template)

    if not options.taxpayerid:
        options.taxpayerid = config.get('Refere', 'taxpayerid')
        setattr(options, 'name', config.get('Refere', 'name'))
    #setattr(options, 'account_number', config.get('Refere', 'account_number'))

    setattr(options, 'url', config.get('Common', 'url'))
    setattr(options, 'key', config.get('Common', 'key'))
    setattr(options, 'register', config.get('Common', 'register'))
    # Plugins
    settattr_from_configuration_group(options, config, 'Plugins')
    # QRCode
    settattr_from_configuration_group(options, config, 'QRCode')

    if options.verbose:
        print(options)

    driver = Driver(options)

    if options.update:
        for taxpaierid in options.update:
            driver.updateRecord(str(taxpaierid))
    if options.generate:
        for taxpayerid in options.generate:
            template = driver.generateInvoiceTemplete(taxpayerid)
            if not options.output:
                print(template)
            else:
                index = options.output.rfind('.')
                output = options.output[:index] + '-' + taxpayerid + options.output[index:]
                with open(output, 'w') as fd:
                    fd.write(template)

    return 0


if __name__ == "__main__":
    main()
