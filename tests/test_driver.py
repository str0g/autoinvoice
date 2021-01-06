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
from pathlib import Path
from shutil import copyfile
from os import remove
import filecmp

from autoinvoice.driver import Driver
from autoinvoice.cmdline import Options


class TestDriver(unittest.TestCase):
    def setUp(self):
        self.database_path = '/tmp/.autoinvoice'
        Path(self.database_path).mkdir(exist_ok=True)
        self.database = '{}/dbase.db'.format(self.database_path)
        copyfile('tests/data/dbase.db', self.database)

    def tearDown(self):
        remove(self.database)
        Path(self.database_path).rmdir()

    def test_generateInvoiceTemplate(self):
        exp = '''\
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
\\setemail{guns4hire@pm.me}
\\setaccountnumber{04 1140 2004 0000 3102 7864 4964}
\\setdeadline{10}
\\setinvoicenumber{3/201908}

\\setreceivername{GŁÓWNY URZĄD STATYSTYCZNY}
\\setreceiveraddress{ul. Test-Krucza 208 \\\\ 00-925 Warszawa}
\\setreceivercompanyid{5261040828}

\\additem{Event strzelecki}{178.86 PLN}{23}{220.01 PLN}
\\setsubtotal{178.86 PLN}
\\setvat{41.14 PLN}
\\settotal{220.01 PLN}
\\setinvoicedate{23 sierpnia 2019}
\\overridedateofissue{23.08.2019}

\\begin{document}

\\makeinvoice

\\end{document}
'''

        options = Options()
        options.database = self.database
        options.taxpayerid = '5222680297'
        options.template = 'tests/data/template1.tex'
        setattr(options, 'register', 'apiregon')
        setattr(options, 'invoice_numbering', '')
        setattr(options, 'items', None)
        setattr(options, 'qrcode_generator', '')
        taxpayerid = '5261040828'

        driver = Driver(options)
        out = driver.generateInvoiceTemplete(taxpayerid)
        self.assertEqual(out, exp)

    def test_getRecord(self):
        # with db test and pre steps...
        #driver = Driver()
        # post steps
        pass
