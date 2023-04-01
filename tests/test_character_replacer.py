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

import unittest

from autoinvoice import configs
from autoinvoice.mod_character_replacer.manager import manager
from autoinvoice.mod_character_replacer.plugins.tex import Tex


class TestGetPdfLatexSubprocess(unittest.TestCase):
    def setUp(self) -> None:
        self._dict = {
            'ref_email': 'refemail',
            'ref_companyname': 'refcompanyname',
            'ref_address': 'refaddress',
            'ref_city': 'refcity',
            'invoice_number': 'invoice',
            'customername': 'customername',
            'address': 'address',
            'city': 'city',
        }

    def test_tex_character(self):
        configs.config.set('Paths', 'template', 'file.tex')
        plugin = manager()
        self.assertIsInstance(plugin, Tex)

        specials = '&%$#_{}~^\\'

        mod_dict = {}
        for key in self._dict.keys():
            mod_dict[key] = f'{self._dict[key]}{specials}'

        exp_specials = '\\&\\%\\$\\#\\_\\{\\}\\~\\^\\\\'
        exp_dict = {}
        for key in self._dict.keys():
            exp_dict[key] = f'{self._dict[key]}{exp_specials}'

        self.assertNotEqual(mod_dict, self._dict)

        plugin(mod_dict)

        self.maxDiff = None
        self.assertDictEqual(mod_dict, exp_dict)
