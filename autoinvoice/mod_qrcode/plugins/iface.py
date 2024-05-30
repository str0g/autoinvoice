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

import qrcode

from autoinvoice.common import pure_virtual


class IQRCode:
    def __init__(self):
        self.to_qrcode = ''

    def __call__(self) -> dict:
        qr = qrcode.make(self.to_qrcode)
        io = BytesIO()
        qr.save(io, format='png')
        #qr.save(io, kind='PNG')
        io.seek(0)
        b64 = base64.b64encode(io.getvalue()).decode('utf-8')

        return {f'qrcode_{self.get_name()}': b64}

    @pure_virtual
    def get_name(self):
        return IQRCode.__name__

@pure_virtual
def get() -> IQRCode:
    # Suppose to return class not allocation
    return IQRCode
