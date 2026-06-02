-- KPI Queries: Uranium & Energy Market Intelligence Dashboard
-- Run against: uranium_dashboard.db

-- KPI 1: Latest spot price
SELECT price_date, price_usd_lb
FROM fact_uranium_price
ORDER BY price_date DESC LIMIT 1;

-- KPI 2: 12-month average price
SELECT ROUND(AVG(price_usd_lb), 2) AS avg_price_12m
FROM fact_uranium_price
WHERE price_date >= DATE('now', '-12 months');

-- KPI 3: Month-over-month change %
WITH ranked AS (
    SELECT price_date, price_usd_lb,
           LAG(price_usd_lb) OVER (ORDER BY price_date) AS prev_price
    FROM fact_uranium_price
)
SELECT price_date,
       price_usd_lb,
       ROUND(((price_usd_lb - prev_price) / prev_price) * 100, 2) AS mom_pct
FROM ranked
ORDER BY price_date DESC LIMIT 1;

-- KPI 4: Year-over-year price change %
WITH annual AS (
    SELECT year, AVG(price_usd_lb) AS avg_price
    FROM fact_uranium_price GROUP BY year
),
yoy AS (
    SELECT year, avg_price,
           LAG(avg_price) OVER (ORDER BY year) AS prev_year_price
    FROM annual
)
SELECT year,
       ROUND(avg_price, 2) AS avg_price,
       ROUND(((avg_price - prev_year_price) / prev_year_price) * 100, 2) AS yoy_pct
FROM yoy ORDER BY year DESC LIMIT 5;

-- KPI 5: Top producing countries (latest year)
SELECT country_name, production_tu, pct_world_share
FROM fact_production
WHERE year = (SELECT MAX(year) FROM fact_production)
ORDER BY production_tu DESC LIMIT 5;

-- KPI 6: Canada production share over time
SELECT year, production_tu, pct_world_share
FROM fact_production
WHERE country_name = 'Canada'
ORDER BY year;

-- 12-month moving average (used for Page 2 overlay)
SELECT
    p.price_date,
    p.price_usd_lb,
    ROUND(AVG(p2.price_usd_lb), 2) AS moving_avg_12m
FROM fact_uranium_price p
JOIN fact_uranium_price p2
  ON p2.price_date BETWEEN DATE(p.price_date, '-11 months') AND p.price_date
GROUP BY p.price_date
ORDER BY p.price_date;
