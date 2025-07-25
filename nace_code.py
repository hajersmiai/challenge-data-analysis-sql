from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pandas as pd
import matplotlib.pyplot as plt

def show():
        engine = create_engine("sqlite:///data/kbo_database.db")
        Session = sessionmaker(bind=engine)
        session = Session()

        ################ Average age of companies by sector (NACE code) ###########
        label_translation = {"Enseignement secondaire professionnel ou technique organisé par les forces armées": "Secondary Vocational or Technical Education Organized by the Armed Forces",
                            "Mutuelles et caisses d'assurance soins": "Mutuals and Health Insurance Funds",
                            "Location de logements sociaux": "Social Housing Rental",
                            "Entreprises d'assurances multibranches à prédominance non-vie": "Multi-branch Insurance Companies Predominantly Non-life",
                            "Autre distribution de crédit": "Other Credit Distribution",
                            "Extraction et agglomération de la houille": "Coal Mining and Agglomeration",
                            "Fabrication d'appareils de téléphonie": "Manufacturing of Telephony Devices",
                            "Administration communale, à l'exclusion des C.P.A.S.": "Municipal Administration, Excluding Public Social Welfare Centers (CPAS)",
                            "Location et exploitation de logements sociaux": "Rental and Operation of Social Housing",
                            "Fabrication d'autres produits céramiques à usage technique": "Manufacturing of Other Ceramic Products for Technical Use",
                            "Activités des ateliers de découpe de viande": "Activities of Meat Cutting Workshops",
                            "Façonnage et finition du bois": "Wood Shaping and Finishing",
                            "Réparation et entretien de véhicules de combat, de navires, de bateaux, d’aéronefs et d’engins spatiaux militaires": "Repair and Maintenance of Military Combat Vehicles, Ships, Boats, Aircraft, and Spacecraft",
                            "Autre transformation et conservation de la viande, à l’exception de la viande de volaille": "Other Meat Processing and Preservation, Except Poultry",
                            "Traitement thermique des métaux": "Heat Treatment of Metals",
                            "Construction d’aéronefs et d’engins spatiaux militaires et machines connexes": "Military Aircraft and Spacecraft Construction and Related Machinery",
                            "Stockage de l’électricité": "Electricity Storage",
                            "Activités d'intermédiation et commercialisation de brevets": "Patent Intermediation and Marketing Activities",
                            "Activités de service d’intermédiation pour la location et la location-bail d’autres biens corporels et d’immobilisations incorporelles non financières": "Intermediation and Leasing Services for Other Tangible Assets and Non-financial Intangible Assets",
                            "Activités de service d’intermédiation dans le domaine de l’appui scolaire et du tutorat": "Intermediation Services in the Field of School Support and Tutoring"
        }

        req = text("""
            SELECT 
            a.NaceCode,
            c.Description AS nace_label,
            ROUND(
                AVG(
                    (julianday('now') - 
                    julianday(
                        substr(e.StartDate, 7, 4) || '-' || substr(e.StartDate, 4, 2) || '-' || substr(e.StartDate, 1, 2)
                    )) / 365.25
                ), 1
            ) AS avg_age_years,
            COUNT(*) AS company_count
            FROM enterprise e
            JOIN activity a ON e.EnterpriseNumber = a.EntityNumber
            LEFT JOIN code c 
                ON c.Code = CAST(a.NaceCode AS TEXT)
                AND c.Category like 'Nace%'
                AND c.Language = 'FR'
            WHERE a.Classification = 'MAIN'
            AND e.StartDate IS NOT NULL
            AND LENGTH(e.StartDate) = 10
            GROUP BY a.NaceCode, c.Description
            ORDER BY avg_age_years DESC;
        """)
        result = session.execute(req).fetchall()
        df = pd.DataFrame(result, columns=["NaceCode", "nace_label", "avg_age_years", "company_count"])
        # Translate NACE labels
        df["nace_label_en"] = df["nace_label"].map(label_translation).fillna(df["nace_label"])
        # Forced conversion to numeric
        df["avg_age_years"] = pd.to_numeric(df["avg_age_years"], errors="coerce")
        df["company_count"] = pd.to_numeric(df["company_count"], errors="coerce")

        # Top 10 of oldest sectors
        top10_old = df.sort_values(by="avg_age_years", ascending=False).head(10)

        # delete rows with NaN in avg_age_years
        top10_old["nace_label_en"] = top10_old["nace_label_en"].str.slice(0, 60) + "..."

        plt.figure(figsize=(10, 6))
        plt.barh(top10_old["nace_label_en"], top10_old["avg_age_years"], color='teal')
        plt.xlabel("Average Age (years)", fontsize=12)
        plt.title("Top 10 most mature sectors (NACE)", fontsize=14)
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.show()

        # Top 10 of newest sectors
        top10_new = df.sort_values(by="avg_age_years", ascending=True).head(10)

        # delete rows with NaN in avg_age_years
        top10_new["nace_label_en"] = top10_new["nace_label_en"].str.slice(0, 60) + "..."

        plt.figure(figsize=(10, 6))
        plt.barh(top10_new["nace_label_en"], top10_new["avg_age_years"], color='teal')
        plt.xlabel("Average Age (years)", fontsize=12)
        plt.title("Top 10 newest sectors (NACE)", fontsize=14)
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.show()