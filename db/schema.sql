PRAGMA foreign_keys = ON;

CREATE TABLE sectors (
    sector_id INTEGER PRIMARY KEY,
    sector_name TEXT
);

CREATE TABLE companies (
    company_id INTEGER PRIMARY KEY,
    company_name TEXT,
    ticker TEXT,
    sector_id INTEGER,
    FOREIGN KEY (sector_id) REFERENCES sectors(sector_id)
);

CREATE TABLE profitandloss (
    company_id INTEGER,
    year INTEGER,
    sales REAL,
    operating_profit REAL,
    opm REAL,
    net_profit REAL,
    eps REAL,
    dividend REAL,
    tax_rate REAL,
    PRIMARY KEY (company_id, year),
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

CREATE TABLE balancesheet (
    company_id INTEGER,
    year INTEGER,
    total_assets REAL,
    total_liabilities REAL,
    equity REAL,
    PRIMARY KEY (company_id, year),
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

CREATE TABLE cashflow (
    company_id INTEGER,
    year INTEGER,
    cash_from_operating REAL,
    cash_from_investing REAL,
    cash_from_financing REAL,
    net_cash REAL,
    PRIMARY KEY (company_id, year),
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

CREATE TABLE stock_prices (
    company_id INTEGER,
    date TEXT,
    close_price REAL,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

CREATE TABLE financial_ratios (
    company_id INTEGER,
    year INTEGER,
    roe REAL,
    PRIMARY KEY (company_id, year),
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

CREATE TABLE analysis (
    company_id INTEGER,
    analysis TEXT
);

CREATE TABLE documents (
    company_id INTEGER,
    url TEXT
);

CREATE TABLE prosandcons (
    company_id INTEGER,
    pros TEXT,
    cons TEXT
);

CREATE TABLE peer_groups (
    company_id INTEGER,
    peer_id INTEGER
);