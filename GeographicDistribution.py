import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import pgeocode
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

def show():
        # Connexion à la base de données
        engine = create_engine("sqlite:///data/kbo_database.db")
        Session = sessionmaker(bind=engine)
        session = Session()

        # Requête SQL
        stmt = text("""
            SELECT 
                a.Zipcode AS zipcode,
                COUNT(*) AS company_count
            FROM address a
            JOIN enterprise e ON e.EnterpriseNumber = a.EntityNumber
            WHERE a.Zipcode IS NOT NULL
            GROUP BY a.Zipcode
            ORDER BY company_count DESC;
        """)

        result = session.execute(stmt).fetchall()
        df = pd.DataFrame(result, columns=["zipcode", "company_count"])
        df["zipcode"] = df["zipcode"].astype(str)

        # Récupérer latitude et longitude avec pgeocode
        nomi = pgeocode.Nominatim('BE')
        geo_df = df.copy()
        geo_df["latitude"] = geo_df["zipcode"].apply(lambda x: nomi.query_postal_code(x).latitude)
        geo_df["longitude"] = geo_df["zipcode"].apply(lambda x: nomi.query_postal_code(x).longitude)

        # Supprimer les lignes avec coordonnées manquantes
        geo_df.dropna(subset=["latitude", "longitude"], inplace=True)

        # Création de la carte
        fig = px.scatter_mapbox(
            geo_df,
            lat="latitude",
            lon="longitude",
            size="company_count",
            color="company_count",
            hover_name="zipcode",
            size_max=20,
            zoom=6,
            mapbox_style="carto-positron",
            title="Geographic Distribution of Companies in Belgium by Zipcode"
        )

        fig.show()
