from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pandas as pd
import matplotlib.pyplot as plt

def show():
        DATABASE_URL = "sqlite:///data/kbo_database.db"
        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(bind=engine)
        session = Session()
        # ##############"exploit real activity ################

        # Some companies may be technically active but awaiting deregistration or inactive in practice.
        req1 = text("""
            SELECT 
            CASE 
                WHEN DateStrikingOff IS NULL THEN 'Active'
                ELSE 'Removed'
            END AS company_state,
            COUNT(*) AS count,
            ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM address), 2) AS percentage
            FROM address
            GROUP BY company_state;""")

        result1 = session.execute(req1).fetchall()
        df1 = pd.DataFrame(result1, columns=["company_state", "count", "percentage"])

        # Pie chart
        df1.set_index("company_state")["count"].plot(
            kind="pie", autopct="%1.1f%%", figsize=(7, 7),
            title="Distribution of active vs. deregistered companies"
        )
        plt.ylabel("")
        plt.tight_layout()
        plt.show()

        # detect companies active in the register but without an active establishment:
        # Insight: Many registered businesses may be administrative or inactive in reality if they do not have establishments.

        req2 = text("""        
                SELECT 
                CASE 
                    WHEN e.EnterpriseNumber IN (
                        SELECT DISTINCT EnterpriseNumber FROM establishment
                    ) THEN 'With Establishments'
                    ELSE 'No Establishment'
                END AS establishment_status,
                COUNT(*) AS count,
                ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM enterprise), 2) AS percentage
                FROM enterprise e
                GROUP BY establishment_status;

        """)
        result2 = session.execute(req2).fetchall()
        df2 = pd.DataFrame(result2, columns=["establishment_status", "count", "percentage"])

        #pie chart
        df2.set_index("establishment_status")["count"].plot(
            kind="pie", autopct="%1.1f%%", figsize=(7, 7),
            title="Distribution of companies with and without establishments"
        )
        plt.ylabel("")
        plt.tight_layout()
        plt.show()

        # Main activity reported or not
        req3 = text("""
            SELECT 
            CASE 
                WHEN a.EntityNumber IS NULL THEN 'No Activity Declared'
                ELSE 'Activity Declared'
            END AS activity_status,
            COUNT(*) AS count,
            ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM enterprise), 2) AS percentage
            FROM enterprise e
            LEFT JOIN (
            SELECT DISTINCT EntityNumber 
            FROM activity 
            WHERE Classification = 'MAIN'
            ) a ON e.EnterpriseNumber = a.EntityNumber
            GROUP BY activity_status;

        """)
        result3 = session.execute(req3).fetchall()
        df3 = pd.DataFrame(result3, columns=["activity_status", "count", "percentage"])
        # Pie chart
        df3.set_index("activity_status")["count"].plot(
            kind="pie", autopct="%1.1f%%", figsize=(7, 7),
            title="Distribution of companies with and without main activity declared"
        )
        plt.ylabel("")
        plt.tight_layout()
        plt.show()