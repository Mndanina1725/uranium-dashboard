# Tableau Public Setup Guide
## Uranium & Energy Market Intelligence Dashboard

---

## Before You Start

1. Download **Tableau Public** (free, Mac): https://public.tableau.com/app/discover
2. Create a free Tableau Public account at the same URL
3. Have your `data/cleaned/` folder open in Finder

---

## Step 1 — Connect to Data

Tableau Public uses one data source per workbook, so you'll use a **data union/join** approach with the price CSV as your primary source.

1. Open Tableau Public → **Connect to Data → Text File**
2. Navigate to `data/cleaned/` and select **`fact_uranium_price.csv`**
3. You'll land on the **Data Source** tab — your price data is now loaded

**Add the production data:**
4. In the left panel under **Connections**, click **Add** → **Text File**
5. Select `fact_production.csv`
6. Drag `fact_production` onto the canvas next to `fact_uranium_price`
7. Tableau will prompt for a join — close the join dialog (you don't need a join, you'll use them as separate sheets)

**Repeat for the other two files:**
8. Add `fact_nuclear_generation.csv` the same way
9. Add `dim_country.csv` the same way

**Pro tip:** Rename each connection in the left panel by right-clicking → Rename for clarity.

---

## Step 2 — Verify Data Types

Click each table and confirm these types in the Data Source tab (click the icon above each column to change):

| Table | Column | Type |
|---|---|---|
| fact_uranium_price | price_date | Date |
| fact_uranium_price | price_usd_lb | Number (decimal) |
| fact_uranium_price | year, month | Number (whole) |
| fact_production | production_tu, pct_world_share | Number (decimal) |
| fact_production | year | Number (whole) |
| fact_nuclear_generation | generation_twh | Number (decimal) |

---

## Step 3 — Build Sheet 1: Price Trend Line Chart

1. Click **Sheet 1** tab at the bottom
2. In the **Data** panel, switch the data source to `fact_uranium_price`
3. Drag **Price Date** to **Columns** — right-click it → **Exact Date** (so it shows monthly)
4. Drag **Price Usd Lb** to **Rows**
5. Tableau will draw a line chart automatically
6. Right-click the chart → **Trend Line → Show Trend Lines** (optional)
7. In **Marks**, change the mark type to **Line**
8. Right-click **Price Usd Lb** on Rows → **Add Table Calculation → Moving Average** → set to **12** periods
   - This adds your 12M moving average overlay as a second line
9. Double-click the sheet tab → rename it **"Price Trend"**

**Formatting:**
- Right-click the chart background → **Format** → set background to `#0D1B2A`
- Change line colour to `#F5A623` (click the colour mark → More Colors → enter hex)

---

## Step 4 — Build Sheet 2: Top Producers Bar Chart

1. Click the **+** to add a new sheet
2. Switch data source to `fact_production`
3. Drag **Country Name** to **Rows**
4. Drag **Production Tu** to **Columns**
5. In the **Filters** shelf, drag **Year** → select only **2024** → click OK
6. Click **Sort Descending** on the toolbar to sort by production volume
7. In **Marks**, set colour to `#2196F3`
8. To highlight Canada: drag **Country Name** to **Color** → right-click Canada in the legend → **Edit Color** → set to `#F5A623`
9. Rename sheet **"Top Producers"**

---

## Step 5 — Build Sheet 3: Production by Country (Stacked Bar)

1. New sheet → switch to `fact_production`
2. Drag **Year** to **Columns**
3. Drag **Production Tu** to **Rows**
4. Drag **Country Name** to **Color** in the Marks card
5. In Filters, drag **Country Name** → select: Kazakhstan, Canada, Namibia, Australia, Uzbekistan
6. In Marks, change type to **Bar** — Tableau will stack automatically
7. Rename sheet **"Production by Country"**

---

## Step 6 — Build Sheet 4: Canada vs Kazakhstan

1. New sheet → switch to `fact_production`
2. Drag **Year** to **Columns**
3. Drag **Production Tu** to **Rows**
4. Drag **Country Name** to **Color**
5. In Filters, drag **Country Name** → select only: Canada, Kazakhstan
6. Marks type: **Line**
7. Set Canada line to `#F5A623`, Kazakhstan to `#2196F3`
8. Rename sheet **"Canada vs Kazakhstan"**

---

## Step 7 — Build Sheet 5: World Production Trend

1. New sheet → switch to `fact_production`
2. Drag **Year** to **Columns**
3. Drag **Production Tu** to **Rows** → right-click → **Measure → Sum**
4. Marks type: **Area**
5. Colour: `#F5A623` with low opacity fill
6. Rename sheet **"World Production"**

---

## Step 8 — Build Sheet 6: KPI Text Sheets

For each KPI, create a simple **text sheet**:

1. New sheet → switch to `fact_uranium_price`
2. Drag **Price Usd Lb** to the **Text** mark
3. Right-click → **Measure → Maximum** (for latest price)
4. In Marks, click **Text** → format the number with $ prefix, 2 decimal places
5. Rename **"KPI Latest Price"**

Repeat for each KPI:
| Sheet Name | Source | Field | Aggregation |
|---|---|---|---|
| KPI Latest Price | fact_uranium_price | Price Usd Lb | Maximum |
| KPI 12M Avg | fact_uranium_price | Price Usd Lb | Average (filter last 12 months) |
| KPI Canada Share | fact_production | Pct World Share | (filter Canada, max year) |

For **YoY %** and **MoM %** — use a calculated field:
- Click **Analysis → Create Calculated Field**
- Name: `YoY Price Change %`
- Formula:
```
(AVG([Price Usd Lb]) - LOOKUP(AVG([Price Usd Lb]), -12)) / ABS(LOOKUP(AVG([Price Usd Lb]), -12))
```
- Format the result as a percentage

---

## Step 9 — Build Dashboard 1: Executive Overview

1. Click the **dashboard icon** (looks like a grid) at the bottom → **New Dashboard**
2. Set size: **Fixed → 1400 x 900**
3. Set background colour to `#0D1B2A`: Dashboard menu → **Format** → Background → Custom Color
4. **Drag sheets from the left panel onto the canvas:**

**Layout:**
```
[ KPI Latest ] [ KPI 12M Avg ] [ KPI MoM ] [ KPI YoY ] [ KPI Canada ]
[                                           ] [                        ]
[          Price Trend (large)              ] [   Top Producers        ]
[                                           ] [                        ]
[ Insight text box                                                      ]
```

5. For the **insight text box**: drag a **Text** object from the Objects panel (bottom left) → double-click → paste:
> *Uranium spot prices have risen approximately 19% year-over-year, reaching ~$88/lb in mid-2026. Renewed utility contracting and growing nuclear commitments from AI hyperscalers are driving long-term demand. Canada — the world's second-largest producer — supplies 15.3% of global uranium, positioning it as a critical swing supplier in a tightening market.*

6. Double-click the dashboard tab → rename **"Executive Overview"**

---

## Step 10 — Build Dashboard 2: Price & Production Trends

1. New dashboard → same 1400x900 fixed size, same `#0D1B2A` background
2. **Layout:**
```
[ Price + Moving Avg (large)    ] [ World Production              ]
[                                ] [                               ]
[ Production by Country         ] [ Canada vs Kazakhstan          ]
[                                ] [                               ]
[ Year filter / slicer          ]
[ Insight text box                                                 ]
```

3. **Add a Year filter:** drag any sheet with Year onto the dashboard → click the dropdown arrow on the Year filter pill → **Apply to Worksheets → All Using This Data Source**
4. **Insight text box:**
> *The uranium price cycle shows a sustained recovery from sub-$30/lb lows in 2016–2020 to current levels above $85/lb. Canada's production has grown consistently, supported by Athabasca Basin operations. Kazakhstan remains the dominant global producer at ~43% world share, but Canadian supply quality and geopolitical stability make it strategically irreplaceable.*

5. Rename tab **"Price & Production Trends"**

---

## Step 11 — Formatting Tips

- **Titles:** Double-click any chart title → change font to white, background `#0D1B2A`
- **Gridlines:** Format → Lines → set Row/Column dividers to `#1a3050`
- **Axis labels:** Format → Font → set to white
- **Remove borders** on KPI text sheets for a clean card look
- **Sheet borders on dashboard:** click each sheet → Layout panel → set Border to none or `#1a3050`

---

## Step 12 — Publish to Tableau Public

1. **File → Save to Tableau Public**
2. Sign in with your Tableau Public account
3. Name it: **"Uranium & Energy Market Intelligence Dashboard"**
4. Click Save — Tableau will upload and open it in your browser
5. Copy the public URL — this is your shareable portfolio link for Samuel

---

## KPI Reference (verified values)

| KPI | Value |
|---|---|
| Latest spot price | $88.30 / lb (May 2026) |
| 12-month average | $78.32 / lb |
| Month-over-month | +2.6% |
| Year-over-year | +19.0% |
| Top producer | Kazakhstan — 22,800 tU (43%) |
| Canada world share | 15.3% (2024) |

---

## Troubleshooting

**"Null" values appearing** → Check that price_date is set to Date type, not String, in the Data Source tab.

**Stacked bar not stacking** → Make sure mark type is Bar and Country Name is on Color (not on Rows).

**Moving average not showing** → The table calculation needs at least 12 rows of data; make sure no date filter is cutting off history.

**Publish fails** → Tableau Public requires an internet connection and that your workbook contains at least one dashboard (not just sheets).
