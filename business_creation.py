from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pandas as pd
import matplotlib.pyplot as plt

def show(): 
        # Connexion
        engine = create_engine("sqlite:///data/kbo_database.db")
        Session = sessionmaker(bind=engine)
        session = Session()

        # Requête
        stmt = text("""
            SELECT StartDate, TypeOfEnterprise
            FROM enterprise
            WHERE StartDate IS NOT NULL;
        """)

        result = session.execute(stmt).fetchall()
        df = pd.DataFrame(result, columns=["StartDate", "TypeOfEnterprise"])

        # Convertir StartDate au bon format
        df["StartDate"] = pd.to_datetime(df["StartDate"], format="%d-%m-%Y", errors="coerce")

        # Supprimer les lignes avec dates invalides
        df = df[df["StartDate"].notna()]

        # Extract year for grouping
        df["year"] = df["StartDate"].dt.to_period("Y").astype(str)

        # Map des types d'entreprise
        df["TypeLabel"] = df["TypeOfEnterprise"].map({1: "Natural Person", 2: "Legal Entity"})

        # Group by year and type
        df_grouped = df.groupby(["year", "TypeLabel"]).size().reset_index(name="company_count")

        # Pivot pour la courbe
        df_pivot = df_grouped.pivot(index="year", columns="TypeLabel", values="company_count").fillna(0)

        # Plot
        plt.figure(figsize=(12, 6))
        df_pivot.plot(kind="line",marker='o')
        plt.title("Creation of Enterprises by Year and Type", fontsize=16)
        plt.xlabel("year")
        plt.ylabel("Number of Enterprises Created")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        # keep the last 10 years only

        dernieres_annees = sorted(df["year"].unique())[-10:]
        df = df[df["year"].isin(dernieres_annees)]

        # Type d’entreprise
        df["TypeLabel"] = df["TypeOfEnterprise"].map({1: "Natural Person", 2: "Legal Entity"})

        # Agrégation
        df_grouped = df.groupby(["year", "TypeLabel"]).size().reset_index(name="company_count")
        df_pivot = df_grouped.pivot(index="year", columns="TypeLabel", values="company_count").fillna(0)

        # Plot
        plt.figure(figsize=(12, 6))
        df_pivot.plot(kind="line", marker='o')
        plt.title("Creation of Enterprises by Type (Last 10 Years)", fontsize=16)
        plt.xlabel("Year")
        plt.ylabel("Number of Enterprises Created")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()