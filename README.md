# Carbon Footprint & Sustainability Insights  
### Data Analysis | Sustainability Analytics | Power BI Dashboard | Python (Pandas, Plotly)

This project explores global CO₂ emissions, sustainability trends, and environmental performance across countries using **Python** and **Power BI**.  
It highlights global emission patterns, per-capita pollution levels, regional differences, and correlations using advanced data cleaning and interactive visualizations.

## Project Objectives

- Analyze global **CO₂ emission trends** over time  
- Compare CO₂ **per capita** across regions and countries  
- Identify **top polluting countries**  
- Evaluate **regional sustainability patterns**  
- Use **MICE imputation** to fix missing environmental data  
- Build a **Power BI dashboard** with KPIs and interactive visuals  
- Derive **insights for climate policy and sustainability planning**

##  Dataset Information

- **Rows:** 5677  
- **Columns:** Country, Region, Date, Kilotons of CO₂, Metric Tons Per Capita  
- **Years Covered:** Multiple years across global regions  

## Data Cleaning Process

###  Date Parsing  
Converted the `Date` string into `datetime` and extracted the `Year`.

### Column Standardization  
- Kilotons of Co2 → co2_kilotons  
- Metric Tons Per Capita → co2_per_capita  

###  Missing Value Treatment (MICE)
Applied Iterative Imputer (Bayesian Ridge) for multi-variable estimation.

### Cleaned Output File  
`outputs/cleaned_carbon_emissions.csv`

## Python Analysis

Main script: `analysis.py`

Generates:
- Global CO₂ Trend  
- Global CO₂ Per Capita Trend  
- Regional CO₂ Trend  
- Top 10 CO₂ Per Capita  
- Scatter (Latest Year)  
- Correlation Heatmap  

All charts saved under: `outputs/charts/`

##  Power BI Dashboard

KPIs (Latest Year):
- Total CO₂ Emissions: 33.87M  
- CO₂ Per Capita: 4.14  
- Countries: 190  

Visuals include:
- Line Charts  
- Top 10 Countries  
- Filled Map  
- Correlation Matrix  

##  Key Insights

- CO₂ emissions show **steady growth**.
- **Asia** contributes the highest emissions.
- High per-capita emitters include Qatar, UAE, Kuwait, Bahrain.
- Weak correlation (0.19) between total and per-capita emissions.

## Run Instructions

### Install dependencies:
pip install pandas plotly scikit-learn

### Run script:
python analysis.py

### View charts:
Open HTML files in `outputs/charts/`.

##  Conclusion

This project delivers deep sustainability insights using Python & Power BI, supporting climate policy and research.

##  Contact
Email: santhoshreddyparkula@gmail.com  
LinkedIn: linkedin.com/in/santhoshreddyparkula  
