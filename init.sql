CREATE DATABASE IF NOT EXISTS qonto;

USE qonto;

CREATE TABLE IF NOT EXISTS bank_accounts(
    id int NOT NULL AUTO_INCREMENT,
    iban varchar(34) NOT NULL,
    bic varchar(11) NOT NULL,
    organization_name VARCHAR(255) NOT NULL,
    balance_cents int NOT NULL,
    created_at DATETIME NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (iban)
);

CREATE TABLE IF NOT EXISTS transfers(
    id int NOT NULL AUTO_INCREMENT,
    bank_account_id int NOT NULL,
    counterparty_name VARCHAR(255) NOT NULL,
    counterparty_iban varchar(34) NOT NULL,
    counterparty_bic varchar(11) NOT NULL,
    amount_cents int NOT NULL,
    description TEXT NOT NULL,
    created_at DATETIME NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (bank_account_id) REFERENCES bank_accounts (id)
);

INSERT INTO bank_accounts (id, organization_name, iban, bic, balance_cents, created_at)
VALUES ('1', 'ACME Corp', 'FR10474608000002006107XXXXX', 'OIVUSCLQXXX', 10000000, '2024-02-07 00:00:00');
