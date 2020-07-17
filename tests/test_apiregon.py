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

from autoinvoice.CompanyRegister.plugins.apiregon import APIREGON
from .dummy import Dummy


class TestAPIREGON(unittest.TestCase):
    def test_getRecords(self):
        paths = ['tests/data/sample1.xml', 'tests/data/sample2.xml']

        sample1_out = [{'taxpayerid': '5261040828', 'regon': '000331501', 'companyname': 'GŁÓWNY URZĄD STATYSTYCZNY', 'state': 'MAZOWIECKIE', 'address': 'ul. Test-Krucza 208', 'postcode': '00-925', 'city': 'Warszawa', 'refere': '@TODO'}]

        sample2_out = [{'taxpayerid': 'nnnnnnnnnn', 'regon': 'xxxxxxxxx', 'companyname': 'AAAAAAAA', 'state': 'LUBELSKIE', 'address': 'ul. Test-Wilcza yy', 'postcode': '23-200', 'city': 'Kraśnik', 'refere': '@TODO'}, {'taxpayerid': 'nnnnnnnnnn', 'regon': 'xxxxxxxxx', 'companyname': 'GOSPODARSTWO ROLNE', 'state': 'LUBELSKIE', 'address' : 'zz', 'postcode': '23-213', 'city': 'Sulów', 'refere': '@TODO'}]

        krs = APIREGON(Dummy().values)
        for path in paths:
            out = krs.getRecords(path, None, None)
            if path == paths[0]:
                self.assertEqual(sample1_out, out)
            elif path == paths[1]:
                self.assertEqual(sample2_out, out)
            else:
                raise ValueError('Fix test')

    def test_getRecords_neg(self):
        with self.assertRaises(ValueError):
            krs = APIREGON(Dummy().values)
            out = krs.getRecords(None, None, None)

    def test_getRecordswithAPI(self):
        exp = {'taxpayerid': '5261040828', 'regon': '000331501', 'companyname': 'GŁÓWNY URZĄD STATYSTYCZNY', 'state': 'MAZOWIECKIE', 'address': 'ul. Test-Krucza 208', 'postcode': '00-925', 'city': 'Warszawa', 'refere': ''}

        url = 'https://wyszukiwarkaregontest.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc'
        key = 'abcde12345abcde12345'

        krs = APIREGON(Dummy().values)
        out = krs.getRecords(exp['taxpayerid'], url, key)[0]

        self.assertDictEqual(exp, out)
