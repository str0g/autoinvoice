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

from os.path import expanduser

class ConfigurationCreator:
    def __init__(self, input_options: dict = None):
        self.input_options = {
            'url': '',
            'key': '',
            'mod_invoice_numbering': '',
            'mod_qrcodes': '',
            'mod_builder': '',
            'taxpayerid': '',
            'name': '',
            'account_number': '',
            'register': 'apiregon',
            'database': expanduser('~/.autoinvoice/dbase.db'),
            'template': '/usr/share/polishinvoice/templates/simple.tex',
            'verbose': False,
            'email': ''
        }
        if input_options:
            self.input_options.update(input_options)
        self.config_template = '''\
[Common]
url = {url}
key = {key}

[Plugins]
mod_company_register = {register}
mod_invoice_numbering = {mod_invoice_numbering}
mod_qrcodes = {mod_qrcodes}
mod_builder = {mod_builder}

[Paths]
database = {database}
template = {template}

[Refere]
taxpayerid = {taxpayerid}
name = {name}
account_number = {account_number}
email = {email}

[Options]\
'''

    def get_configuration(self):
        out = self.config_template.format(**self.input_options)
        if self.input_options['verbose']:
            out = '''\
{}
verbose = True\
'''.format(out)
        return out

    def __str__(self):
        input_options = {
            'taxpayerid': self.input_options['taxpayerid'],
            'database': self.input_options['database'],
            'template': self.input_options['template'],
        }
        out = '''[Input options]\
%s
[Configuration]
%s''' % (self.input_options, self.get_configuration())
        return out

#{'generate': None, 'update': [5261044039, 5261044039], 'configuration': 'tests/data/config_apiregon', 'database': None, 'template': None, 'output': None, 'taxpayerid': None, 'items': None, 'verbose': True}