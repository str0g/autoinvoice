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
from .utils import set_default_config, reload_configuration_to_defaults
from .cmdline_creator import CmdlineCreator

template = 'tests/data/templates/qrcode.tex'
config = 'tests/data/configs/zbp2d.ini'
items = 'tests/data/items/items1.json'


class TestGetQRCode_simple(unittest.TestCase):
    def setUp(self):

        amount = Decimal(666.71).quantize(Decimal('1.00'))
        self.default_data = {
            'invoice_number': '01/12/2020',
            'ref_companyname': 'GUNS4HIRE',
            'total': str(amount)
        }
        #
        reload_configuration_to_defaults(config)
        configs.config.set('Plugins', 'mod_qrcodes', 'zbp2d')
        if not 'zbp2d' in configs.config.sections():
            configs.config.add_section('zbp2d')
        configs.config.set('zbp2d', 'country_iso', 'PL')

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
        qrbytes = qr['qrcode_zbp2d'].encode('utf-8')
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
        cc = CmdlineCreator(
            {'configuration': config, 'generate': ['5261040828'], 'verbose': False, 'items': items},
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
\\setinvoicenumber{DummyStatic}

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
iVBORw0KGgoAAAANSUhEUgAAAcIAAAHCAQAAAABUY/ToAAADr0lEQVR4nO2cTa7jKhCFTzWWMsTSXUCWgnfQS4ruzmApWcCT8NAS1nkDKP/kpif9EsXJqxolxp/AUqmgTgFC/J2lX38JAkYaaaSRRhpppJHHI6VZB6R+FiTpAIwiSD0gw9hBhlHfGl48WiMPSQaSZAbkcj0R8JMAvrSX0nkSAI4kyT35itEaeUhy1PiS+lmA8UQkadEHGLv6Vg1Vj+rTyA8lQwbkkufqUow1GLmfEsAhRmvkAcju5j8BQtKZkBDXZw/t08jPItWHPAGMANIAoLrP+FUkZFAAV4hx703v9Z1GPp1MIiLSA3LJjusCqP4KGZABc03LHtWnkR9CgnsDfAGZHUkWMHoSS0q2sfhe32nk88jqQ5rbO/3FAjKrh0VfwAhHRizP3us7jXweqR4BVJEIgWXxnBaWEFg2EpL5kJH3SUd+V/HHsenUABjHDvzuAQCzIJ1JGR7Vp5EfQUKlZ0fA76NPdmSEI0J221csDhl5hwychHEUkctVhHE8EcAsdRoDgLoUipitXmbk3uqcxSSOgM8AUDoBZmHqXUH6ncF0LqitIc+vHK2RRyQ3uX2dskJ2bekcfQG5xqF9lm9zmZE35NiB3+e1UE8C44kyVI1RdceQDzFaI49E6ppaFaD6LGpGr62LerRISBaHjFRbNUZ1FQB1yspuKxwBbqcevdd3Gvk8UtdDS5CpEck3nXpdI7VpzKvaaD5kpNo9TXqtcGzU6ei3erb5kJGLcWMZzYdagQxoJVhNziwOGXnHbuplujwqOo3VX5rb18zffMjIra3SkBZUC3QDCLRav+wHqaUP8yEjt7bm9s03dPK6adAQZHOZkbfWXAVuEaHXTfhLbMoqHJGW2xv5B9JPwugnEemXMxx+qvteRfpZELhs+3hQn0Z+BrlZD61/NY93XEWilqt52nrIyL0te+9nITDXvxKuAtZnvnRMPQTh2kFCXg53vNd3Gvk8clvraAXVttWsNoeldU9YHDJyMe5tdRqdy9SlqiN5fdF8yEg1zcsA7BOxTUPIwKaaZj5k5B2yStS5PZQBAJJ0bT9I28fYtOva+p7faeQTyc29HwDgC+TCSeRCrZwlEal3Ej2qTyM/g7y9s6FaEleAsQdS/0+Hduheb3T4r30a+eFkW/ZM9SwZee1qCGqzmt0/ZOSt/bj3A34Sop0N6hBi6QgAEvIXEPLXK0dr5IHJ9d6PAY4i/SwyjKd69rXWOto513JDvmK0Rh6KFLvj3EgjjTTSSCON/J+T/wLW3lOnFLDvxgAAAABJRU5ErkJggg==
\\end{filecontents*}

\\begin{document}
\\immediate\write18{base64 -d qrcode.64 > qrcode.png}

\\makeinvoice

\\end{document}

'''

        self.maxDiff = None
        self.assertListEqual(out, exp.split('\n'))
