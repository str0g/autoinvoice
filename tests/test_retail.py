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

from .cmdline_creator import CmdlineCreator

config = 'tests/data/configs/retail.ini'
items = 'tests/data/items/items7.json'


class TestGetQRCode_simple(unittest.TestCase):
    exp = '''\
\\documentclass[polish]{article}

\\usepackage{polski}
\\usepackage[utf8]{inputenc}
\\usepackage{fullpage}
\\usepackage[polish]{polishinvoice}
\\usepackage{bookmark}

\\setdetailedinvoice{true}

\\pagestyle{empty}
\\setinvoicetitle{Faktura}

\\setname{GUNS4HIRE ŁUKASZ BUŚKO}
\\setourref{Łukasz Buśko}
\\setaddress{ul. Lajosa Kossutha 12 lok. 48 \\\\ 01-315 Warszawa}
\\setcompanyid{5222680297}
\\setaccountnumber{93 1140 2004 0000 3203 0062 1961}
\\setdeadline{8}
\\setinvoicenumber{DummyStatic}

\\setreceivername{Jan Brzechwa}
\\setreceiveraddress{ul. Brzechwy 42 \\\\ 66-666 Żmerynka}

\\additem {B&T SPC-9 Magwell} {1.00} {121.95} {121.95 PLN} {23} {150.00 PLN}

\\setsubtotal{121.95 PLN}
\\setvat{28.05 PLN}
\\settotal{150.00 PLN}

\\setinvoicedate{08 maj 2023}
\\overridedateofissue{08.05.2023}


\\begin{document}

\\makeinvoice

\\end{document}

'''

    def test_template_phone(self):
        cc = CmdlineCreator(
            {'configuration': config, 'generate': ['+48189807150'], 'verbose': False, 'items': items},
        )

        code, out = cc.run()
        self.assertEqual(code, 0)

        self.maxDiff = None
        self.assertListEqual(out, self.exp.split('\n'))

    def test_template_email(self):
        cc = CmdlineCreator(
            {'configuration': config, 'generate': ['jan.brzechwa@wieszcze.pl'], 'verbose': False, 'items': items},
        )

        code, out = cc.run()
        self.assertEqual(code, 0)

        self.maxDiff = None
        self.assertListEqual(out, self.exp.split('\n'))
