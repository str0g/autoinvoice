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

import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    d['taxpayerid'] = str(row[0])
    return d


class DataBase:
    def __init__(self, path):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()
        self.cur.row_factory = dict_factory
        self.migrate()
        self.database_2_00()

    def __deinit__(self):
        self.con.close()

    def is_table(self, table):
        try:
            self.cur.execute(f'SELECT * FROM {table}')
            return True
        except sqlite3.OperationalError as e:
            print(e)
            return False

    def database_1_00(self):
        if not self.is_table('companies'):
            self.cur.execute('''CREATE TABLE companies
            (taxpayerid int PRIMARY KEY NOT NULL UNIQUE, regon text, companyname text,
                    state text, address text, postcode text, city text, refere text, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL )''')
            self.con.commit()
        if not self.is_table('version'):
            self.cur.execute('CREATE TABLE version (record int PRIMARY KEY NOT NULL UNIQUE, version int)')
            self.con.commit()
            self.update_version('1.00')

    def database_2_00(self):
        if not self.is_table('customers'):
            self.cur.execute('''CREATE TABLE customers (
                id INTEGER,
                taxpayerid INTEGER NULL UNIQUE,
                phone_number text NULL UNIQUE,
                email text NULL UNIQUE,
                regon text NULL UNIQUE,
                customername text,
                state text,
                address text,
                postcode text,
                city text,
                refere text,
                extra_note text,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT)
                )''')
            self.con.commit()
        if not self.is_table('version'):
            self.cur.execute('CREATE TABLE version (record int PRIMARY KEY NOT NULL UNIQUE, version int)')
            self.con.commit()
            self.update_version('2.00')
        if not self.is_table('sales'):
            # Naive amount to get approximate value, the same goes for timestamp, for more accurent data open invoice stored in bin format
            self.cur.execute('''CREATE TABLE sales (
                id INTEGER,
                customer INTEGER NOT NULL,
                invoice_id text UNIQUE,
                amount REAL,
                invoice_pdf BLOB NOT NULL UNIQUE,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                FOREIGN KEY("customer") REFERENCES "customers"("id"),
                PRIMARY KEY("id" AUTOINCREMENT)
                )''')
            self.con.commit()

    def migrate(self):
        if not self.is_table('sales'):
            return
        version = self.get_version()
        if version == '1.00':
            # Create what scenery to update
            self.database_2_00()
            self.cur.execute("SELECT * FROM companies")
            for record in self.cur.fetchall():
                self.cur.execute('''INSERT INTO customers
                        (taxpayerid, regon, customername, state, address, postcode, city, refere)
                        VALUES
                        (:taxpayerid, :regon, :companyname, :state, :address, :postcode, :city, :refere)''', record)
                self.con.commit()
            self.cur.execute("DROP TABLE companies")
            # set new version
            self.update_version('2.00')

    def update_version(self, version: str):
        _version = self.version_to_db_format(version)
        self.cur.execute(f'INSERT INTO version (record, version) VALUES (1, {_version}) \
            ON CONFLICT(record) \
            DO UPDATE SET version={_version}')
        self.con.commit()

    def get_version(self):
        self.cur.execute('SELECT version FROM version where record=1')
        return self.version_from_db_format(self.cur.fetchone()['version'])

    def version_to_db_format(self, version: str) -> int:
        tmp = 0
        _version = version.split('.')
        _version.reverse()
        for index, value in enumerate(_version):
            tmp += (int(value) << 8 * index)
        return tmp

    def version_from_db_format(self, version: int) -> str:
        tmp_version = []
        for i in range(4):
            shift_n = 8 * i
            tmp_version.insert(0, str((version >> shift_n) & 0xff))
        rm = 0
        for index, value in enumerate(tmp_version):
            if value == '0':
                rm += 1
                continue
            else:
                break
        tmp_version = tmp_version[rm:]
        if len(tmp_version) == 2:
            return '%d.%.2d' % (int(tmp_version[0]), int(tmp_version[1]))
        elif len(tmp_version) == 3:
            return '%d.%.2d.%d' % (int(tmp_version[0]), int(tmp_version[1]), int(tmp_version[2]))

        return '.'.join(tmp_version[rm:])

    def _insert(self, record: dict):
        self.cur.execute('''INSERT INTO customers
        (taxpayerid, regon, customername)
        VALUES
        (?,?,?)''', (record['taxpayerid'], record['regon'], record['customername'],))
        self.con.commit()

    def insert(self, record: dict):
        self.cur.execute('''INSERT INTO customers
        (taxpayerid, regon, customername, state, address, postcode, city, refere)
        VALUES
        (:taxpayerid, :regon, :customername, :state, :address, :postcode, :city, :refere)''', record)
        self.con.commit()

    def update(self, record: dict):
        """
        Don't need to be entire record required, field is taxpayerid
        """
#        print(record)
        _record = self.getRecord(record["taxpayerid"])
        _record.update(record)
#        print(_record)
        self.cur.execute('''UPDATE customers SET
                regon=:regon, customername=:customername, state=:state, address=:address, postcode=:postcode, city=:city, refere=:refere
                WHERE
                taxpayerid=:taxpayerid''', _record)
        self.con.commit()

    def getRecord(self, TaxPayerId) -> dict:
        if TaxPayerId[0] == "+":
            self.cur.execute(
                "SELECT taxpayerid, phone_number, email, regon, customername, state, address, postcode, city, refere FROM customers WHERE phone_number=(?)",
                (TaxPayerId,))
        elif TaxPayerId.find("@") > 0:
            self.cur.execute(
                "SELECT taxpayerid, phone_number, email, regon, customername, state, address, postcode, city, refere FROM customers WHERE email=(?)",
                (TaxPayerId,))
        else:
            self.cur.execute("SELECT taxpayerid, phone_number, email, regon, customername, state, address, postcode, city, refere FROM customers WHERE taxpayerid=(?)", (TaxPayerId,))
        return self.cur.fetchone()

