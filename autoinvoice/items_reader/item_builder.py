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

from decimal import Decimal
from os import linesep


class ItemBuilder:
    def __init__(self, input: dict):
        self.item_pattern = input['pattern']
        self.subtotal = Decimal(0)
        self.total = Decimal(0)
        self.items = ''
        for item in input['items']:
            tax = item['tax']
            amount = Decimal(item['amount'])
            amount_with_tax = amount * Decimal('1.{}'.format(tax))

            self.subtotal += amount
            self.total += amount_with_tax
            self.items += self.item_pattern.format(**{
                'description': item['description'],
                'amount': amount.quantize(Decimal('1.00')),
                'tax': tax,
                'total': amount_with_tax.quantize(Decimal('1.00'))
            }) + linesep
        self.tax = self.total - self.subtotal

    def __call__(self) -> dict:
        return {
            'items': self.items,
            'subtotal': str(self.subtotal.quantize(Decimal('1.00'))),
            'tax': str(self.tax.quantize(Decimal('1.00'))),
            'total': str(self.total.quantize(Decimal('1.00')))
        }
