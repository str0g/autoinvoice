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

from .dummy import Dummy

from autoinvoice.CompanyRegister.plugins.apiregon import APIREGON
from autoinvoice.CompanyRegister.CompanyRegisterPluginManager import getCompanyRegister


class TestgetCompanyRegister(unittest.TestCase):
    def test_getCompanyRegister(self):
        inp = Dummy()
        inp.values.verbose = True
        inp.values.register = 'apiregon'
        self.assertIs(APIREGON, type(getCompanyRegister(inp.values)))

    def test_getCompanyRegister_neg(self):
        inp = Dummy()
        inp.values.verbose = True
        inp.values.register = 'CZ'
        with self.assertRaises(KeyError):
            getCompanyRegister(inp.values)
