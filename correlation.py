import pandas as pd
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
import seaborn as sns
import matplotlib.pyplot as plt

DATABASE_URL = "sqlite:///data/kbo_database.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Charger les principales tables
df_ent = pd.read_sql("SELECT * FROM enterprise", con=engine)
df_act = pd.read_sql("SELECT EntityNumber, NaceCode, Classification FROM activity", con=engine)
df_addr = pd.read_sql("SELECT * FROM address", con=engine)

# Joindre : entreprises + activité principale + adresse
df = df_ent.merge(
    df_act[df_act["Classification"] == "MAIN"],
    how="left",
    left_on="EnterpriseNumber",
    right_on="EntityNumber"
).merge(
    df_addr,
    how="left",
    left_on="EnterpriseNumber",
    right_on="EntityNumber"
)
# Corrélation brute entre colonnes numériques
print(df.corr(numeric_only=True))