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
from shutil import copyfile
from os import remove
from os.path import expanduser
from pathlib import Path
import filecmp
import sys

from .dummy import Dummy
from .configuration_creator import ConfigurationCreator
from .cmdline_creator import CmdlineCreator
from .utils import set_default_config, default_configs_string, reload_configuration_to_defaults
from autoinvoice import configs

test_config = 'tests/data/config'
test_config_apiregon = 'tests/data/config_apiregon'
test_template = 'tests/data/template1.tex'
test_text_tex = 'tests/data/text-{}.tex'

class TestOptions(unittest.TestCase):
    def test_tax_ref(self):
        inputx = ['12345', 'name surename']
        parser = Dummy()
        configs.tax_ref(None, None, inputx, parser)

        self.assertEqual(inputx[0], parser.values.taxpayerid)
        self.assertEqual(inputx[1], parser.values.name)

    def test_tax_ref_negative(self):
        inputx = ['12345a', 'name surename']
        parser = Dummy()
        with self.assertRaises(ValueError):
            configs.tax_ref(None, None, inputx, parser)

    def test_options(self):
        if '--verbose' in sys.argv:
            sys.argv.remove('--verbose')
        reload_configuration_to_defaults()
        default = {'generate': None, 'update': None, 'configuration': 'does-not-exist',
                'database': None, 'template': None, 'output': None, 'taxpayerid': None, 'items': None, 'verbose': False}

        self.assertDictEqual(configs.options.__dict__, default)


class TestConfiguration(unittest.TestCase):
    def setUp(self):
        reload_configuration_to_defaults()
        set_default_config()

    def test_default(self):
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

        sys.argv.append('--verbose')

        exp = default_configs_string.split('\n')[:-2]
        exp.append('verbose = True')
        exp.append('')
        exp.append('')

        with RedirectedStdout() as stream:
            configs.set_configuration()
            out = str(stream).split('\n')
            self.assertListEqual(out, exp)


class TestInputValidation(unittest.TestCase):
    def setUp(self):
        self.database_path = '/tmp/.autoinvoice'
        Path(self.database_path).mkdir(exist_ok=True)
        self.database = '{}/dbase.db'.format(self.database_path)
        copyfile('tests/data/dbase.db', self.database)

        self.default_config_output = ConfigurationCreator().get_configuration()

        self.expected_output ='''\
{}

{}
'''
#CompletedProcess(args={}, returncode=0)''' @TODO Remove me

        self.custom_config_output = ConfigurationCreator(
            {'template': test_template, 'name': 'Łukasz Buśko',
             'taxpayerid': '5222680297', 'database': '/tmp/.autoinvoice/dbase.db', 'verbose': True}
        ).get_configuration()

    def tearDown(self):
        remove(self.database)
        Path(self.database_path).rmdir()

    def test_default_values(self):
        cc = CmdlineCreator(
            {'configuration': 'this-file-does-not-exist',
             'template': test_template,
              },
            {'-d': self.database}
        )
        custom_config_output = ConfigurationCreator({
            'database': self.database,
            'template': test_template,
            'register': 'apiregon2',
            'verbose': True,
        }).get_configuration()

        code, out = cc.run()
        self.assertEqual(code, 0)

        exp = self.expected_output.format(custom_config_output,
        cc.command_output(), cc.command_line_input()).split('\n')

        self.maxDiff = None
        self.assertListEqual(out, exp)

    def test_override_default_values(self):
        cc = CmdlineCreator(
            {
                'configuration': test_config,
                'template': test_template,
                'taxpayerid': '5222680297',
                'name': 'Łukasz Buśko'
            },
            {'-d': self.database}
        )

        code, out = cc.run()
        self.assertEqual(code, 0)

        exp = self.expected_output.format(self.custom_config_output, cc.command_output(),
        cc.command_line_input()).split('\n')

        self.assertListEqual(out, exp)

    def test_update(self):
        tab = [5261044039, 5261044039]

        input = {
            'template': test_template, 'name': 'Łukasz Buśko',
            'key': 'abcde12345abcde12345', 'taxpayerid': '5222680297',
            'url': 'https://wyszukiwarkaregontest.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc'
        }
        input_config = {'database': self.database, 'verbose': True}
        input_config.update(input)

        custom_config_output = ConfigurationCreator(input_config).get_configuration()

        input_cmdline = {'configuration': test_config_apiregon, 'update': tab}
        cc = CmdlineCreator(input_cmdline, {'-u': tab, '-d': self.database})

        code, out = cc.run()

        self.assertEqual(code, 0)

        exp = self.expected_output.format(custom_config_output, cc.command_output(),
        cc.command_line_input()).split('\n')

        self.assertListEqual(out, exp)

    def test_new(self):
        tab = ['5261040828', '5261044039']

        cc = CmdlineCreator(
            {'configuration': test_config, 'generate': tab,
              'taxpayerid': '5222680297', 'name': 'Łukasz Buśko', 'template': test_template,
              },
            {'-d': self.database}
        )

        code, out = cc.run()

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
\\setemail{lukasz.busko@guns4hire.cc}
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
\\setemail{lukasz.busko@guns4hire.cc}
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
        self.assertEqual(code, 0)

        _taxpayer = {'taxpayerid': '5222680297', 'regon': '382921340', 'companyname': 'GUNS4HIRE ŁUKASZ BUŚKO', 'state': 'MAZOWIECKIE', 'address': 'ul. Lajosa Kossutha 12 lok. 48', 'postcode': '01-315', 'city': 'Warszawa', 'refere': 'Łukasz Buśko'}

        _stats = {'taxpayerid': tab[0], 'regon': '000331501', 'companyname': 'GŁÓWNY URZĄD STATYSTYCZNY', 'state': 'MAZOWIECKIE', 'address': 'ul. Test-Krucza 208', 'postcode': '00-925', 'city': 'Warszawa', 'refere': '@TODO'}

        exp ='''\
{}

{}
{}
{}

{}
{}

'''.format(self.custom_config_output, cc.command_output(), _taxpayer,
        LaTeX_U, _taxpayer, LaTeX_S).split('\n')

        self.maxDiff = None
        self.assertListEqual(out, exp)

    def test_output(self):
        tab = ['5261040828']
        output = '/tmp/text.tex'

        cc = CmdlineCreator(
            { 'configuration': test_config, 'generate': tab, 'output': output,
              'taxpayerid': '5222680297', 'name': 'Łukasz Buśko', 'template': test_template,
              },
            { '-d': self.database }
        )

        code, out = cc.run()
        self.assertEqual(code, 0)

        #_taxpayer = {'taxpayerid': '5261040828', 'regon': '000331501', 'companyname': 'GŁÓWNY URZĄD STATYSTYCZNY', 'state': 'MAZOWIECKIE', 'address': 'ul. Test-Krucza 208', 'postcode': '00-925', 'city': 'Warszawa', 'refere': '@TODO'}
        _taxpayer = {'taxpayerid': '5222680297', 'regon': '382921340', 'companyname': 'GUNS4HIRE ŁUKASZ BUŚKO', 'state': 'MAZOWIECKIE', 'address': 'ul. Lajosa Kossutha 12 lok. 48', 'postcode': '01-315', 'city': 'Warszawa', 'refere': 'Łukasz Buśko'}

        exp = '''\
{}

{}
{}
'''.format(self.custom_config_output, cc.command_output(), _taxpayer).split('\n')
        self.maxDiff = None
        self.assertListEqual(out, exp)

        filex = '/tmp/text-{}.tex'.format(tab[0])
        self.assertTrue(filecmp.cmp(test_text_tex.format(tab[0]), filex))
        remove(filex)
