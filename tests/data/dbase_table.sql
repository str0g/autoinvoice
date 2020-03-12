PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE companies (taxpayerid int PRIMARY KEY NOT NULL UNIQUE, regon text, companyname text,state text, address text, postcode text, city text, refere text, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL );

