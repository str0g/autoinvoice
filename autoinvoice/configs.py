# -*- coding: utf-8 -*-

#################################################################################
#    Autoinvoice is a program to automate invoicing process                     #
#    Copyright (C) 2021  Łukasz Buśko                                           #
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


def tax_ref(option, opt_str, value, parser):
    if(not value[0].isnumeric()):
        raise ValueError('taxpayerid must be numeric')
    parser.values.taxpayerid = value[0]
    setattr(parser.values, 'name', value[1])


def get_options():
    parser = OptionParser()
    parser.add_option("-g", "--generate", action="append", type="int",
            help="Input Taxpayerid and generate document template, can be used multiple times")
    parser.add_option("-u", "--update", action="append", type="int",
            help="Update records for Taxpayerid, can be used multiple times")
    parser.add_option("-c", "--configuration", type="string",
            default="~/.autoinvoice/config",
            help="Configuration file")
    parser.add_option("-d", "--database", type="string",
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

    if options.configuration.find('~') != -1:
        options.configuration = expanduser(options.configuration)

    return options


def get_configuration(options):
    config = ConfigParser()
    #read default values
    config.read_dict({
            'Common': {
                        'url': '',
                        'key': '',
                        },
            'Plugins': {
                            'mod_company_register': 'apiregon2',
                            'mod_invoice_numbering': '',
                            'mod_qrcodes': '',
                        },
            'Paths': {
                            'database': '~/.autoinvoice/dbase.db',
                            'template': '/usr/share/polishinvoice/templates/simple.tex'
                        },
            'Refere': {
                            'taxpayerid': '',
                            'name': '',
                            'account_number': '',
                        },
            })

    config.read([options.configuration], encoding='utf-8')

    def expand_user_path(config, *args):
        tmp = config.get(*args)
        if tmp.find('~') != -1:
            config.set(*args, expanduser(tmp))

    expand_user_path(config, 'Paths', 'database')
    expand_user_path(config, 'Paths', 'template')

    return config


def update_configuration(options, config):
    config.add_section('Options')
    if options.database:
        if options.database.find('~') != -1:
            options.database = expanduser(options.database)
        config.set('Paths', 'database', options.database)
    if options.template:
        if options.template.find('~') != -1:
            options.template = expanduser(options.template)
        config.set('Paths', 'template', options.template)
    if options.taxpayerid:
        config.set('Refere', 'taxpayerid', options.taxpayerid)
        config.set('Refere', 'name', options.name)
    if options.items:
        config.set('Options', 'items', options.items)
    if options.verbose:
        config.set('Options', 'verbose', str(options.verbose))


def set_configuration():
    options = get_options()
    config = get_configuration(options)

    update_configuration(options, config)

    if options.verbose:
        import sys
        config.write(sys.stdout)

    return config, options


config, options = set_configuration()


def reload_configuraiton():
    config, options = set_configuration()
