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

from os.path import expanduser, join
from shutil import copyfile
import sys

from autoinvoice import configs

default_configs_string = f"""\
[Common]
url = 
key = 

[Plugins]
mod_company_register = apiregon2
mod_invoice_numbering = 
mod_qrcodes = 
mod_builder = 

[Paths]
database = {expanduser('~/.autoinvoice/dbase.db')}
template = /usr/share/polishinvoice/templates/simple.tex

[Refere]
taxpayerid = 
name = 
account_number = 
email = 

[Options]

"""


def reload_configuration_to_defaults(config='does-not-exist'):
    sys.argv = sys.argv[:2]
    sys.argv.append('-c')
    sys.argv.append(config)
    configs.reload_configuraiton()


# @TODO this function needs to be renamed
def set_default_config():
    configs.config.set('Refere', 'taxpayerid', '5222680297')
    configs.config.set('Refere', 'account_number', '93114020040000320300621961')
    #
    #configs.config.set('QRCode', 'country_iso', 'PL')
    #


def use_temporary_directory(func):
    def inner(*args, **kwargs):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as tmpdirname:
            from_database = 'tests/data/dbase.db'
            to_database = join(tmpdirname, 'dbase.db')
            copyfile(from_database, to_database)
            #
            sys.argv.append('--database')
            sys.argv.append(to_database)
            #
            configs.config.set('Paths', 'database', to_database)
            #
            func(*args, tmpdirname=tmpdirname, **kwargs)
    return inner
