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
from autoinvoice import configs
from autoinvoice.common import pure_virtual


class ICompanyRegister:
    def __init__(self):
        self.verbose = configs.config.getboolean('Options', 'verbose', fallback=False)

    @pure_virtual
    def getRecords(self, TaxPayerId, url, key) -> []:
        """
        Return vector with dictionaries related to single tax payer id
        """
        return [self.buildRecord(...)]

    def buildRecord(self, taxpayerid, regon, customername, state, address, postcode, city, refere) -> dict:
        if not isinstance(taxpayerid, str):
            raise ValueError('taxpayerid is not str, {}'.format(type(taxpayerid)))
        if not isinstance(regon, str):
            raise ValueError('regon is not str, {}'.format(type(regon)))
        if not isinstance(customername, str):
            raise ValueError('name is not str, {}'.format(type(customername)))
        if not isinstance(state, str):
            raise ValueError('state is not str, {}'.format(type(state)))
        if not isinstance(address, str):
            raise ValueError('address is not str, {}'.format(type(address)))
        if not isinstance(postcode, str):
            raise ValueError('postcode is not str, {}'.format(type(postcode)))
        if not isinstance(city, str):
            raise ValueError('city is not str, {}'.format(type(city)))
        if not isinstance(refere, str):
            raise ValueError('refere is not str, {}'.format(type(refere)))
        return {
                'taxpayerid' : taxpayerid,
                'regon' : regon,
                'customername' : customername,
                'state' : state,
                'address' : address,
                'postcode' : postcode,
                'city' : city,
                'refere' : refere
                }

    def recordToRefere(self, record) -> dict:
        """
        Takes as input database record
        """
        if self.verbose:
            print(record)

        return {
                'ref_taxpayerid' : record['taxpayerid'],
                'ref_regon' : record['regon'],
                'ref_companyname' : record['customername'],
                'ref_state' : record['state'],
                'ref_address' : record['address'],
                'ref_postcode' : record['postcode'],
                'ref_city' : record['city'],
                'ref_refere' : record['refere'],
                }


@pure_virtual
def get():
    return ICompanyRegister