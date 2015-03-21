BEGIN;
CREATE TABLE "housepricehistory_soldproperty" (
    "uid" varchar(36) NOT NULL PRIMARY KEY,
    "price" integer NOT NULL,
    "date" integer NOT NULL,
    "postcode" varchar(8) NOT NULL,
    "type" varchar(1) NOT NULL,
    "isold" boolean NOT NULL,
    "duration" varchar(1) NOT NULL,
    "paon" varchar(255) NOT NULL,
    "saon" varchar(255) NOT NULL,
    "street" varchar(255) NOT NULL,
    "locality" varchar(255) NOT NULL,
    "town" varchar(255) NOT NULL,
    "district" varchar(255) NOT NULL,
    "county" varchar(255) NOT NULL
);
COMMIT;