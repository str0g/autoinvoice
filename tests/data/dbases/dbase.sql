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
INSERT INTO customers VALUES(1,5222680297,NULL,NULL,'382921340','GUNS4HIRE ŁUKASZ BUŚKO','MAZOWIECKIE','ul. Lajosa Kossutha 12 lok. 48','01-315','Warszawa','Łukasz Buśko',NULL,'2023-04-01 16:32:26');
INSERT INTO customers VALUES(2,5261040828,NULL,NULL,'000331501','GŁÓWNY URZĄD STATYSTYCZNY','MAZOWIECKIE','ul. Test-Krucza 208','00-925','Warszawa','',NULL,'2023-04-01 16:32:26');
INSERT INTO customers VALUES(3,5261044039,NULL,NULL,'011612810','SAMSUNG ELECTRONICS POLSKA SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ','MAZOWIECKIE','ul. Postępu 14','02-676','Warszawa','Cho Sungchul',NULL,'2023-04-01 16:32:26');
INSERT INTO customers VALUES(4,NULL,'+48189807150','jan.brzechwa@wieszcze.pl',NULL,'Jan Brzechwa','Winnicki','ul. Brzechwy 42','66-666','Żmerynka','Jan Brzechwa','WZM22','2023-05-08 18:21:11');
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
