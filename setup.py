#! /usr/bin/env python3
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

from setuptools import setup, find_packages
from os.path import join, dirname
from os import linesep


def get_description():
    def readfile(fname):
        return open(join(dirname(__file__), fname)).read()
    description = ''
    for fname in ('README.md', 'CONTRIBUTORS', 'LICENSE'):
        description += readfile(fname) + linesep + linesep
    return description


setup(
        name='AutoInvoice',
        version='1.3.0',
        author='Łukasz Buśko',
        author_email='busko.lukasz@pm.me',
        description='Invoice template generator, with plugins for downloading business clients information basin on tax payer id',
        license='GPL',
        keywords='invoice invoices latex generator',
        url='github.com/str0g/AutoInvoice',
        packages=find_packages(
            exclude=['tests']),
        long_description=get_description(),
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Programing Language :: Python 3.7',
            'Topic :: Utilities',
            'License :: GPL License',
        ],
        install_requires=[
            'RegonAPI==1.1.1',
            'litex.regon==1.0.5',
            'requests==2.26.0',
            'qrcode==7.3.1',
            'pillow==9.0.0',
            'opencv-python==4.5.3.56'
        ],
        include_package_data=True,
        test_suite='tests',
        python_requires='>=3.6'
)
