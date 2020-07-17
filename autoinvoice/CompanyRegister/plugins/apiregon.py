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

from litex.regon import REGONAPI, REGONAPIError
from requests.exceptions import MissingSchema

from ..ICompanyRegister import ICompanyRegister


class APIREGON(ICompanyRegister):
    def getRecords(self, TaxPayerId, url, key):
        if not TaxPayerId:
            raise ValueError("taxpayerid None")

        return self.getDataByAPIREGON(TaxPayerId, url, key)

    def getDataByAPIREGON(self, TaxPayerId, url, key) -> [dict]:
        """
        Test driven implementation
        """
        if TaxPayerId.isnumeric():
            out = []
            api = None
            session = None
            try:
                api = REGONAPI(url)
                session = api.login(key)
                records = api.search(TaxPayerId, detailed=True)
                for record in records:
                    if record.Typ == 'F':
                        address, name = self._fizyczne(record.detailed)
                    elif record.Typ == 'P':
                        address, name = self._prawne(record.detailed)
                    else:
                        raise NotImplementedError("Unknown type: {}".format(record.Typ))

                    out.append(self.buildRecord(
                        TaxPayerId,
                        str(record[0].Regon),
                        str(record[0].Nazwa),
                        str(record[0].Wojewodztwo),
                        address,
                        str(record[0].KodPocztowy),
                        str(record[0].Miejscowosc),
                        name)) # imie1 nazwisko
            except REGONAPIError  as e:
                print("RegonAPI {} for session: {}, tax:{}, url:{}, key:{}".format(e, session, TaxPayerId, url, key))
            except MissingSchema as e:
                print("RegonAPI {} for session: {}, tax:{}, url:{}, key:{}".format(e, session, TaxPayerId, url, key))
            finally:
                if session:
                    api.logout()

            return out
        else:
            with open(TaxPayerId) as fd:
                return self.xmlToRecord(fd.read())

    def _address(self, street, streetnumber, premisesnumber):
        address = None

        if street:
            address = street
            if streetnumber and street:
                address = '{} {}'.format(street, streetnumber)
            elif streetnumber:
                address = streetnumber
            else:
                raise ValueError('[{}|{}|{}]'.format(street, streetnumber, premisesnumber))

        if premisesnumber:
            address = '{}/{}'.format(address, premisesnumber)

        return address


    def _prawne(self, data):
        return self._address(data.praw_adSiedzUlica_Nazwa, data.praw_adSiedzNumerNieruchomosci,
                             data.praw_adSiedzNumerLokalu), ''

    def _fizyczne(self, data):
        name = '{} {}'.format(str(data.fiz_imie1).capitalize(), str(data.fiz_nazwisko).capitalize())

        return self._address(data.fiz_adSiedzUlica_Nazwa, data.fiz_adSiedzNumerNieruchomosci,
                             data.fiz_adSiedzNumerLokalu), name

    def xmlToRecord(self, data) -> [dict]:
        """
        Required <data> element as input then will retrieve whats needed
        Returns database ready record
        """
        import xml.etree.ElementTree as ET

        records = []
        root = ET.fromstring(data)

        for data in root:
            address = ''
            street = data.findtext('Ulica')
            streetnumber = data.findtext('NrNieruchomosci')
            premisesnumber = data.findtext('NrLokalu')
        
            if street:
                address = street
            if streetnumber and street:
                address = '{} {}'.format(street, streetnumber)
            elif streetnumber:
                address = streetnumber
            if premisesnumber:
                address = '{}/{}'.format(address, premisesnumber)
        
            records.append(
                self.buildRecord(data.findtext('Nip'),
                                 data.findtext('Regon'),
                                 data.findtext('Nazwa'),
                                 data.findtext('Wojewodztwo'),
                                 address,
                                 data.findtext('KodPocztowy'),
                                 data.findtext('Miejscowosc'),
                                 '@TODO'))  # imie1 nazwisko
        return records


def get():
    return APIREGON