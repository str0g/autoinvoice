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

from decimal import Decimal, getcontext, ROUND_HALF_UP
from os import linesep


class ItemBuilder:
    def __init__(self, items: dict):
        getcontext().rounding = ROUND_HALF_UP
        self.item_pattern = items['pattern']
        self.subtotal = Decimal(0)
        self.total = Decimal(0)
        self.tax = Decimal(0)
        self.items = ''
        for item in items['items']:
            if 'quantity' in item:
                self.with_quantity(item)
            else:
                self.with_out_quantity(item)
        self.tax = self.total - self.subtotal

    def __call__(self) -> dict:
        return {
            'items': self.items,
            'subtotal': str(self.subtotal.quantize(Decimal('1.00'))),
            'tax': str(self.tax.quantize(Decimal('1.00'))),
            'total': str(self.total.quantize(Decimal('1.00')))
        }

    def with_quantity(self, item: dict):
        tax = item['tax']
        price = Decimal(item['amount']).quantize(Decimal('1.00'))
        quantity = Decimal(item['quantity']).quantize(Decimal('1.00'))
        amount = price * quantity
        amount_with_tax = amount * Decimal('1.{}'.format(tax))

        self.subtotal += amount
        self.total += amount_with_tax
        self.items += self.item_pattern.format(**{
            'description': item['description'],
            'quantity': quantity,
            'price': price,
            'amount': amount.quantize(Decimal('1.00')),
            'tax': tax,
            'total': amount_with_tax.quantize(Decimal('1.00'))
            }) + linesep

    def with_out_quantity(self, item: dict):
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

