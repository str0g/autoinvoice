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

from autoinvoice.mod_company_register.plugins.iface import ICompanyRegister


class TestICompanyRegister(unittest.TestCase):
    def setUp(self):
        self.reg = ICompanyRegister()

    def test_getRecords(self):
        with self.assertRaises(NotImplementedError):
            self.reg.getRecords(111111, None, None)

        with self.assertRaises(NotImplementedError):
            self.reg.getRecords(None, None, None)

    def test_recordToRefere(self):
        record_in = {'taxpayerid': '5261040828', 'regon': '000331501', 'customername': 'GŁÓWNY URZĄD STATYSTYCZNY', 'state': 'MAZOWIECKIE', 'address': 'ul. Test-Krucza 208', 'postcode': '00-925', 'city': 'Warszawa', 'refere': '@TODO'}

 
        record_exp = {'ref_taxpayerid': '5261040828', 'ref_regon': '000331501', 'ref_companyname': 'GŁÓWNY URZĄD STATYSTYCZNY', 'ref_state': 'MAZOWIECKIE', 'ref_address': 'ul. Test-Krucza 208', 'ref_postcode': '00-925', 'ref_city': 'Warszawa', 'ref_refere': '@TODO'}

        
        record_out = self.reg.recordToRefere(record_in)
        self.assertEqual(record_out, record_exp)


