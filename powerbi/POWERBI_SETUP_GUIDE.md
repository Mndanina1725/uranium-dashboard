# Power BI Setup Guide
## Uranium & Energy Market Intelligence Dashboard

---

## Step 1 — Connect to Data

1. Open **Power BI Desktop**
2. **Home → Get Data → Text/CSV**
3. Import each file from `data/cleaned/`:
   - `fact_uranium_price.csv`
   - `fact_production.csv`
   - `fact_nuclear_generation.csv`
   - `dim_country.csv`
4. In **Power Query Editor**, confirm these data types:
   - `price_date` → **Date**
   - `price_usd_lb`, `production_tu`, `pct_world_share`, `generation_twh` → **Decimal Number**
   - `year`, `month` → **Whole Number**
   - All name/text fields → **Text**
5. Click **Close & Apply**

---

## Step 2 — Set Relationships (Model View)

Switch to **Model view** and create these relationships:

| From | To | Cardinality |
|---|---|---|
| `fact_production[country_name]` | `dim_country[country_name]` | Many-to-One |
| `fact_nuclear_generation[country_name]` | `dim_country[country_name]` | Many-to-One |

---

## Step 3 — Create DAX Measures

In the **Report view**, select `fact_uranium_price` in the Fields pane → **New Measure** for each:

```dax
Latest Price =
    CALCULATE(
        MAX(fact_uranium_price[price_usd_lb]),
        fact_uranium_price[price_date] = MAX(fact_uranium_price[price_date])
    )
```

```dax
Avg Price 12M =
    CALCULATE(
        AVERAGE(fact_uranium_price[price_usd_lb]),
        DATESINPERIOD(
            fact_uranium_price[price_date],
            LASTDATE(fact_uranium_price[price_date]),
            -12, MONTH
        )
    )
```

```dax
YoY Price Change % =
    VAR CurrentYear = CALCULATE(
        AVERAGE(fact_uranium_price[price_usd_lb]),
        YEAR(fact_uranium_price[price_date]) = YEAR(TODAY())
    )
    VAR PriorYear = CALCULATE(
        AVERAGE(fact_uranium_price[price_usd_lb]),
        YEAR(fact_uranium_price[price_date]) = YEAR(TODAY()) - 1
    )
    RETURN DIVIDE(CurrentYear - PriorYear, PriorYear)
```

```dax
Canada World Share =
    CALCULATE(
        AVERAGE(fact_production[pct_world_share]),
        dim_country[country_name] = "Canada",
        fact_production[year] = MAX(fact_production[year])
    )
```

```dax
World Production Total =
    CALCULATE(
        SUM(fact_production[production_tu]),
        fact_production[year] = MAX(fact_production[year])
    )
```

Format `YoY Price Change %` and `Canada World Share` as **Percentage** in the Measure Tools ribbon.

---

## Step 4 — Apply Colour Theme

**View → Themes → Customize current theme:**

| Element | Hex |
|---|---|
| Background | `#0D1B2A` (deep navy) |
| Primary accent / data colour 1 | `#F5A623` (uranium gold) |
| Secondary / data colour 2 | `#2196F3` (electric blue) |
| Canvas background | `#0D1B2A` |
| Font colour | `#FFFFFF` |

---

## Step 5 — Page 1: Executive Overview

**Add these visuals:**

| Visual | Type | Fields |
|---|---|---|
| Latest Uranium Price | KPI Card | Value: `Latest Price` measure |
| 12-Month Avg Price | KPI Card | Value: `Avg Price 12M` |
| YoY Price Change | KPI Card | Value: `YoY Price Change %` |
| Canada World Share | KPI Card | Value: `Canada World Share` |
| Uranium Price Trend | Line Chart | X: `price_date`, Y: `price_usd_lb` |
| Top Producers | Horizontal Bar | Y: `country_name`, X: `production_tu` — filter to latest year |
| Insight Summary | Text Box | See text below |

**Insight text box (Page 1):**
> Uranium spot prices have risen approximately 19% year-over-year, reaching ~$88/lb in mid-2026. Renewed utility contracting and growing nuclear commitments from AI hyperscalers are driving long-term demand. Canada — the world's second largest producer — supplies 15% of global uranium, positioning it as a critical swing supplier in a tightening market.

---

## Step 6 — Page 2: Price & Production Trends

**Add these visuals:**

| Visual | Type | Fields |
|---|---|---|
| Price Over Time | Line Chart | X: `price_date`, Y: `price_usd_lb` |
| MoM % Change | Column Chart | X: `price_date` (Month), Y: calculated MoM column or DAX |
| Production by Country | Stacked Bar | X: `year`, Y: `production_tu`, Legend: `country_name` |
| World Production Trend | Area Chart | X: `year`, Y: SUM `production_tu` |
| Canada vs Top Producers | Line Chart | X: `year`, Y: `production_tu` — filter to Canada, Kazakhstan, Namibia, Australia |
| Year Slicer | Slicer | Field: `year` (from `fact_production`) |

**Insight text box (Page 2):**
> The uranium price cycle shows a sustained recovery from sub-$30/lb lows in 2016–2020 to current levels above $85/lb. Canada's production has grown consistently, supported by Athabasca Basin operations. Kazakhstan remains the dominant global producer at ~43% world share, but Canadian supply quality and geopolitical stability make it strategically irreplaceable.

---

## Deliverable Checklist

- [x] `data/cleaned/` contains all 4 CSVs
- [x] `uranium_dashboard.db` loads without errors
- [x] All 6 KPI SQL queries return valid results
- [ ] Power BI connects to cleaned CSVs
- [ ] All 5 DAX measures work in Power BI
- [ ] Page 1 complete with 4 KPI cards, line chart, bar chart, text box
- [ ] Page 2 complete with price trend, production charts, slicer
- [ ] Colour theme applied consistently

---

## Live KPI Results (verified against uranium_dashboard.db)

| KPI | Value |
|---|---|
| Latest spot price | $88.30/lb (May 2026) |
| 12-month average | $78.32/lb |
| MoM change | +2.6% |
| YoY change (2026 vs 2025) | +19.0% |
| Top producer | Kazakhstan — 22,800 tU (43%) |
| Canada world share (2024) | 15.3% |
