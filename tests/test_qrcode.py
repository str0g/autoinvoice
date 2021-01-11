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

from autoinvoice.mod_qrcode.plugins.zbp2d import Zbp2d
from autoinvoice.mod_qrcode.manager import manager
from autoinvoice import configs
from .utils import set_default_config
from .cmdline_creator import CmdlineCreator

template = 'tests/data/template_qrcode.tex'
config = 'tests/data/config_qrcode_zbp2d'
path_json = 'tests/data/items1.json'


class TestGetQRCode_simple(unittest.TestCase):
    def setUp(self):

        amount = Decimal(666.71).quantize(Decimal('1.00'))
        self.default_data = {
            'invoice_number': '01/12/2020',
            'ref_companyname': 'GUNS4HIRE',
            'total': str(amount)
        }

        self.database_path = '/tmp/.autoinvoice'
        self.database = '{}/dbase.db'.format(self.database_path)
        #
        set_default_config()
        configs.config.set('Plugins', 'mod_qrcodes', 'zbp2d')
        if not 'zbp2d' in configs.config.sections():
            configs.config.add_section('zbp2d')
        configs.config.set('zbp2d', 'country_iso', 'PL')


    def tearDown(self):
        rmtree(self.database_path, ignore_errors=True)

    def test_qrcode_encode_decode(self):
        cmp_data = self.default_data.copy()
        cmp_data['total'] = cmp_data['total'].replace(',', '')
        cmp_str = '5222680297|PL|93114020040000320300621961|66671|GUNS4HIRE|01/12/2020|||'

        qr = Zbp2d(cmp_data)()

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
        plugin = manager()
        self.assertListEqual(plugin, [Zbp2d])

    def test_input(self):
        cmp_data = self.default_data.copy()

        configs.config.set('zbp2d', 'country_iso', '')
        with self.assertRaises(ValueError):
            qt = Zbp2d(cmp_data)()
        configs.config.set('zbp2d', 'country_iso', 'PLNX')
        with self.assertRaises(ValueError):
            qt = Zbp2d(cmp_data)()
        configs.config.set('zbp2d', 'country_iso', 'PL')

        configs.config.set('Refere', 'account_number', '012345678901234567891')
        with self.assertRaises(ValueError):
            qt = Zbp2d(cmp_data)()
        configs.config.set('Refere', 'account_number', '012345678901234567891234567')
        with self.assertRaises(ValueError):
            qt = Zbp2d(cmp_data)()
        configs.config.set('Refere', 'account_number', '93114020040000320300621961')

        configs.config.set('Refere', 'taxpayerid', '52226802970')
        with self.assertRaises(ValueError):
            qt = Zbp2d(cmp_data)()

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
\\setaccountnumber{93 1140 2004 0000 3203 0062 1961}
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
iVBORw0KGgoAAAANSUhEUgAAAcIAAAHCAQAAAABUY/ToAAADbklEQVR4nO2cQY7iMBBFf00i9dJIcwCO4txgjtTqI80NkqNwgJGSJVLQn4VdthNYtZoBev5fIAg8JUilql9lJ0Z8TtOPT4KASJEiRYoUKVLk85GW1QOT9UjvgIuZHQAblh42LP6r4cFXK/IpyUiSnAEbcDEgvXTZcE/Hc/pIktySnz+nyG9GLp5fItd8aLIeHBczjkufDnmC+ppzivweZL8/MBkAoPNICn96A7rVvu6cIr83Sc4dOQKwIaxAnAGy5Ka7nFPka5OehwIBLAAQVljkJeUdAzoa0K3EArQDydf6nyLvTk5mTQ8GLG9EPPUpDyHO2WybmdmWfMTVinwqEtwqdWjj5luUlqzR+Fr/U+S9SRsAAItPhd7njrVD4xjOhilNj5SHRO5VMw0QyGSixzQa6sgxrLnfLyMk5SGRt8mLIZ7MgBQ0ZwPC2YClBz8O/pPpSNrw+KsV+URkzkMxFS83RckAzQCALn9bUpXykMgbJD+O2fGYWQ+SZ7MhOeliitLLRetlInfKaWXuCIQVKfukyeLckWNg+8LijJSHRGalGaPF8WyIv3sYAuGt18UYTwYAlsaLVtdhX+x/irwfuc1DxeyUNfo8Y+zSsfROfkjkRtlEh7U4HpRaBjRxxblrvbdiSKTLp9Mr3PHQJ0Wkz4dKXxa5aj4kcqccEaFd0sjpZnZjTf/o0yPFkMhG1fa0VS2s8DKWe7XcnAGKIZE7eR7ykhVZF16rzy77h5SHRF6p8UMspijlITdAeQ0tUH2ZyFvKFQxd6ehrNK1NBfMNjurLRO5VB0I+p85TRI+XkpFmX/pQDIncyKc/a+nB4EPFkO8DauKK6u1FXmk3H/LDtW65nY6Nb1IMiWxUe/tNX1ZX672MFXukWiZyK89DZdCYVj02pgiA78730qcYElnUxlDZb5Zm0kCzDXZHKIZEFnGr7Hh8haMOGnMgBeUhkXv5fAgAynxovOWp6zY1xZDIVk0to1tn1BvK8nQapS+Tpxa5164vy+urmz35HldojbViSGTW9XM/fq094vwTyLtiL4Y4gwYABMpO2df6nyL/IRlPb/kOsumAnHgmM0v2aNLzh0Re6coPwbfBRl8EyS6o7kZTLRN5Tdbnfryz3Dq9mN9lf/Dn603HdUc+4mpFPhVpesa5SJEiRYoUKfI/J/8CVWmhq6yvzDwAAAAASUVORK5CYII=
\\end{filecontents*}

\\begin{document}
\\immediate\write18{base64 -d qrcode.64 > qrcode.png}

\\makeinvoice

\\end{document}

'''
        self.maxDiff = None
        self.assertListEqual(out, exp.split('\n'))
