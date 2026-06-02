# Uranium & Energy Market Intelligence Dashboard

A data pipeline and interactive dashboard built to analyze the global uranium market. The project pulls from three public datasets, cleans and structures the data with Python, stores it in a SQLite database, and visualizes it as a two-page HTML dashboard.

Built as a portfolio project targeting energy sector data roles.

---

## What It Does

- Tracks uranium spot prices from 1990 to present
- Shows uranium production by country from 2013 to 2024
- Displays nuclear electricity generation by country
- Calculates six business KPIs: latest price, 12-month average, month-over-month change, year-over-year change, top producing countries, and Canada's world supply share

---

## Project Structure

```
uranium-dashboard/
├── data/
│   ├── raw/              # Original source files
│   └── cleaned/          # Processed CSVs ready for analysis
├── python/
│   └── data_cleaning.py  # Cleans raw data into 4 structured CSVs
├── sql/
│   ├── 01_create_tables.sql  # SQLite schema
│   ├── 02_load_data.py       # Loads CSVs into SQLite
│   └── 03_kpi_queries.sql    # Six KPI queries
├── powerbi/
│   ├── POWERBI_SETUP_GUIDE.md
│   └── TABLEAU_SETUP_GUIDE.md
├── uranium_dashboard.html    # Interactive dashboard (open in browser)
└── uranium_dashboard.db      # SQLite database
```

---

## Stack

- Python 3 / Pandas — data cleaning
- SQLite — data storage and KPI queries
- HTML / Chart.js — dashboard and visualizations

---

## How to Run

**1. Install dependencies**
```bash
pip3 install pandas
```

**2. Clean the raw data**
```bash
cd uranium-dashboard
python3 python/data_cleaning.py
```

**3. Load into SQLite**
```bash
python3 sql/02_load_data.py
```

**4. Open the dashboard**

Open `uranium_dashboard.html` in any browser. No server required.

---

## Dashboard

Two pages:

**Executive Overview** — five KPI cards, uranium price history from 1990 to present, and a top producers bar chart comparing the eight largest uranium-producing countries.

**Price & Production Trends** — spot price with a 12-month moving average overlay, world production trend, stacked country production chart, and a Canada vs Kazakhstan comparison.

---

## Data Sources

- Uranium spot price: UxC / Macrotrends (monthly, USD/lb, 1990–2026)
- Uranium production by country: World Nuclear Association (annual, tonnes uranium, 2013–2024)
- Nuclear electricity generation: Our World in Data (annual, TWh, 2013–2024)

---

## KPI Results (May 2026)

| Metric | Value |
|---|---|
| Latest spot price | $88.30 / lb |
| 12-month average | $78.32 / lb |
| Month-over-month change | +2.6% |
| Year-over-year change | +19.0% |
| Largest producer | Kazakhstan (43% world share) |
| Canada world share | 15.3% |
