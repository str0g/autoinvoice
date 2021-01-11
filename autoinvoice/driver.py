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

from pathlib import Path

from . import configs
from .mod_company_register.manager import manager as manager_register
from .mod_company_register.database import DataBase
from .mod_invoice_numbering import manager as manager_invoice_numbering
from .mod_items_reader.manager import manager as manager_items
from .mod_qrcode.manager import manager as manager_qr


class Driver:
    def __init__(self):
        self.database = None
        self.crm = manager_register()
        self.invoice_number = manager_invoice_numbering()
        self.invoice_items = manager_items()
        self.mod_qrcode = manager_qr()
        self.url = configs.config.get('Common', 'url')
        self.key = configs.config.get('Common', 'key')
        self.ref_taxpayerid = configs.config.get('Refere', 'taxpayerid')

        self.database_init()

    def database_init(self):
        database = configs.config.get('Paths', 'database', fallback=None)
        if not database:
            self.db = None
            return
        path = Path(database)
        path.touch(mode=0o640, exist_ok=True)
        self.database = DataBase(database)

    def getRecord(self, taxpayerid):
        record = None
        if self.database:
            record = self.database.getRecord(taxpayerid)
        if not record:
            record = self.crm.getRecords(taxpayerid, self.url, self.key)
            if not record:
                raise ValueError("Record not found")

            cnt = len(record)
            if cnt > 1:
                '''
                Its possible to retrieve more then one record for some companies.
                Currently always first record will be picked
                '''
                print('@TODO', record)
                print('pick index', cnt)

            index = 0
            record = record[index]
            self.addRecord(record)

        return record

    def addRecord(self, record):
        if self.database:
            self.database.insert(record)

    def updateRecord(self, taxpayerid):
        if self.database:
            record = self.crm.getRecords(taxpayerid, self.url, self.key)
            if not record:
                print('Record has not been found for', taxpayerid)
                return
            self.database.update(record[0])

    def configs_to_template_dict(self) -> dict:
        return {
            'ref_account_number': configs.config.get('Refere', 'account_number')
        }

    def generateInvoiceTemplete(self, taxpayerid):
        ref = self.crm.recordToRefere(self.getRecord(self.ref_taxpayerid))
        client = self.getRecord(taxpayerid)
        client.update(ref)

        if self.invoice_number:
            client.update(self.invoice_number)

        if self.invoice_items:
            client.update(self.invoice_items)

        for plugins in self.mod_qrcode:
            client.update(plugins(client)())

        client.update(self.configs_to_template_dict())

        with open(configs.config.get('Paths', 'template')) as fd:
            template = fd.read()
            out = template.format(**client)

        return out
