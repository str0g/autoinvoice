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

import os
import stat

from autoinvoice.common import pure_virtual


class IBuilder:
    def set_permissions(self, path: str, permissions=stat.S_IRUSR | stat.S_IWUSR):
        os.chmod(path, permissions)

    @pure_virtual
    def __call__(self, template, filename: str):
        # do some action
        # set_permissions() on output file
        pass


@pure_virtual
def get() -> object:
    # Suppose to return class not allocation
    return IBuilder
