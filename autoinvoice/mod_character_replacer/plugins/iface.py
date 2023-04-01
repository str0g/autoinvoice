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

from autoinvoice.common import pure_virtual


class ICharacterReplacer:
    CHARACTER_TO_REPLACE = ''

    def __call__(self, _dict: dict):
        if isinstance(self.CHARACTER_TO_REPLACE, str):
            replace = list(self.CHARACTER_TO_REPLACE)
        else:
            replace = self.CHARACTER_TO_REPLACE

        def replacer(_dict: dict, key: str):
            _list = list(_dict[key])
            return {
                key: ''.join([f'\\{c}' if c in replace else c for c in _list])
            }

        if _dict.get('invoice_number'):
            _dict.update(replacer(_dict, 'invoice_number'))
        _dict.update(replacer(_dict, 'ref_email'))
        _dict.update(replacer(_dict, 'ref_companyname'))
        _dict.update(replacer(_dict, 'ref_address'))
        _dict.update(replacer(_dict, 'ref_city'))
        _dict.update(replacer(_dict, 'address'))
        _dict.update(replacer(_dict, 'city'))
        _dict.update(replacer(_dict, 'customername'))

@pure_virtual
def get() -> object:
    # Suppose to return class not allocation
    return ICharacterReplacer
