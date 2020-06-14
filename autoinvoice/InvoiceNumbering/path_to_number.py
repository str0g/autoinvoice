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
from os import getcwd, sep
from .IInvoiceNumber import IInvoiceNumber

class PathToNumber(IInvoiceNumber):
    def get_invoice_number(self) -> str:
        """
        Get current and top directory and format form it string
        current/top
        """
        path = getcwd().split(sep)[-2:]
        if path[1].isnumeric():
            number = path[1]
        else:
            for i, s in enumerate(path[1]):
                if not s.isnumeric():
                    break
            number = path[1][:i]

        return '{}/{}'.format(number, path[0])
