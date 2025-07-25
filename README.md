
#  KBO Explorer - Belgian Companies Storytelling

Welcome to **KBO Explorer**, an interactive data storytelling app built with **Python**, **SQLite**, **SQLAlchemy**, and **Streamlit**.

This project offers an in-depth analysis of companies registered in **Belgium** using public data from the **Banque-Carrefour des Entreprises (BCE/KBO)**.

---

## Objective

Provide an intuitive and visual exploration tool for:

- Policymakers
- Entrepreneurs
- Data analysts
- Researchers

...interested in understanding **how Belgian companies are structured**, **how they evolve**, and **where key economic patterns emerge**.

---

## 🛠️ Tech Stack

- `Python 3.10+`
- `SQLite` — local relational database
- `SQLAlchemy` — ORM for structured queries
- `Pandas` — data manipulation
- `Plotly` — interactive visualizations
- `Streamlit` — dashboard UI
- `GeoPandas` + `pgeocode` — geospatial mapping

---

##  Database Structure

```
┌──────────────────┐        ┌────────────────────┐
│   enterprise     │◄──────►│     activity        │
│ (EnterpriseNumber)        │ (EntityNumber)     │
│                      ▲    └────────────────────┘
│                      │
│                      │    ┌────────────────────┐
│                      └────► address            │
│                           │ (EntityNumber)     │
│                           └────────────────────┘
│                      ▲
│                      │    ┌────────────────────┐
│                      └────► denomination       │
│                           │ (EntityNumber)     │
│                           └────────────────────┘
│                      ▲
│                      │    ┌────────────────────┐
│                      └────► contact            │
│                           │ (EntityNumber)     │
│                           └────────────────────┘
│
└──────────────────┘
        ▲
        │
        │
        ▼
┌────────────────────┐
│  establishment     │
│ (EnterpriseNumber) │
└────────────────────┘

Other tables:
- `code` : dictionary (code → description) for various fields.
- `branch` : appears similar to `establishment`
- `meta` : metadata about extraction process
```

---

##  Project Structure

```
challenge-data-analysis-sql/
├── data/                            # SQLite DB and GeoJSON files
│   ├── kbo_database.db
│   └── belgium_provinces.geojson
│
├── insights/                        # PNG insights & visuals
│   ├── creation entreprise by year and type.png
│   ├── Distribution of active vs deregistered companies.png
│   ├── Top 10 Juridical Form distribution with entreprise type.png
│   ├── top 10 most mature sectors.png
│   └── KBO-logo.jpg
│
├── JuridicalForms.py                # Legal status analysis
├── GeographicDistribution.py        # Mapping company distribution
├── dominant_sector_province.py     # Choropleth for sector dominance
├── dominant_economic_sector_per_province.py
├── business_creation.py            # Sector creation trends
├── status_entrprise.py             # Active/inactive companies
├── nace_code.py                    # Sector maturity analysis
│
├── inspect_database.py             # Data quality report
├── correlation.py                  # Relationship inspection
│
├── geojson_script_download.py      # Generates provinces GeoJSON
├── dashboard.py                    # Streamlit app entry point
├── requirements.txt
└── README.md
```

---

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/your-username/challenge-data-analysis-sql.git
cd challenge-data-analysis-sql
```

### 2. Create & activate virtual environment

```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On Unix/macOS
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Prepare GeoJSON (if needed)

```bash
python geojson_script_download.py
```

### 5. Launch Streamlit app

```bash
streamlit run dashboard.py
```

---

##  Features

- **Home** — Project goals and overview
- **Legal Forms** — Juridical structure distribution
- **Geographic Distribution** — Company spread by province & postal code
- **Sector Analysis (NACE)** — Oldest & newest economic sectors
- **Dominant Economic Sectors** — Choropleth by province
- **Business Status** — Active vs deregistered companies

---

##  Acknowledgments

- [Banque-Carrefour des Entreprises (KBO/BCE)](https://kbopub.economie.fgov.be/kbopub/zoeknummerform.html)
- [GADM](https://gadm.org/) for shapefiles
- [pgeocode](https://pypi.org/project/pgeocode/) for postal code geocoding

---

> Made with ❤️ in Belgium
