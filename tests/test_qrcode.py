# -*- coding: utf-8 -*-

#################################################################################
#    Autoinvoice is a program to automate invoicing process                     #
#    Copyright (C) 2020  Łukasz Buśko                                           #
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
import base64
import os
from decimal import Decimal
from pathlib import Path
from shutil import copyfile, rmtree

import cv2
import numpy

from .dummy import Dummy, get_dummy
from autoinvoice.qrcode_generator.plugins.zbp2d_std import QRCode_zbp2d
from autoinvoice.qrcode_generator.qrmanager import qrmanager
from .cmdline_creator import CmdlineCreator

template = 'tests/data/template_qrcode.tex'
config = 'tests/data/config_qrcode_zbp2d'
path_json = 'tests/data/items2.json'


class TestGetQRCode_simple(unittest.TestCase):
    def setUp(self):
        self.dummy = Dummy()
        self.dummy.values.taxpayerid = 5222680297
        setattr(self.dummy.values, 'QRCode', get_dummy())
        setattr(self.dummy.values.QRCode, 'accountnumber', '93114020040000320300621961')
        setattr(self.dummy.values.QRCode, 'country_iso', 'PL')

        amount = Decimal(666.71).quantize(Decimal('1.00'))
        self.default_data = {
            'invoice_number': '01/12/2020',
            'companyname': 'GUNS4HIRE',
            'total': str(amount)
        }

        self.database_path = '/tmp/.autoinvoice'
        self.database = '{}/dbase.db'.format(self.database_path)

    def tearDown(self):
        rmtree(self.database_path, ignore_errors=True)

    def test_qrcode_encode_decode(self):
        cmp_data = self.default_data.copy()
        cmp_data['total'] = cmp_data['total'].replace(',','')
        cmp_str = '5222680297|PL|93114020040000320300621961|66671|GUNS4HIRE|01/12/2020|||'

        qr = QRCode_zbp2d(self.dummy.values, cmp_data)()

        self.assertIsInstance(qr, dict)
        self.assertEqual(len(qr), 1)
        self.assertIsInstance([key for key in qr.keys()][0], str)
        self.assertIsInstance([value for value in qr.values()][0], bytes)
        #
        np = numpy.asarray(bytearray(base64.b64decode(qr['qrcode'])), dtype=numpy.uint8)
        img = cv2.imdecode(np, cv2.IMREAD_UNCHANGED)
        #
        detector = cv2.QRCodeDetector()
        data, bbox, straight_qrcode = detector.detectAndDecode(img)
        self.assertEqual(data, cmp_str)

    def test_plugin(self):
        setattr(self.dummy.values, 'qrcode_generator', 'zbp2d_std')
        plugin = qrmanager(self.dummy.values)
        self.assertIsNotNone(plugin)
        self.assertEqual(plugin.__name__, QRCode_zbp2d.__name__)

    def test_template(self):
        Path(self.database_path).mkdir(exist_ok=True)
        os.makedirs('{}/202012/01_tmp_dir'.format(self.database_path))
        copyfile('tests/data/dbase.db', self.database)
        path_config = '{}/{}'.format(self.database_path, 'config')
        test_template = '{}/{}'.format(self.database_path, 'template.tex')
        copyfile(config, path_config)
        copyfile(template, test_template)

        cc = CmdlineCreator(
            {'configuration': path_config, 'generate': ['5261040828'], 'verbose': False, 'items': path_json},
            {'-d': self.database},
        )

        code, out = cc.run()
        self.assertEqual(code, 0)
