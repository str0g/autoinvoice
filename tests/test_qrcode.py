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
from decimal import Decimal
import base64

import cv2
import numpy

from autoinvoice.qrcode import get_qrcode

class TestGetQRCode_simple(unittest.TestCase):
    def test_input(self):
        amount = Decimal(666.71).quantize(Decimal('1.00'))
        data = {
            'ref_accountnumber': '1234567890',
            'invoice_number': '01/12/2020',
            'ref_taxpayerid': '5222680297',
            'ref_companyname': 'GUNS4HIRE',
            'amount': str(amount),
            'country_iso': 'PL'
        }
        cmp_data = data.copy()
        cmp_data['amount'] = cmp_data['amount'].replace(',','')
        cmp_str = '5222680297|PL|1234567890|66671|GUNS4HIRE|01/12/2020|||'
        qr = get_qrcode(data)

        self.assertIsInstance(qr, dict)
        self.assertEqual(len(qr), 1)
        self.assertIsInstance([key for key in qr.keys()][0], str)
        self.assertIsInstance([value for value in qr.values()][0], bytes)
        #
        np = numpy.asarray(bytearray(base64.b64decode(qr['qrcode'])), dtype=numpy.uint8)
        #img = cv2.imdecode(np, cv2.IMREAD_GRAYSCALE)
        #img = cv2.imdecode(np, cv2.IMREAD_COLOR)
        img = cv2.imdecode(np, cv2.IMREAD_UNCHANGED)
        #
        detector = cv2.QRCodeDetector()
        data, bbox, straight_qrcode = detector.detectAndDecode(img)
        self.assertEqual(data, cmp_str)
