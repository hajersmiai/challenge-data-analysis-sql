from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

def show():
        DATABASE_URL = "sqlite:///data/kbo_database.db"
        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(bind=engine)
        session = Session()

        stmt = text("""
            UPDATE enterprise
            SET JuridicalForm = 610.0
            WHERE JuridicalForm IS NULL
            AND TypeOfEnterprise = 1
        """)
        result = session.execute(stmt)
        session.commit()
        print(f"Updated {result.rowcount} rows in the enterprise table.")
        # Traduction des labels FR → EN
        label_translation = {
            "Société à responsabilité limitée": "Limited Liability Company",
            "Personne physique": "Natural Person",
            "Société anonyme": "Public Limited Company",
            "Association sans but lucratif": "Non-profit Association",
            "Société coopérative": "Cooperative Company",
            "Etablissement public": "Public Establishment",
            "Société simple": "Simple Company",
            "Société en nom collectif": "General Partnership",
            "Société en commandite": "Limited Partnership",
            "Société ou association sans personnalité juridique":" Company or Association without Legal Personality",
            "Entité étrangère sans établissement belge avec représentant responsable TVA": "Foreign Entity without Belgian Establishment with VAT Responsible Representative",
            # Ajoute d’autres formes si besoin
        }

        # Requête identique mais en français
        stmt1 = text("""
        WITH juridical_counts AS (
            SELECT 
                JuridicalForm,
                TypeOfEnterprise,
                COUNT(*) AS count,
                ROUND(100.0 * COUNT(*) / (
                    SELECT COUNT(*) FROM enterprise WHERE JuridicalForm IS NOT NULL
                ), 2) AS percentage
            FROM enterprise
            WHERE JuridicalForm IS NOT NULL
            GROUP BY JuridicalForm, TypeOfEnterprise
        )
        SELECT 
            jc.JuridicalForm,
            jc.TypeOfEnterprise,
            c.Description AS juridical_label,
            jc.count,
            jc.percentage
        FROM juridical_counts jc
        LEFT JOIN code c 
            ON c.Code = CAST(CAST(jc.JuridicalForm AS INT) AS TEXT)
            AND c.Category = 'JuridicalForm'
            AND c.Language = 'FR'
        ORDER BY jc.TypeOfEnterprise, jc.count DESC;
        """)

        # Charger les résultats
        result1 = session.execute(stmt1).fetchall()
        df1 = pd.DataFrame(result1, columns=["JuridicalForm", "TypeOfEnterprise", "juridical_label", "count", "percentage"]).head(10)

        # Traduction dans une nouvelle colonne
        df1["juridical_label_en"] = df1["juridical_label"].map(label_translation).fillna(df1["juridical_label"])

        ## Couleurs uniques par juridical_label_en
        unique_labels = df1["juridical_label_en"].unique()
        color_palette = plt.cm.tab10.colors  # 10 couleurs
        form_color_map = {label: color_palette[i % 10] for i, label in enumerate(unique_labels)}

        # Couleur de bordure selon TypeOfEnterprise
        edge_color_map = {1: "black", 2: "gray"}

        # Préparation des couleurs
        colors = [form_color_map[label] for label in df1["juridical_label_en"]]
        edge_colors = [edge_color_map[typ] for typ in df1["TypeOfEnterprise"]]

        # Plot
        fig, ax = plt.subplots(figsize=(10, 10))
        wedges, texts, autotexts = ax.pie(
            df1["count"],
            labels=df1["juridical_label_en"],
            colors=colors,
            wedgeprops={"edgecolor": "black", "linewidth": 2},
            autopct="%1.1f%%",
            startangle=140,
            textprops={"fontsize": 9}
        )

        # Modifier la couleur de bordure après coup
        for i, wedge in enumerate(wedges):
            wedge.set_edgecolor(edge_colors[i])

        # Légende pour formes juridiques
        form_legend = [Patch(facecolor=form_color_map[label], label=label) for label in unique_labels]

        # Légende pour type d’entreprise
        type_legend = [
            Patch(facecolor="white", edgecolor="black", linewidth=2, label="Natural Person"),
            Patch(facecolor="white", edgecolor="gray", linewidth=2, label="Legal Entity"),
        ]

        # Affichage
        plt.legend(handles=form_legend + type_legend, loc="upper left", bbox_to_anchor=(1.05, 1), title="Legend")
        plt.title("Top 10 of Juridical Form Distribution with Enterprise Type", fontsize=14)
        plt.axis("equal")
        plt.tight_layout()
        plt.show()