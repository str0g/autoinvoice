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

from .driver import Driver
from . import configs

def main():
    options = configs.options
    if options.verbose:
        print(options)

    driver = Driver()

    if options.update:
        for taxpaierid in options.update:
            driver.updateRecord(str(taxpaierid))
    if options.generate:
        for taxpayerid in options.generate:
            template = driver.generateInvoiceTemplete(taxpayerid)
            if not options.output:
                print(template)
            else:
                index = options.output.rfind('.')
                output = options.output[:index] + '-' + taxpayerid + options.output[index:]
                with open(output, 'w') as fd:
                    fd.write(template)

    return 0


if __name__ == "__main__":
    main()
