CREATE TABLE IF NOT EXISTS dim_country (
    country_id   INTEGER PRIMARY KEY,
    country_name TEXT NOT NULL,
    region       TEXT
);

CREATE TABLE IF NOT EXISTS fact_uranium_price (
    price_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    price_date   DATE    NOT NULL,
    year         INTEGER NOT NULL,
    month        INTEGER NOT NULL,
    price_usd_lb REAL    NOT NULL
);

CREATE TABLE IF NOT EXISTS fact_production (
    production_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    country_name    TEXT    NOT NULL,
    year            INTEGER NOT NULL,
    production_tu   REAL    NOT NULL,
    pct_world_share REAL
);

CREATE TABLE IF NOT EXISTS fact_nuclear_generation (
    gen_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    country_name   TEXT    NOT NULL,
    year           INTEGER NOT NULL,
    generation_twh REAL    NOT NULL
);
