PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE companies (taxpayerid int PRIMARY KEY NOT NULL UNIQUE, regon text, companyname text,state text, address text, postcode text, city text, refere text, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL );
INSERT INTO companies VALUES(5222680297,'382921340','GUNS4HIRE ŁUKASZ BUŚKO','MAZOWIECKIE','ul. Lajosa Kossutha 12 lok. 48','01-315','Warszawa','Łukasz Buśko','2019-09-18 12:51:39');
INSERT INTO companies VALUES(5261040828,'000331501','GŁÓWNY URZĄD STATYSTYCZNY','MAZOWIECKIE','ul. Test-Krucza 208','00-925','Warszawa','','2019-09-19 20:51:39');
INSERT INTO companies VALUES(5261044039,'011612810','SAMSUNG ELECTRONICS POLSKA SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ','MAZOWIECKIE','ul. Postępu 14','02-676','Warszawa','Cho Sungchul','2019-09-20 08:51:39');
COMMIT;
