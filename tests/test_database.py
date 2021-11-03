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
import os
import sqlite3

from autoinvoice.mod_company_register.database import DataBase

data_in = {'taxpayerid': '5261040828', 'regon': '000331501', 'companyname': 'GŁÓWNY URZĄD STATYSTYCZNY', 'state': 'MAZOWIECKIE', 'address': 'ul. Test-Krucza 208', 'postcode': '00-925', 'city': 'Warszawa', 'refere': '@TODO'}


class TestDataBase(unittest.TestCase):
    path_db = 'dbase_test.db'

    def setUp(self):
        pass

    def tearDown(self):
        try:
            os.remove(self.path_db)
        except FileNotFoundError:
            pass

    def test_isTables(self):
        db = DataBase(self.path_db)
        self.assertTrue(db.is_table('companies'))

    def test_createTables_nothing_should_happen(self):
        db = DataBase(self.path_db)
        db.database_1_00()

    def test_insert(self):
        db = DataBase(self.path_db)
        db.insert(data_in)

    def test_insert_neg(self):
        db = DataBase(self.path_db)
        db.insert(data_in)
        try:
            db.insert(data_in)
        except sqlite3.IntegrityError:
            pass

    def test_getRecord(self):
         db = DataBase(self.path_db)

         self.assertEqual(None, db.getRecord('5261040828'))

         db.insert(data_in)
         self.assertEqual(data_in, db.getRecord('5261040828'))

    def test_update(self):
         db = DataBase(self.path_db)
         db.insert(data_in)
         self.assertEqual(data_in, db.getRecord('5261040828'))
         
         #to test every filed
         vec = [
                 ('regon', '00123456'),
                 ('companyname', 'the boring company'),
                 ('address', 'space 1'),
                 ('postcode', '01000'),
                 ('city', 'Marse One'),
                 ('state', 'Commiefornia'),
                 ('refere', 'Grzegorze Brzęczyszczykiewicz'),
                ]

         for v in vec:
            data_in[v[0]] = v[1]
            self.assertNotEqual(data_in, db.getRecord('5261040828'))
         
            db.update(data_in)
            self.assertEqual(data_in, db.getRecord('5261040828'))

    def test_version_to_db_format(self):
        self.assertEqual(3232235777, DataBase.version_to_db_format(self=None, version='192.168.1.1'))
        self.assertEqual(256, DataBase.version_to_db_format(self=None, version='1.00'))
        self.assertEqual(266, DataBase.version_to_db_format(self=None, version='1.10'))
        self.assertEqual(286, DataBase.version_to_db_format(self=None, version='1.30'))
        self.assertEqual(65537, DataBase.version_to_db_format(self=None, version='1.00.1'))

    def test_version_from_db(self):
        self.assertEqual('192.168.1.1', DataBase.version_from_db_format(self=None, version=3232235777))
        self.assertEqual('1.00', DataBase.version_from_db_format(self=None, version=256))
        self.assertEqual('1.10', DataBase.version_from_db_format(self=None, version=266))
        self.assertEqual('1.30', DataBase.version_from_db_format(self=None, version=286))
        self.assertEqual('1.00.1', DataBase.version_from_db_format(self=None, version=65537))

    def test_db_version_1_00_migration(self):
         db = DataBase(self.path_db)
         self.assertEqual('1.00', db.get_version())
