import pandas as pd
import numpy as np
import os

# OPTIONAL (only needed if you want MICE)
from sklearn.experimental import enable_iterative_imputer  # noqa: F401
from sklearn.impute import IterativeImputer
from sklearn.linear_model import BayesianRidge

import plotly.express as px
import plotly.figure_factory as ff

#  PATHS 
DATA_FILE = r"dataset/carbon_emissions.csv" 
OUT_DIR   = r"outputs"
CHART_DIR = os.path.join(OUT_DIR, "charts")

os.makedirs(CHART_DIR, exist_ok=True)

#  LOAD DATA 
print(" Loading dataset from:", DATA_FILE)
df = pd.read_csv(DATA_FILE)

print("\n First 5 rows:")
print(df.head())

print("\nShape:", df.shape)
print("\nColumns:", df.columns.tolist())

#  BASIC CLEANING

# 1. Standardize column names (no spaces)
df = df.rename(columns={
    "Kilotons of Co2": "co2_kilotons",
    "Metric Tons Per Capita": "co2_per_capita"
})

# 2. Parse Date and extract Year
df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y", errors="coerce")
df["Year"] = df["Date"].dt.year

# 3. Check missing values before imputation
print("\n Missing values BEFORE imputation:")
print(df.isna().sum())

# MICE (Iterative Imputer) – for numeric columns 
numeric_cols = ["co2_kilotons", "co2_per_capita"]

# If there are no missing values, this will just return the same data
imputer = IterativeImputer(
    estimator=BayesianRidge(),
    max_iter=20,
    random_state=42
)

df[numeric_cols] = imputer.fit_transform(df[numeric_cols])

print("\n Missing values AFTER MICE imputation:")
print(df.isna().sum())

#  SAVE CLEANED DATA
os.makedirs(OUT_DIR, exist_ok=True)
cleaned_path = os.path.join(OUT_DIR, "cleaned_carbon_emissions.csv")
df.to_csv(cleaned_path, index=False)
print("\n Cleaned data saved to:", cleaned_path)

# SUMMARY STATS 
print("\n Summary statistics (numeric):")
print(df[["co2_kilotons", "co2_per_capita"]].describe())

#  AGGREGATIONS

# Global yearly totals and averages
yearly = df.groupby("Year").agg(
    total_co2_kilotons=("co2_kilotons", "sum"),
    avg_co2_per_capita=("co2_per_capita", "mean")
).reset_index()

# Regional yearly trends
regional_yearly = df.groupby(["Region", "Year"]).agg(
    total_co2_kilotons=("co2_kilotons", "sum"),
    avg_co2_per_capita=("co2_per_capita", "mean")
).reset_index()

# Top 10 countries by average CO2 (per capita)
country_avg = df.groupby("Country").agg(
    avg_co2_kilotons=("co2_kilotons", "mean"),
    avg_co2_per_capita=("co2_per_capita", "mean")
).reset_index()

top10_per_capita = country_avg.sort_values(
    "avg_co2_per_capita", ascending=False
).head(10)

#  CORRELATION
corr = df[["co2_kilotons", "co2_per_capita"]].corr()
print("\n Correlation matrix:")
print(corr)

#  PLOTLY VISUALS (HTML FILES) 

# 1. Global CO2 over time
fig1 = px.line(
    yearly,
    x="Year",
    y="total_co2_kilotons",
    title="Global CO₂ Emissions Over Time (Kilotons)"
)
fig1.write_html(os.path.join(CHART_DIR, "global_co2_trend.html"))

# 2. Global avg per capita over time
fig2 = px.line(
    yearly,
    x="Year",
    y="avg_co2_per_capita",
    title="Global Average CO₂ Per Capita Over Time"
)
fig2.write_html(os.path.join(CHART_DIR, "global_co2_per_capita_trend.html"))

# 3. Regional CO2 trends
fig3 = px.line(
    regional_yearly,
    x="Year",
    y="total_co2_kilotons",
    color="Region",
    title="Regional CO₂ Emissions Over Time"
)
fig3.write_html(os.path.join(CHART_DIR, "regional_co2_trend.html"))

# 4. Top 10 countries by CO2 per capita
fig4 = px.bar(
    top10_per_capita,
    x="Country",
    y="avg_co2_per_capita",
    title="Top 10 Countries by Average CO₂ Emissions Per Capita",
)
fig4.update_layout(xaxis_tickangle=-45)
fig4.write_html(os.path.join(CHART_DIR, "top10_per_capita.html"))

# 5. Scatter: total vs per capita (for most recent year)
latest_year = df["Year"].max()
latest = df[df["Year"] == latest_year]

fig5 = px.scatter(
    latest,
    x="co2_kilotons",
    y="co2_per_capita",
    color="Region",
    hover_name="Country",
    title=f"CO₂ Kilotons vs Per Capita ({latest_year})"
)
fig5.write_html(os.path.join(CHART_DIR, "scatter_latest_year.html"))

# 6. Correlation heatmap
heatmap = ff.create_annotated_heatmap(
    z=corr.values,
    x=corr.columns.tolist(),
    y=corr.index.tolist(),
    colorscale="Viridis"
)
heatmap.update_layout(title="Correlation: CO₂ Kilotons vs Per Capita")
heatmap.write_html(os.path.join(CHART_DIR, "correlation_heatmap.html"))

print("\n All charts saved in:", CHART_DIR)
print("Open the .html files in your browser to see interactive charts ")
