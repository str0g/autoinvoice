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

from autoinvoice.mod_items_reader.manager import manager
from .utils import reload_configuration_to_defaults
from .cmdline_creator import CmdlineCreator
from autoinvoice import configs

template = 'tests/data/templates/read_json.tex'
config = 'tests/data/configs/read_json.json'
items = 'tests/data/items2.json'


class TestReadJson(unittest.TestCase):
    def setUp(self):
        reload_configuration_to_defaults(config)

    def test_read_json(self):
        paths = ['tests/data/items1.json', 'tests/data/items2.json']
        dicts = [{
            'items': '\\additem {item1} {109.50 PLN} {23} {134.69 PLN}\n'
                     '\\additem {next item} {57.00 PLN} {0} {57.00 PLN}\n',
            'subtotal': '166.50',
            'tax': '25.19',
            'total': '191.69'
                },
                {
            'items': '\\additem {Invoice for programing A} {19200.00 PLN} {23} {23616.00 PLN}\n'
                     '\\additem {Invoice for programing B} {4500.00 PLN} {23} {5535.00 PLN}\n'
                     '\\additem {Invoice for firearms training} {304.00 PLN} {23} {373.92 PLN}\n',
            'subtotal': '24004.00',
            'tax': '5520.92',
            'total': '29524.92'
                }]
        for index, path in enumerate(paths):
            configs.config.set('Options', 'items', path)
            out = manager()
            self.assertDictEqual(out, dicts[index])

    def test_read_json_neg(self):
        configs.config.set('Options', 'items', 'tests/data/items1.csv')
        with self.assertRaises(KeyError):
            manager()

    def test_template(self):
        cc = CmdlineCreator(
            {'configuration': config, 'generate': ['5261040828'], 'verbose': False, 'items': items},
        )

        code, out = cc.run()
        self.assertEqual(code, 0)

        self.expected_output = '''\
{}

'''

        LaTeX_U = '''\
\\documentclass[polish]{article}

\\usepackage{polski}
\\usepackage[utf8]{inputenc}
\\usepackage{fullpage}
\\usepackage[polish]{polishinvoice}
\\usepackage{bookmark}

\\pagestyle{empty}
\\setinvoicetitle{Faktura}

\\setname{GUNS4HIRE ŁUKASZ BUŚKO}
\\setourref{Łukasz Buśko}
\\setaddress{ul. Lajosa Kossutha 12 lok. 48 \\\\ 01-315 Warszawa}
\\setcompanyid{5222680297}
\\setphonenumber{+48662152026}
\\setemail{lukasz.busko@guns4hire.cc}
\\setaccountnumber{04 1140 2004 0000 3102 7864 4964}
\\setdeadline{10}
\\setinvoicenumber{DummyStatic}

\\setreceivername{GŁÓWNY URZĄD STATYSTYCZNY}
\\setreceiveraddress{ul. Test-Krucza 208 \\\\ 00-925 Warszawa}
\\setreceivercompanyid{5261040828}

\\additem {Invoice for programing A} {19200.00 PLN} {23} {23616.00 PLN}
\\additem {Invoice for programing B} {4500.00 PLN} {23} {5535.00 PLN}
\\additem {Invoice for firearms training} {304.00 PLN} {23} {373.92 PLN}

\\setsubtotal{24004.00 PLN}
\\setvat{5520.92 PLN}
\\settotal{29524.92 PLN}
\\setinvoicedate{19 lipiec 2020}
\\overridedateofissue{19.07.2020}

\\begin{document}

\\makeinvoice

\\end{document}\
'''

        exp = self.expected_output.format(LaTeX_U).split('\n')
        self.assertListEqual(out, exp)
