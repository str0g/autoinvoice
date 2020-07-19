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
from os import path
from ..common import get_plugins
from ..items_reader import plugins


def read_items(options) -> dict:
    """
    Plugin should be build with naming concept read_[extension] and placed inside plugins folder
    read_json is reference file
    """
    plugins_list = get_plugins(plugins)
    if not options.items:
        return {}

    ext = path.splitext(options.items)[1][1:]
    key = 'autoinvoice.items_reader.plugins.read_{}'.format(ext)

    return plugins_list[key].get()(options.items)()
