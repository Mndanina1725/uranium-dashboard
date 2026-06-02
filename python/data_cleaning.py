import pandas as pd
import os

RAW   = "data/raw"
CLEAN = "data/cleaned"
os.makedirs(CLEAN, exist_ok=True)

# 1. Uranium spot price
price_df = pd.read_csv(f"{RAW}/uranium_spot_price_raw.csv")
price_df.columns = [c.strip().lower().replace(" ", "_") for c in price_df.columns]
price_df = price_df.rename(columns={
    "value":         "price_usd_lb",
    "price":         "price_usd_lb",
    "uranium_price": "price_usd_lb",
})
price_df["price_date"]   = pd.to_datetime(price_df["date"], errors="coerce")
price_df["year"]         = price_df["price_date"].dt.year
price_df["month"]        = price_df["price_date"].dt.month
price_df["price_usd_lb"] = pd.to_numeric(price_df["price_usd_lb"], errors="coerce")
price_df = price_df.dropna(subset=["price_date", "price_usd_lb"]).sort_values("price_date")
price_df[["price_date", "year", "month", "price_usd_lb"]].to_csv(
    f"{CLEAN}/fact_uranium_price.csv", index=False)
print(f"Price rows: {len(price_df)}")

# 2. Uranium production by country
prod_df = pd.read_csv(f"{RAW}/uranium_production_by_country_raw.csv")
prod_df.columns = [c.strip().lower().replace(" ", "_") for c in prod_df.columns]
prod_df = prod_df.rename(columns={
    "country":         "country_name",
    "tonnes_u":        "production_tu",
    "production_(tu)": "production_tu",
    "pct_world":       "pct_world_share",
    "pct_%":           "pct_world_share",
    "share_%":         "pct_world_share",
})
prod_df["production_tu"]   = pd.to_numeric(prod_df["production_tu"],   errors="coerce")
prod_df["pct_world_share"] = pd.to_numeric(prod_df["pct_world_share"], errors="coerce")
prod_df["year"]            = pd.to_numeric(prod_df["year"],            errors="coerce").astype("Int64")
prod_df = prod_df.dropna(subset=["country_name", "year", "production_tu"])
prod_df[["country_name", "year", "production_tu", "pct_world_share"]].to_csv(
    f"{CLEAN}/fact_production.csv", index=False)
print(f"Production rows: {len(prod_df)}")

# 3. Nuclear electricity generation
gen_df = pd.read_csv(f"{RAW}/nuclear_generation_by_country_raw.csv")
gen_df.columns = [c.strip().lower().replace(" ", "_") for c in gen_df.columns]
gen_df = gen_df.rename(columns={"entity": "country_name"})
twh_col = next((c for c in gen_df.columns if "nuclear" in c), None)
if twh_col and twh_col != "generation_twh":
    gen_df = gen_df.rename(columns={twh_col: "generation_twh"})
exclude = ["World", "Asia", "Europe", "Africa", "North America",
           "South America", "Oceania", "OECD", "Non-OECD",
           "High-income countries", "Upper-middle-income countries"]
gen_df = gen_df[~gen_df["country_name"].isin(exclude)]
gen_df["generation_twh"] = pd.to_numeric(gen_df["generation_twh"], errors="coerce")
gen_df = gen_df.dropna(subset=["generation_twh"])
gen_df = gen_df[gen_df["generation_twh"] > 0]
gen_df[["country_name", "year", "generation_twh"]].to_csv(
    f"{CLEAN}/fact_nuclear_generation.csv", index=False)
print(f"Generation rows: {len(gen_df)}")

# 4. Country dimension table
all_countries = pd.concat([
    prod_df[["country_name"]],
    gen_df[["country_name"]],
]).drop_duplicates().sort_values("country_name").reset_index(drop=True)
all_countries["country_id"] = range(1, len(all_countries) + 1)
region_map = {
    "Kazakhstan": "Central Asia",   "Uzbekistan": "Central Asia",
    "Canada": "North America",      "United States": "North America",
    "Namibia": "Africa",            "Niger": "Africa",
    "South Africa": "Africa",       "Australia": "Oceania",
    "Russia": "Europe",             "Ukraine": "Europe",
    "France": "Europe",             "Germany": "Europe",
    "United Kingdom": "Europe",     "China": "Asia",
    "India": "Asia",                "Japan": "Asia",
    "South Korea": "Asia",          "Brazil": "South America",
}
all_countries["region"] = all_countries["country_name"].map(region_map).fillna("Other")
all_countries[["country_id", "country_name", "region"]].to_csv(
    f"{CLEAN}/dim_country.csv", index=False)
print(f"Country dimension rows: {len(all_countries)}")
print("All 4 cleaned files written to data/cleaned/")
