import unittest
import os
from pathlib import Path
from shutil import copyfile, rmtree

from autoinvoice.items_reader.read_items import read_items

from .dummy import Dummy
from .cmdline_creator import CmdlineCreator

template = 'tests/data/template_read_json.tex'
config = 'tests/data/config_read_json'
path_json = 'tests/data/items2.json'


class TestReadJson(unittest.TestCase):
    def setUp(self):
        self.dummy = Dummy()

        self.database_path = '/tmp/.autoinvoice'
        self.database = '{}/dbase.db'.format(self.database_path)

    def tearDown(self):
        rmtree(self.database_path, ignore_errors=True)

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
            self.dummy.values.items = path
            out = read_items(self.dummy.values)
            self.assertDictEqual(out, dicts[index])

    def test_read_json_neg(self):
        self.failureException(read_items(self.dummy.values))
        self.dummy.values.items = 'tests/data/items1.csv'
        with self.assertRaises(KeyError):
            read_items(self.dummy.values)

    def test_template(self):
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
        for i in range(len(out)):
            if out[i] != exp[i]:
                print(out[i], '<=>', exp[i])
            self.assertEqual(out[i], exp[i])
