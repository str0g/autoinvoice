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


from io import BytesIO
import base64

from autoinvoice import configs
import qrcode

from .iface import IQRCode


class Zbp2d(IQRCode):
    """
    Done with
    https://zbp.pl/public/repozytorium/dla_bankow/rady_i_komitety/bankowosc_elektroczniczna/rada_bankowosc_elektr/zadania/2013.12.03_-_Rekomendacja_-_Standard_2D.pdf
    required:
    [Plugins]
    invoice_numbering = <plugin of choice>
    [zbp2d]
    country_iso = <Country ISO code as two, three letters>
    """
    def __init__(self, data: dict):
        super(IQRCode, self).__init__()

        amount = data['total'].replace('.', '')
        companyname = data['ref_companyname']
        invoice_number = data['invoice_number']
        taxpayerid = configs.config.get('Refere', 'taxpayerid')
        account_number = configs.config.get('Refere', 'account_number').replace(' ', '')
        country_iso = configs.config.get('zbp2d', 'country_iso')
        #
        if len(str(taxpayerid)) > 10:
            raise ValueError('to long taxpayerid')
        _len = len(country_iso)
        if _len < 2 or 3 < _len:
            raise ValueError(f'Country code should be 2 characters wide {country_iso}')
        _len = len(account_number)
        if _len < 22 or 26 < _len:
            raise ValueError(f'range 22 to 26 {account_number}')
        _len = len(invoice_number)
        if len(invoice_number) > 32:
            raise ValueError('to long invoice id')

        self.to_qrcode = f"\
{taxpayerid}|\
{country_iso}|\
{account_number}|\
{amount}|\
{companyname}|\
{invoice_number}|\
|\
|"


def get():
    return Zbp2d

