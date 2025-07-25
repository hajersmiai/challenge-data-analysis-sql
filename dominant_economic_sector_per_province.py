from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pandas as pd
import plotly.express as px
import pgeocode

def show():
        # Connect to SQLite database
        engine = create_engine("sqlite:///data/kbo_database.db")
        Session = sessionmaker(bind=engine)
        session = Session()

        # Step 1: SQL query to get activity per postal code with its NACE label and count
        stmt = text("""
            SELECT 
                a.Zipcode AS zipcode,
                c.Description AS nace_label,
                COUNT(*) AS company_count
            FROM address a
            JOIN enterprise e ON e.EnterpriseNumber = a.EntityNumber
            JOIN activity act ON act.EntityNumber = e.EnterpriseNumber
            LEFT JOIN code c ON c.Code = CAST(act.NaceCode AS TEXT)
                AND c.Category Like 'Nace%' AND c.Language = 'FR'
            WHERE a.Zipcode IS NOT NULL AND act.Classification = 'MAIN'
            GROUP BY a.Zipcode, c.Description
        """)
        result = session.execute(stmt).fetchall()

        # Step 2: Convert SQL result to DataFrame and clean
        raw_df = pd.DataFrame(result, columns=["zipcode", "nace_label", "company_count"])
        print("[INFO] Raw result size:", raw_df.shape)

        # Filter out missing postal codes or NACE labels
        df = raw_df.dropna(subset=["zipcode", "nace_label"])
        print("[INFO] Cleaned dataset size:", df.shape)

        # Pad zip codes with leading zeros (e.g., 1000 -> '1000')
        df["zipcode"] = df["zipcode"].astype(str).str.zfill(4)

        # Step 3: Identify the dominant sector for each postal code
        # Sort by company count descending, then keep only the first for each postal code
        dominant_sector = df.sort_values("company_count", ascending=False).drop_duplicates("zipcode")
        print("[INFO] Dominant sectors identified:", dominant_sector.shape)

        # Step 4: Enrich with geolocation data using pgeocode
        nomi = pgeocode.Nominatim('BE')
        # Convert list of zipcodes to DataFrame with location info
        location_df = nomi.query_postal_code(dominant_sector["zipcode"].tolist())
        # Merge location info back with dominant sector
        merged = dominant_sector.reset_index(drop=True).join(location_df[["latitude", "longitude", "state_name"]])

        # Step 5: Clean data (remove rows with missing coordinates)
        merged = merged.dropna(subset=["latitude", "longitude"])
        merged = merged.rename(columns={"state_name": "province"})

        # Step 6: Visualize using a geographic scatter plot
        fig = px.scatter_mapbox(
            merged,
            lat="latitude",
            lon="longitude",
            color="nace_label",              # Color by sector
            hover_name="province",           # Show province on hover
            size="company_count",            # Size reflects number of companies
            zoom=6,
            mapbox_style="carto-positron",
            title="Dominant Economic Sector per Postal Code / Province"
        )

        fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
        fig.show()
