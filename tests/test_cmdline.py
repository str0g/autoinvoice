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
import subprocess
from shutil import copyfile
from os.path import expanduser, isfile
from os import remove
from pathlib import Path
import filecmp

from autoinvoice import cmdline
from .dummy import Dummy
from .configuration_creator import ConfigurationCreator

test_config = 'tests/data/config'
test_config_apiregon = 'tests/data/config_apiregon'
test_template = 'tests/data/template1.tex'
test_text_tex = 'tests/data/text-{}.tex'

class TestOptions(unittest.TestCase):
    def test_tax_ref(self):
        inputx = ['12345', 'name surename']
        parser = Dummy()
        cmdline.tax_ref(None, None, inputx, parser)

        self.assertEqual(inputx[0], parser.values.taxpayerid)
        self.assertEqual(inputx[1], parser.values.name)

    def test_tax_ref_negative(self):
        inputx = ['12345a', 'name surename']
        parser = Dummy()
        with self.assertRaises(ValueError):
            cmdline.tax_ref(None, None, inputx, parser)

    def test_options(self):
        default = {'generate': None, 'update': None, 'configuration': '~/.autoinvoice/config',
                'database': None, 'template': None, 'output': None, 'taxpayerid': None, 'verbose': False}#,
#                'url' : '' , 'key' : '', 'register' : 'PL'}
        options = cmdline.Options()
        self.assertEqual(options, default)

class TestConfiguration(unittest.TestCase):
    def test_default(self):
        import sys
        from io import StringIO

        class RedirectedStdout:
            def __init__(self):
                self._stdout = None
                self._string_io = None

            def __enter__(self):
                self._stdout = sys.stdout
                sys.stdout = self._string_io = StringIO()
                return self

            def __exit__(self, type, value, traceback):
                sys.stdout = self._stdout

            def __str__(self):
                return self._string_io.getvalue()

        exp = (ConfigurationCreator().get_configuration() + '\n' + '\n').split('\n')
        values = Dummy().values
        values.verbose = True
        with RedirectedStdout() as stream:
            cfg = cmdline.Configuration(values)
            out = str(stream).split('\n')
            for i in range(len(exp)):
                self.assertEqual(out[i], exp[i])
            self.assertEqual(len(exp), len(out))


class TestInputValidation(unittest.TestCase):
    def setUp(self):
        self.database_path = '/tmp/.autoinvoice'
        Path(self.database_path).mkdir(exist_ok=True)
        self.database = '{}/dbase.db'.format(self.database_path)
        copyfile('tests/data/dbase.db', self.database)
        self.default_cmdline_input = ['python3', '-m', 'autoinvoice', '-v', '-c', 'this-file-does-not-exist', '-d', self.database]

        self.default_opt_parser_output = {'generate': None, 'update': None, 'configuration': 'this-file-does-not-exist',
                'database': self.database, 'template': '/usr/share/polishinvoice/templates/simple.tex', 'output' : None,
                'taxpayerid': '', 'verbose': True, 'name' : '', 'url' : '' , 'key' : '', 'register' : 'PL', 'invoice_numbering': ''}

        self.default_config_output = ConfigurationCreator().get_configuration()

        self.expected_output ='''\
{}

{}

CompletedProcess(args={}, returncode=0)'''

        self.custom_config_output = ConfigurationCreator(
            {'template': test_template, 'name': 'Łukasz Buśko',
             'taxpayerid': '5222680297', 'database': '/tmp/.autoinvoice/dbase.db'}
        ).get_configuration()

    def tearDown(self):
        remove(self.database)
        Path(self.database_path).rmdir()

    def test_default_values(self):
        with subprocess.Popen(self.default_cmdline_input, stdout=subprocess.PIPE) as proc:
            out = proc.stdout.read().decode('utf-8').split('\n')

        self.assertEqual(proc.returncode, 0)

        exp = self.expected_output.format(self.default_config_output, 
        self.default_opt_parser_output, self.default_cmdline_input).split('\n')

        for i in range(len(out)):
            if out[i] != exp[i]:
                print(out[i], '<=>', exp[i])
            self.assertEqual(out[i], exp[i])

    def test_override_default_values(self):
        custom_cmdline_input =['python3', '-m', 'autoinvoice', '-v', '-c', test_config, '-d', self.database]

        custom_opt_parser_output = {'generate': None, 'update': None, 'configuration': test_config,
                'database': self.database, 'template': test_template, 'output': None,
                'taxpayerid': '5222680297', 'verbose': True, 'name': 'Łukasz Buśko',
                'url': '' , 'key': '', 'register': 'PL', 'invoice_numbering': ''}

        with subprocess.Popen(custom_cmdline_input, stdout=subprocess.PIPE) as proc:
            out = proc.stdout.read().decode('utf-8').split('\n')
        self.assertEqual(proc.returncode, 0)

        exp = self.expected_output.format(self.custom_config_output, custom_opt_parser_output,
        custom_cmdline_input).split('\n')

        for i in range(len(out)):
            if out[i] != exp[i]:
                print(out[i], '<=>', exp[i])
            self.assertEqual(out[i], exp[i])

    def test_update(self):
        tab = [5261044039, 5261044039]

        custom_cmdline_input = ['python3', '-m', 'autoinvoice', '-v', '-c', test_config_apiregon,
                '-u', str(tab[0]), '--update', str(tab[1])]

        self.default_opt_parser_output['configuration'] = test_config_apiregon
        self.default_opt_parser_output['template'] = test_template
        self.default_opt_parser_output['update'] = tab
        self.default_opt_parser_output['url'] = 'https://wyszukiwarkaregontest.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc'
        self.default_opt_parser_output['key'] = 'abcde12345abcde12345'
        self.default_opt_parser_output['taxpayerid'] = '5222680297'
        self.default_opt_parser_output['name'] = 'Łukasz Buśko'
        self.default_opt_parser_output['invoice_numbering'] = ''
        self.maxDiff = None
        custom_config_output = ConfigurationCreator(
            {'template': test_template, 'name': 'Łukasz Buśko', 'key': 'abcde12345abcde12345',
             'taxpayerid': '5222680297', 'database': '/tmp/.autoinvoice/dbase.db',
             'url': 'https://wyszukiwarkaregontest.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc'}
        ).get_configuration()

        with subprocess.Popen(custom_cmdline_input, stdout=subprocess.PIPE) as proc:
            out = proc.stdout.read().decode('utf-8').split('\n')

        self.assertEqual(proc.returncode, 0)

        exp = self.expected_output.format(custom_config_output, self.default_opt_parser_output,
        custom_cmdline_input).split('\n')

        for i in range(len(out)):
            if out[i] != exp[i]:
                print(out[i], '<=>', exp[i])
            self.assertEqual(out[i], exp[i])

    def test_new(self):
        tab = ['5261040828', '5261044039']
        custom_cmdline_input = ['python3', '-m', 'autoinvoice', '-v', '-c', test_config,
                '-g', tab[0], '--generate', tab[1]]

        self.default_opt_parser_output['configuration'] = test_config
        self.default_opt_parser_output['generate'] = tab
        self.default_opt_parser_output['taxpayerid'] = '5222680297'
        self.default_opt_parser_output['name'] = 'Łukasz Buśko'
        self.default_opt_parser_output['template'] = test_template
        self.default_opt_parser_output['generate'] = tab

        LaTeX_U ='''\
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

\\end{document}\
'''

        LaTeX_S ='''\
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

\\setreceivername{SAMSUNG ELECTRONICS POLSKA SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ}
\\setreceiveraddress{ul. Postępu 14 \\\\ 02-676 Warszawa}
\\setreceivercompanyid{5261044039}

\\additem{Event strzelecki}{178.86 PLN}{23}{220.01 PLN}
\\setsubtotal{178.86 PLN}
\\setvat{41.14 PLN}
\\settotal{220.01 PLN}
\\setinvoicedate{23 sierpnia 2019}
\\overridedateofissue{23.08.2019}

\\begin{document}

\\makeinvoice

\\end{document}\
'''
        with subprocess.Popen(custom_cmdline_input, stdout=subprocess.PIPE) as proc:
            out = proc.stdout.read().decode('utf-8').split('\n')

        self.assertEqual(proc.returncode, 0)

        _taxpayer = {'taxpayerid': '5222680297', 'regon': '382921340', 'companyname': 'GUNS4HIRE ŁUKASZ BUŚKO', 'state': 'MAZOWIECKIE', 'address': 'ul. Lajosa Kossutha 12 lok. 48', 'postcode': '01-315', 'city': 'Warszawa', 'refere': 'Łukasz Buśko'}

        _stats = {'taxpayerid': tab[0], 'regon': '000331501', 'companyname': 'GŁÓWNY URZĄD STATYSTYCZNY', 'state': 'MAZOWIECKIE', 'address': 'ul. Test-Krucza 208', 'postcode': '00-925', 'city': 'Warszawa', 'refere': '@TODO'}

        exp ='''\
{}

{}
{}
{}

{}
{}


CompletedProcess(args={}, returncode=0)'''.format(self.custom_config_output, self.default_opt_parser_output,
        _taxpayer, LaTeX_U, _taxpayer, LaTeX_S, self.default_cmdline_input).split('\n')

        for i in range(len(out)):
            if out[i] != exp[i]:
                print(out[i], '<=>', exp[i])
            self.assertEqual(out[i], exp[i])

    def test_output(self):
        tab = ['5261040828']
        output = '/tmp/text.tex'

        custom_cmdline_input = ['python3', '-m', 'autoinvoice', '-v', '-c', test_config, '-g', tab[0], '-o', output]

        self.default_opt_parser_output['configuration'] = test_config
        self.default_opt_parser_output['generate'] = tab
        self.default_opt_parser_output['output'] = output
        self.default_opt_parser_output['taxpayerid'] = '5222680297'
        self.default_opt_parser_output['name'] = 'Łukasz Buśko'
        self.default_opt_parser_output['template'] = test_template

        with subprocess.Popen(custom_cmdline_input, stdout=subprocess.PIPE) as proc:
            out = proc.stdout.read().decode('utf-8').split('\n')

        self.assertEqual(proc.returncode, 0)

        #_taxpayer = {'taxpayerid': '5261040828', 'regon': '000331501', 'companyname': 'GŁÓWNY URZĄD STATYSTYCZNY', 'state': 'MAZOWIECKIE', 'address': 'ul. Test-Krucza 208', 'postcode': '00-925', 'city': 'Warszawa', 'refere': '@TODO'}
        _taxpayer = {'taxpayerid': '5222680297', 'regon': '382921340', 'companyname': 'GUNS4HIRE ŁUKASZ BUŚKO', 'state': 'MAZOWIECKIE', 'address': 'ul. Lajosa Kossutha 12 lok. 48', 'postcode': '01-315', 'city': 'Warszawa', 'refere': 'Łukasz Buśko'}

        exp = '''\
{}

{}
{}

CompletedProcess(args={}, returncode=0)
'''.format(self.custom_config_output, self.default_opt_parser_output, _taxpayer,_taxpayer,
        self.default_cmdline_input).split('\n')

        for i in range(len(out)):
            if out[i] != exp[i]:
                print(out[i], '<=>', exp[i])
            self.assertEqual(out[i], exp[i])
        filex = '/tmp/text-{}.tex'.format(tab[0])
        self.assertTrue(filecmp.cmp(test_text_tex.format(tab[0]), filex))
        remove(filex)
