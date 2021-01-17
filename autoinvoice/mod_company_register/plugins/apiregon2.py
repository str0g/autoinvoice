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

from enum import IntEnum

from RegonAPI import RegonAPI, ApiAuthenticationError

from autoinvoice.mod_company_register.plugins.iface import ICompanyRegister


class APIREGON2(ICompanyRegister):
    class EnumReports(IntEnum):
        BIR11OsFizycznaDaneOgolne = 0
        BIR11OsFizycznaDzialalnoscCeidg = 1
        BIR11OsFizycznaDzialalnoscRolnicza = 2
        BIR11OsFizycznaDzialalnoscPozostala = 3
        BIR11OsFizycznaDzialalnoscSkreslonaDo20141108 =4
        BIR11OsFizycznaPkd = 5
        BIR11OsFizycznaListaJednLokalnych = 6
        BIR11JednLokalnaOsFizycznej = 7
        BIR11JednLokalnaOsFizycznejPkd = 8
        BIR11OsPrawna = 9
        BIR11OsPrawnaPkd = 10
        BIR11OsPrawnaListaJednLokalnych = 11
        BIR11JednLokalnaOsPrawnej = 12
        BIR11JednLokalnaOsPrawnejPkd = 13
        BIR11OsPrawnaSpCywilnaWspolnicy = 14
        BIR11TypPodmiotu = 15

    REPORTS = [
            "BIR11OsFizycznaDaneOgolne",
            "BIR11OsFizycznaDzialalnoscCeidg",
            "BIR11OsFizycznaDzialalnoscRolnicza",
            "BIR11OsFizycznaDzialalnoscPozostala",
            "BIR11OsFizycznaDzialalnoscSkreslonaDo20141108",
            "BIR11OsFizycznaPkd",
            "BIR11OsFizycznaListaJednLokalnych",
            "BIR11JednLokalnaOsFizycznej",
            "BIR11JednLokalnaOsFizycznejPkd",
            "BIR11OsPrawna",
            "BIR11OsPrawnaPkd",
            "BIR11OsPrawnaListaJednLokalnych",
            "BIR11JednLokalnaOsPrawnej",
            "BIR11JednLokalnaOsPrawnejPkd",
            "BIR11OsPrawnaSpCywilnaWspolnicy",
            "BIR11TypPodmiotu",
    ]

    def getRecords(self, TaxPayerId, url, key):
        if not TaxPayerId:
            raise ValueError("taxpayerid None")
        out = []
        try:
            is_production = True
            if url == 'not_production':
                is_production = False
            api = RegonAPI(bir_version="bir1.1", is_production=is_production)
            api.authenticate(key=key)
            results = api.searchData(nip=TaxPayerId)
            if len(results) > 1:
                print('@TODO more records')
            for result in results:
                address = self._address(result['Ulica'], result['NrNieruchomosci'], result['NrLokalu'])
                regon = result['Regon']
                rtype = ord(result['Typ'].lower())
                if rtype == 0x66:
                    name = self._name(api, regon)
                elif rtype == 0x70:
                    name = ''
                else:
                    raise ValueError('Unsupported type {}'.format(rtype))

                out.append(self.buildRecord(
                    TaxPayerId,
                    regon,
                    result['Nazwa'],
                    result['Wojewodztwo'],
                    address,
                    result['KodPocztowy'],
                    result['Miejscowosc'],
                    name
                    ))
                break
        except ApiAuthenticationError as e:
            print(e)
        except ValueError as e:
            print (e)

        return out

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

    def _name(self, api: RegonAPI, regon: str) -> str:
        result = api.dataDownloadFullReport(regon, self.REPORTS[self.EnumReports.BIR11OsFizycznaDaneOgolne])[0]
        return "{} {}".format(result['fiz_imie1'].capitalize(), result['fiz_nazwisko'].capitalize())


def get():
    return APIREGON2
