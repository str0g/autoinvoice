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
import sys

from autoinvoice.mod_builder.manager import manager
from autoinvoice.mod_builder.plugins.pdflatex_subprocess import PdfLatex
from autoinvoice import configs
from autoinvoice.driver import Driver
from .utils import reload_configuration_to_defaults, use_temporary_directory

template = 'tests/data/templates/qrcode.tex'
config = 'tests/data/configs/pdflatex_subprocess.ini'
items = 'tests/data/items/items1.json'


class TestGetPdfLatexSubprocess(unittest.TestCase):
    def setUp(self) -> None:
        reload_configuration_to_defaults(config)

    def test_plugin(self):
        configs.config.set('Plugins', 'mod_builder', 'pdflatex_subprocess')
        plugin = manager()
        self.assertEqual(plugin, PdfLatex)

    def test_plugin_nobuild_option(self):
        configs.config.set('Plugins', 'mod_builder', 'pdflatex_subprocess')
        configs.config.set('Options', 'nobuilder', 'True')
        plugin = manager()
        self.assertIsNone(plugin)

    @use_temporary_directory
    def test_build(self, *args, **kwargs):
        tmpdirname = kwargs.get('tmpdirname')
        sys.argv.append('--template')
        sys.argv.append(template)
        sys.argv.append('--items')
        sys.argv.append(items)

        configs.reload_configuraiton()

        driver = Driver()
        driver.fill_invoice_template("5222680297")

        self.assertIsNotNone(driver.output())
