#! /bin/sh
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

function test {
	$1
#	if [ $? -ne 0 ]; then
#		exit $?
#	fi
}

rm -r $(find . -name "__pycache__" -type d)
find . -name "*.pyc" -type f -exec rm {} \;

test "python3 -m unittest tests/test_ICompanyRegister.py"
test "python3 -m unittest tests/test_apiregon.py"
test "python3 -m unittest tests/test_apiregon2.py"
test "python3 -m unittest tests/test_CompanyRegisterPluginManager.py"
test "python3 -m unittest tests/test_database.py"
test "python3 -m unittest tests/test_driver.py"
test "python3 -m unittest tests/test_cmdline.py"
test "python3 -m unittest tests/test_path_to_number.py"
test "python3 -m unittest tests/test_read_json.py"
test "python3 -m unittest tests/test_qrcode.py"
