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
from io import StringIO


from autoinvoice import configs
from .utils import default_configs_string, reload_configuration_to_defaults


class TestConfigs(unittest.TestCase):
    def setUp(self) -> None:
        reload_configuration_to_defaults()

    def test_default_settings_no_options(self):
        config = configs.config

        output = StringIO()
        config.write(output)

        self.assertEqual(output.getvalue(), default_configs_string)

    def test_format_bank_number(self):
        nrb = '04 1140 2004 0000 3102 7864 4964'
        self.assertEqual(configs.format_bank_number(nrb), nrb)

        iban = '04 1140 2004 0000 3102 7864 4964'
        self.assertEqual(configs.format_bank_number(iban), iban)

        with self.assertRaises(ValueError):
            num = '04 1140 2004 0000 3102 786'
            configs.format_bank_number(num)

        with self.assertRaises(ValueError):
            num = '04 1140 2004 0000 3102 7864 4964 5'
            configs.format_bank_number(num)

    def test_email(self):
        invalid_email1 = '@'
        invalid_email2 = '@email'
        invalid_email3 = 'a@email'
        invalid_email4 = 'a@'

        no_email = ''
        valid_email1 = 'm@m.m'
        valid_email2 = 'lukasz.busko@guns4hire.cc'
        valid_email3 = 'lukasz.busko@dom.longext'

        self.assertFalse(configs.is_email(invalid_email1))
        self.assertFalse(configs.is_email(invalid_email2))
        self.assertFalse(configs.is_email(invalid_email3))
        self.assertFalse(configs.is_email(invalid_email4))

        self.assertTrue(configs.is_email(no_email))
        # will fail regexp needs to be adjusted
        self.assertFalse(configs.is_email(valid_email1))
        self.assertTrue(configs.is_email(valid_email2))
        self.assertTrue(configs.is_email(valid_email3))
