import unittest
import os
import subprocess
from shutil import copyfile, rmtree
from pathlib import Path
from tempfile import TemporaryDirectory
from autoinvoice.InvoiceNumbering.path_to_number import PathToNumber
from .dummy import Dummy

template='tests/data/template_path_to_number.tex'
config='tests/data/config_path_to_number'

class TestPathToNumber(unittest.TestCase):
    def test_path(self):
        ptn = PathToNumber(Dummy().values)
        self.assertEqual('/repos', ptn.get_invoice_number())

    def test_real_path(self):
        with TemporaryDirectory() as tmpdir:
            pathx = '202006/01'
            path = os.path.join(tmpdir, pathx) 
            os.makedirs(path)
            os.chdir(path)
            ptn = PathToNumber(Dummy().values)
            self.assertEqual('01/202006', ptn.get_invoice_number())

    def test_real_path_desc(self):
        with TemporaryDirectory() as tmpdir:
            pathx = '202006/02_somestrings'
            path = os.path.join(tmpdir, pathx) 
            os.makedirs(path)
            os.chdir(path)
            ptn = PathToNumber(Dummy().values)
            self.assertEqual('02/202006', ptn.get_invoice_number())

    def setUp(self):
        self.database_path = '/tmp/.autoinvoice'
        self.database = '{}/dbase.db'.format(self.database_path)

    def test_feel_template(self):
        Path(self.database_path).mkdir(exist_ok=True)
        os.makedirs('{}/202006/03_tmp_dir'.format(self.database_path))
        copyfile('tests/data/dbase.db', self.database)
        config_path_to_number = '{}/{}'.format(self.database_path, 'config')
        test_template = '{}/{}'.format(self.database_path, 'template.tex')
        copyfile(config, config_path_to_number)
        copyfile(template, test_template)
        cmdline_input = ['python3', '-m', 'autoinvoice', '-c', config_path_to_number, '-d', self.database, '-g', '5261040828']

        opt_parser_output = {'generate': ['5261040828'], 'update': None, 'configuration': config_path_to_number,
                'database': self.database, 'template': test_template, 'output' : None,
                'taxpayerid': '5222680297', 'verbouse': True, 'name' : 'Łukasz Buśko', 'url' : '' , 'key' : '', 'register' : 'PL', 'invoice_numbering' : 'path_to_number'}

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
\\setemail{guns4hire@pm.me}
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

        with subprocess.Popen(cmdline_input, stdout=subprocess.PIPE) as proc:
            out = proc.stdout.read().decode('utf-8').split('\n')
        self.assertEqual(proc.returncode, 0)

        exp = self.expected_output.format(LaTeX_U).split('\n')
        for i in range(len(out)):
            if out[i] != exp[i]:
                print(out[i], '<=>', exp[i])
            self.assertEqual(out[i], exp[i])

    def tearDown(self):
        rmtree(self.database_path, ignore_errors=True)


