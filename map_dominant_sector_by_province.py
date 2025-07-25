
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pandas as pd
import plotly.express as px
import pgeocode
import json

def show():
        # Load GeoJSON file
        with open("data/belgium_provinces.geojson", "r", encoding="utf-8") as f:
            geojson_data = json.load(f)

        # Connect to SQLite
        engine = create_engine("sqlite:///data/kbo_database.db")
        Session = sessionmaker(bind=engine)
        session = Session()

        # Query dominant sectors per zipcode
        stmt = text("""
            SELECT 
                a.Zipcode AS zipcode,
                c.Description AS nace_label,
                COUNT(*) AS company_count
            FROM address a
            JOIN enterprise e ON e.EnterpriseNumber = a.EntityNumber
            JOIN activity act ON act.EntityNumber = e.EnterpriseNumber
            LEFT JOIN code c ON c.Code = CAST(act.NaceCode AS TEXT)
                AND c.Category like 'Nace%' AND c.Language = 'FR'
            WHERE a.Zipcode IS NOT NULL AND act.Classification = 'MAIN'
            GROUP BY a.Zipcode, c.Description
        """)
        df = pd.DataFrame(session.execute(stmt).fetchall(), columns=["zipcode", "nace_label", "company_count"])
        df = df[df["nace_label"].notna() & df["zipcode"].notna()]
        df["zipcode"] = df["zipcode"].astype(str).str.zfill(4)

        # Dominant sector per zipcode
        dominant_sector = df.sort_values("company_count", ascending=False).drop_duplicates("zipcode")

        # Use pgeocode to get province from zipcode
        nomi = pgeocode.Nominatim("BE")
        location_df = nomi.query_postal_code(dominant_sector["zipcode"])
        location_df = location_df[["postal_code", "state_name"]].rename(columns={"postal_code": "zipcode", "state_name": "province"})
        location_df["zipcode"] = location_df["zipcode"].astype(str).str.zfill(4)

        # Merge with sector data
        dominant_sector = dominant_sector.merge(location_df, on="zipcode", how="left")

        # Aggregate to province level
        dominant_by_province = (
            dominant_sector.groupby(["province", "nace_label"])
            .agg({"company_count": "sum"})
            .reset_index()
            .sort_values("company_count", ascending=False)
            .drop_duplicates("province")
        )

        # Province name mapping to match GeoJSON
        province_mapping = {
            "Antwerpen": "Antwerpen",
            "Walloon Brabant": "Brabant Wallon",
            "Brussels Hoofdstedelijk Gewest": "Bruxelles",
            "Brussels": "Bruxelles",
            "Hainaut": "Hainaut",
            "Liege": "Liège",
            "Liège": "Liège",
            "Limburg": "Limburg",
            "Limbourg": "Limburg",
            "Luxembourg": "Luxembourg",
            "Namur": "Namur",
            "East Flanders": "Oost-Vlaanderen",
            "Oost-Vlaanderen": "Oost-Vlaanderen",
            "West Flanders": "West-Vlaanderen",
            "West-Vlaanderen": "West-Vlaanderen",
            "Flemish Brabant": "Vlaams Brabant",
            "Vlaams-Brabant": "Vlaams Brabant",
        }

        dominant_by_province["province_en"] = dominant_by_province["province"].map(province_mapping)

        # Log any unmatched provinces
        unmatched = dominant_by_province[dominant_by_province["province_en"].isna()]
        if not unmatched.empty:
            print(" Unmatched provinces in mapping:")
            print(unmatched["province"].unique())

        # Plot the choropleth
        fig = px.choropleth(
            dominant_by_province,
            geojson=geojson_data,
            featureidkey="properties.name",
            locations="province_en",
            color="nace_label",
            hover_name="province_en",
            hover_data={"company_count": True, "nace_label": True},
            title="Dominant Sector by Province (Belgium)"
        )
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
        fig.show()
