PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE customers (
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
                );
CREATE TABLE version (record int PRIMARY KEY NOT NULL UNIQUE, version int);
INSERT INTO version VALUES(1,512);
CREATE TABLE sales (
                id INTEGER,
                customer INTEGER NOT NULL,
                invoice_id text UNIQUE,
                amount REAL,
                invoice_pdf BLOB NOT NULL UNIQUE,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                FOREIGN KEY("customer") REFERENCES "customers"("id"),
                PRIMARY KEY("id" AUTOINCREMENT)
                );
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('customers',3);
COMMIT;
