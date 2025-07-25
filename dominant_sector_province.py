from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pandas as pd
import plotly.express as px
import pgeocode
import json

def show():
        # Load local GeoJSON file
        with open("data/belgium_provinces.geojson", "r", encoding="utf-8") as f:
            geojson_data = json.load(f)

        # Connect to the SQLite database
        engine = create_engine("sqlite:///data/kbo_database.db")
        Session = sessionmaker(bind=engine)
        session = Session()

        # Query: Get the number of companies per sector and postal code
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

        # Load results into a DataFrame
        df = pd.DataFrame(session.execute(stmt).fetchall(), columns=["zipcode", "nace_label", "company_count"])

        # Clean zipcodes and remove invalid rows
        df = df[df["nace_label"].notna() & df["zipcode"].notna()]
        df["zipcode"] = df["zipcode"].astype(str).str.zfill(4)

        # Find the dominant sector per zipcode
        dominant_sector = df.sort_values("company_count", ascending=False).drop_duplicates("zipcode")

        # Use pgeocode to map zipcodes to provinces
        nomi = pgeocode.Nominatim("BE")
        location_df = nomi.query_postal_code(dominant_sector["zipcode"])
        location_df = location_df[["postal_code", "state_name"]].rename(columns={"postal_code": "zipcode", "state_name": "province"})
        location_df["zipcode"] = location_df["zipcode"].astype(str).str.zfill(4)

        # Merge provinces into the dominant sector data
        dominant_sector = dominant_sector.merge(location_df, on="zipcode", how="left")

        # Aggregate to get the dominant sector by province
        dominant_by_province = (
            dominant_sector.groupby(["province", "nace_label"])
            .agg({"company_count": "sum"})
            .reset_index()
            .sort_values("company_count", ascending=False)
            .drop_duplicates("province")
        )

        # Map French province names to the English ones used in GeoJSON
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
        print(dominant_by_province["province_en"].isna().sum())
        # Plot choropleth using the matched province names
        fig = px.choropleth(
            dominant_by_province,
            geojson=geojson_data,
            featureidkey="properties.name",  # Match with the province name in GeoJSON
            locations="province_en",
            color="nace_label",
            hover_name="province_en",
            hover_data={"company_count": True, "nace_label": True},
            title="Dominant Sector by Province (Belgium)",
            
        )
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
        fig.show()
