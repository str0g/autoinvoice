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

from ..common import get_plugins
from ..mod_qrcode import plugins
from .. import configs


def manager():
    plugins_list = get_plugins(plugins)
    plugins_list_cfg = [configs.config.get('Plugins', 'mod_qrcodes')]
    out = []
    for p in plugins_list_cfg:
        key = 'autoinvoice.mod_qrcode.plugins.{}'.format(p)
        try:
            out.append(plugins_list[key].get())
        except KeyError as e:
            pass
            #print(f'{e}')

    return out