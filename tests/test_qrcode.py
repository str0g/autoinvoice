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
from autoinvoice.qrcode_generator.plugins.zbp2d import Zbp2d
from autoinvoice.qrcode_generator.qrmanager import qrmanager
from .cmdline_creator import CmdlineCreator

template = 'tests/data/template_qrcode.tex'
config = 'tests/data/config_qrcode_zbp2d'
path_json = 'tests/data/items1.json'


class TestGetQRCode_simple(unittest.TestCase):
    def setUp(self):
        self.dummy = Dummy()
        self.dummy.values.taxpayerid = 5222680297
        setattr(self.dummy.values, 'account_number', '93114020040000320300621961')
        setattr(self.dummy.values, 'country_iso', 'PL')

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

        qr = Zbp2d(self.dummy.values, cmp_data)()

        self.assertIsInstance(qr, dict)
        self.assertEqual(len(qr), 1)
        self.assertIsInstance([key for key in qr.keys()][0], str)
        self.assertIsInstance([value for value in qr.values()][0], str)
        #
        qrbytes = qr['qrcode'].encode('utf-8')
        np = numpy.asarray(bytearray(base64.b64decode(qrbytes)), dtype=numpy.uint8)
        img = cv2.imdecode(np, cv2.IMREAD_UNCHANGED)
        #
        detector = cv2.QRCodeDetector()
        data, bbox, straight_qrcode = detector.detectAndDecode(img)
        self.assertEqual(data, cmp_str)

    def test_plugin(self):
        setattr(self.dummy.values, 'qrcode_generator', 'zbp2d')
        plugin = qrmanager(self.dummy.values)
        self.assertIsNotNone(plugin)
        self.assertEqual(plugin.__name__, Zbp2d.__name__)

    def test_input(self):
        cmp_data = self.default_data.copy()

        setattr(self.dummy.values, 'country_iso', '')
        print(len(self.dummy.values.country_iso))
        with self.assertRaises(ValueError):
            qt = Zbp2d(self.dummy.values, cmp_data)()
        setattr(self.dummy.values, 'country_iso', 'PLNX')
        with self.assertRaises(ValueError):
            qt = Zbp2d(self.dummy.values, cmp_data)()
        setattr(self.dummy.values, 'country_iso', 'PL')

        setattr(self.dummy.values, 'account_number', '93114020040000320300621961')
        self.dummy.values.account_number = '012345678901234567891'
        with self.assertRaises(ValueError):
            qt = Zbp2d(self.dummy.values, cmp_data)()
        self.dummy.values.account_number = '012345678901234567891234567'
        with self.assertRaises(ValueError):
            qt = Zbp2d(self.dummy.values, cmp_data)()
        setattr(self.dummy.values, 'account_number', '93114020040000320300621961')

        self.dummy.values.taxpayerid = 52226802970
        with self.assertRaises(ValueError):
            qt = Zbp2d(self.dummy.values, cmp_data)()

    def test_template(self):
        Path(self.database_path).mkdir(exist_ok=True)
        os.makedirs('{}/202012/01_tmp_dir'.format(self.database_path))
        copyfile('tests/data/dbase.db', self.database)
        path_config = '{}/{}'.format(self.database_path, 'config_qrcode_zbp2d')
        test_template = '{}/{}'.format(self.database_path, 'template_qrcode.tex')
        copyfile(config, path_config)
        copyfile(template, test_template)

        cc = CmdlineCreator(
            {'configuration': path_config, 'generate': ['5261040828'], 'verbose': False, 'items': path_json},
            {'-d': self.database},
        )

        code, out = cc.run()
        self.assertEqual(code, 0)
        exp = '''\
% build with pdflatex --shell-escape

\\documentclass[polish]{article}

\\usepackage{polski}
\\usepackage[utf8]{inputenc}
\\usepackage{fullpage}
\\usepackage[polish]{polishinvoice}
\\usepackage{bookmark}
\\usepackage{graphicx}

% must be set in order to embedded image work
\\graphicspath{.}
%

\\pagestyle{empty}
\\setinvoicetitle{Faktura}

\\setname{GUNS4HIRE ŁUKASZ BUŚKO}
\\setourref{Łukasz Buśko}
\\setaddress{ul. Lajosa Kossutha 12 lok. 48 \\\\ 01-315 Warszawa}
\\setcompanyid{5222680297}
\\setphonenumber{+48662152026}
\\setemail{lukasz.busko@guns4hire.cc}
\\setaccountnumber{93114020040000320300621961}
\\setdeadline{10}
\\setinvoicenumber{/repos}

\\setreceivername{GŁÓWNY URZĄD STATYSTYCZNY}
\\setreceiveraddress{ul. Test-Krucza 208 \\\\ 00-925 Warszawa}
\\setreceivercompanyid{5261040828}

\\additem {item1} {109.50 PLN} {23} {134.69 PLN}
\\additem {next item} {57.00 PLN} {0} {57.00 PLN}

\\setsubtotal{166.50 PLN}
\\setvat{25.19 PLN}
\\settotal{191.69 PLN}
\\setinvoicedate{25 grudzień 2020}
\\overridedateofissue{25.12.2020}

\\setwithqrcodes
\\setqrcodebankpayment{qrcode.png}
\\begin{filecontents*}{qrcode.64}
iVBORw0KGgoAAAANSUhEUgAAAcIAAAHCAQAAAABUY/ToAAADd0lEQVR4nO2cX4qkMBCHv1qFflTYA8xR4s2WOdLeQI8yBxjQx4VI7UMSjc4sC7M9dE/vrx5EMR+JUNTfGHM+JtO3D4IgUqRIkSJFihR5f6RlaTHrV7MByt1i6QJLGTXceLUi75IM7u4+g48ALGaEGfz5KQI0DjTu7u5H8harFXmX5LLZl01fxu3uuQcbADNrrzenyMcg29Oz0YFPPUYYwcK8tk43X3NOkY9FnnUIAAPwqX9tmfpXCC92zTlFPhZZdKhzYAFYjGSC6MABt+1tXZD8Wt8p8tPJyczMeiDMjcPSQni5uA3prsUG1pSW3X61Iu+KxI8CXbkEjylN87GLJXXbZPxa3yny88ikQwR3J8wkO7QrDXTu7nPjOenv8mDpkMgiJR5aenx6ii10EVguzmTg05B8l3nwtSX8tBIUfa3vFPl5ZPFlM6Si4phKiZFccuwiyRiNZAMlXybyIMkOpWQeYmt0r9ny0MXWwrziKVcrSZmF8VarFXm/ZKpJT5ZzsBwALRf3Z2uxAdhztZuvVuR9kcUzpSA6e7D8YiZnY5sbq5Iz+TKRRUo8lHtjBI9VclY0Zmu8Kh4S+UayRlRN+aa6lLf7OKRDIk+y14dSFOQeySZobrb6UBmXTZV0SGQlVW7PHvHMxavV42JO/2WHRL4lbaAkYiNgQ5cDoN0Y2ZD829XmFPkoZBU1Jw+2FxVzh6PxbH3Ko+yQyKOc+mU+dp7Tr6omnYY2Xuf7X+s7RX4eeYyVI7nNUVr2ScIMJVqK0iGR75Ep83q2izP1wNQXDzbuQ5dL2ll9pTlFPgp5jIe8SuazfytZWy5Wo7xM5FlOdeqiJaf9Q8VUjUiHRJ5lj4dK/NwcjNG85WWlXCQdEnmUqsYY5qJIObDe7spb1RhFviO1L+v2uy0HKy9OgZJ0SOQmlS8bt858VUrs6oaH7JDId8SPsm/Mz1UhmqrTmo2RdEjkG3I/9yPJ9BTTcQ3u/st8ZLW0jxFW/V8m8iTZ+pSgqD78Y0/1580Oae+HyD+R5dyP/WfXsh+kHBYzpV9cZYdE/oXc937ky5J/oj5sdbzunCIfjAyblkz9vgN2NfvhEaZ+tezp7mK1Iu+AfOfcj+8Rlu/RYc1vg6+tT/2c/hz65zlFPhZJ7Z62gHlrweYOR+d1w0MxtchaTGecixQpUqRIkSL/c/I3VbeHrjSjunsAAAAASUVORK5CYII=
\\end{filecontents*}

\\begin{document}
\\immediate\write18{base64 -d qrcode.64 > qrcode.png}

\\makeinvoice

\\end{document}

'''
        self.assertListEqual(out, exp.split('\n'))
