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

import tempfile
import os
import subprocess
import shutil

from autoinvoice import configs
from .iface import IBuilder


class PdfLatex(IBuilder):
    def __call__(self, template, filename: str):
        outfile_tex = f'{filename}.tex'
        outfile_pdf = f'{filename}.pdf'
        with tempfile.TemporaryDirectory() as tmpdirname:
            out_tex = os.path.join(tmpdirname, outfile_tex)
            out_pdf = os.path.join(tmpdirname, outfile_pdf)

            with open(out_tex, 'w') as fd:
                fd.write(template)

            try:
                proc = subprocess.run(['pdflatex', '--shell-escape', outfile_tex], stdout=subprocess.PIPE, timeout=1,
                                      cwd=tmpdirname)
                proc.check_returncode()
                self.set_permissions(out_pdf)
                shutil.move(out_pdf, outfile_pdf)
            except subprocess.TimeoutExpired as e:
                print(e)
            except subprocess.CalledProcessError as e:
                print(e)


def get() -> object:
    return PdfLatex
