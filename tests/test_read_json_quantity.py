import unittest
import os
from pathlib import Path
from shutil import copyfile, rmtree

from autoinvoice.items_reader.read_items import read_items

from .dummy import Dummy
from .cmdline_creator import CmdlineCreator

template = 'tests/data/template_read_json.tex'
config = 'tests/data/config_read_json'


class TestReadJson(unittest.TestCase):
    def setUp(self):
        self.dummy = Dummy()

        self.database_path = '/tmp/.autoinvoice'
        self.database = '{}/dbase.db'.format(self.database_path)

    def tearDown(self):
        rmtree(self.database_path, ignore_errors=True)

    def test_read_json(self):
        paths = ['tests/data/items3.json', 'tests/data/items4.json']
        dicts = [{
            'items': '\\additem {Invoice for programing A} {16000.00 PLN} {23} {19680.00 PLN}\n'
                     '\\additem {Invoice for programing B} {23080.96 PLN} {23} {28389.58 PLN}\n'
                     '\\additem {Invoice for firearms training} {304.00 PLN} {23} {373.92 PLN}\n',
            'subtotal': '39384.96',
            'tax': '9058.54',
            'total': '48443.50'
                },
                {
            'items': '\\additem {Invoice for programing A} {160.00} {100.00} {16000.00 PLN} {23} {19680.00 PLN}\n'
                     '\\additem {Invoice for programing B} {184.00} {125.44} {23080.96 PLN} {23} {28389.58 PLN}\n'
                     '\\additem {Invoice for firearms training} {1.00} {304.00} {304.00 PLN} {23} {373.92 PLN}\n',
            'subtotal': '39384.96',
            'tax': '9058.54',
            'total': '48443.50'
                }]
        for index, path in enumerate(paths):
            self.dummy.values.items = path
            out = read_items(self.dummy.values)
            self.assertDictEqual(out, dicts[index])

    def test_read_json_neg(self):
        return
        # @TODO
        self.failureException(read_items(self.dummy.values))
        self.dummy.values.items = 'tests/data/items1.csv'
        with self.assertRaises(KeyError):
            read_items(self.dummy.values)

    def test_template(self):
        path_json = 'tests/data/items3.json'
        Path(self.database_path).mkdir(exist_ok=True)
        os.makedirs('{}/202006/03_tmp_dir'.format(self.database_path))
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
\\setemail{guns4hire@pm.me}
\\setaccountnumber{04 1140 2004 0000 3102 7864 4964}
\\setdeadline{10}
\\setinvoicenumber{/repos}

\\setreceivername{GŁÓWNY URZĄD STATYSTYCZNY}
\\setreceiveraddress{ul. Test-Krucza 208 \\\\ 00-925 Warszawa}
\\setreceivercompanyid{5261040828}

\\additem {Invoice for programing A} {16000.00 PLN} {23} {19680.00 PLN}
\\additem {Invoice for programing B} {23080.96 PLN} {23} {28389.58 PLN}
\\additem {Invoice for firearms training} {304.00 PLN} {23} {373.92 PLN}

\\setsubtotal{39384.96 PLN}
\\setvat{9058.54 PLN}
\\settotal{48443.50 PLN}
\\setinvoicedate{19 lipiec 2020}
\\overridedateofissue{19.07.2020}

\\begin{document}

\\makeinvoice

\\end{document}\
'''

        exp = self.expected_output.format(LaTeX_U).split('\n')
        for i in range(len(out)):
            if out[i] != exp[i]:
                print(out[i], '<=>', exp[i])
            self.assertEqual(out[i], exp[i])

    def test_template_with_quantity(self):
        path_json = 'tests/data/items4.json'
        Path(self.database_path).mkdir(exist_ok=True)
        os.makedirs('{}/202006/03_tmp_dir'.format(self.database_path))
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
\\setemail{guns4hire@pm.me}
\\setaccountnumber{04 1140 2004 0000 3102 7864 4964}
\\setdeadline{10}
\\setinvoicenumber{/repos}

\\setreceivername{GŁÓWNY URZĄD STATYSTYCZNY}
\\setreceiveraddress{ul. Test-Krucza 208 \\\\ 00-925 Warszawa}
\\setreceivercompanyid{5261040828}

\\additem {Invoice for programing A} {160.00} {100.00} {16000.00 PLN} {23} {19680.00 PLN}
\\additem {Invoice for programing B} {184.00} {125.44} {23080.96 PLN} {23} {28389.58 PLN}
\\additem {Invoice for firearms training} {1.00} {304.00} {304.00 PLN} {23} {373.92 PLN}

\\setsubtotal{39384.96 PLN}
\\setvat{9058.54 PLN}
\\settotal{48443.50 PLN}
\\setinvoicedate{19 lipiec 2020}
\\overridedateofissue{19.07.2020}

\\begin{document}

\\makeinvoice

\\end{document}\
'''

        exp = self.expected_output.format(LaTeX_U).split('\n')
        for i in range(len(out)):
            if out[i] != exp[i]:
                print(out[i], '<=>', exp[i])
            self.assertEqual(out[i], exp[i])
