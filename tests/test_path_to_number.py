import unittest
import os
from shutil import copyfile, rmtree
from pathlib import Path
from tempfile import TemporaryDirectory
#
from autoinvoice.mod_invoice_numbering.plugins.path_to_number import PathToNumber
from autoinvoice import configs
from .cmdline_creator import CmdlineCreator

template = 'tests/data/template_path_to_number.tex'
config = 'tests/data/config_path_to_number'


class TestPathToNumber(unittest.TestCase):
    def setUp(self):
        configs.reload_configuraiton()
        self.database_path = '/tmp/.autoinvoice'
        self.database = '{}/dbase.db'.format(self.database_path)

        configs.config.set('Plugins', 'mod_invoice_numbering', 'path_to_number')
        configs.config.set('Paths', 'database', self.database)

    def tearDown(self):
        rmtree(self.database_path, ignore_errors=True)

    def test_path(self):
        ptn = PathToNumber()
        self.assertEqual('/repos', ptn())

    def test_real_path(self):
        with TemporaryDirectory() as tmpdir:
            pathx = '202006/01'
            path = os.path.join(tmpdir, pathx) 
            os.makedirs(path)
            os.chdir(path)
            ptn = PathToNumber()
            self.assertEqual('01/202006', ptn())

    def test_real_path_desc(self):
        with TemporaryDirectory() as tmpdir:
            pathx = '202006/02_somestrings'
            path = os.path.join(tmpdir, pathx) 
            os.makedirs(path)
            os.chdir(path)
            ptn = PathToNumber()
            self.assertEqual('02/202006', ptn())

    def test_feel_template(self):
        Path(self.database_path).mkdir(exist_ok=True)
        os.makedirs('{}/202006/03_tmp_dir'.format(self.database_path))
        copyfile('tests/data/dbase.db', self.database)
        config_path_to_number = '{}/{}'.format(self.database_path, 'config')
        test_template = '{}/{}'.format(self.database_path, 'template.tex')
        copyfile(config, config_path_to_number)
        copyfile(template, test_template)

        cc = CmdlineCreator(
            {'configuration': config_path_to_number, 'generate': ['5261040828'], 'verbose': False},
            {'-d': self.database}
        )

        code, out = cc.run()
        self.assertEqual(code, 0)

        self.expected_output ='''\
{}

'''

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
\\setinvoicenumber{/repos}

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

        exp = self.expected_output.format(LaTeX_U).split('\n')
        for i in range(len(out)):
            if out[i] != exp[i]:
                print(out[i], '<=>', exp[i])
            self.assertEqual(out[i], exp[i])
