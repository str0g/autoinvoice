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

from .CompanyRegister.CompanyRegisterPluginManager import getCompanyRegister
from .CompanyRegister.database import DataBase
from .InvoiceNumbering import getInvoiceNumber

class Driver:
    def __init__(self, options):
        self.options = options
        self.crm = getCompanyRegister(options)
        self.invoice_number = getInvoiceNumber(options)

        self.database_init()

    def database_init(self):
        if not self.options.database:
            self.db = None
            return
        path = Path(self.options.database)
        path.touch(mode=0o640,exist_ok=True)
        self.db = DataBase(self.options.database)

    def getRecord(self, taxpayerid):
        record = None
        if self.db:
            record = self.db.getRecord(taxpayerid)
        if not record:
            record = self.crm.getRecords(taxpayerid, self.options.url, self.options.key)
            if not record:
                raise ValueError("Record not found")

            cnt = len(record)
            if(cnt>1):
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
        if self.db:
            self.db.insert(record)

    def updateRecord(self, taxpayerid):
        if self.db:
            record = self.crm.getRecords(taxpayerid, self.options.url, self.options.key)
            if not record:
                print('Record has not been found for', taxpayerid)
                return
            self.db.update(record[0])

    def generateInvoiceTemplete(self, taxpayerid):
        ref = self.crm.recordToRefere(self.getRecord(self.options.taxpayerid))
        client = self.getRecord(taxpayerid)
        client.update(ref)
        if self.invoice_number:
            client.update(self.invoice_number)


        with open(self.options.template) as fd:
            template = fd.read()
            out = template.format(**client)
                    
        return out
