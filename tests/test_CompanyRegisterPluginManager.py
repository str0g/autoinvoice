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

import unittest

from autoinvoice.mod_company_register.plugins.apiregon2 import APIREGON2
from autoinvoice.mod_company_register.manager import manager
from autoinvoice import configs


class TestgetCompanyRegister(unittest.TestCase):
    def setUp(self):
        configs.reload_configuraiton()
        configs.config.set('Plugins', 'mod_company_register', 'apiregon2')

    def test_getCompanyRegister(self):
        self.assertIs(APIREGON2, type(manager()))

    def test_getCompanyRegister_neg(self):
        configs.config.set('Plugins', 'mod_company_register', 'CZ')
        configs.config.set('Options', 'verbose', 'True')
        with self.assertRaises(KeyError):
            manager()
