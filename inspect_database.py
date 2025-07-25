import pandas as pd
from sqlalchemy import create_engine , inspect
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "sqlite:///data/kbo_database.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

inspector = inspect(engine)
# Inspect the database
# Get the list of tables in the database
tables = inspector.get_table_names()
# Accross tables and columns
for table in tables:
    print(f"\n📘 Table: {table}")
    
    # Columns
    columns = inspector.get_columns(table)
    for col in columns:
        print(f"   - {col['name']:20} | {col['type']}")
# Get the primary key for each table
    primary_keys = inspector.get_pk_constraint(table)
    print(f"   Primary Key: {primary_keys['constrained_columns']}")
    
    # Get foreign keys
    foreign_keys = inspector.get_foreign_keys(table)
    for fk in foreign_keys:
        print(f"   Foreign Key: {fk['name']} -> {fk['referred_table']} ({fk['referred_columns']})")
    
    # Get indexes
    indexes = inspector.get_indexes(table)
    for index in indexes:
        print(f"   Index: {index['name']} - Unique: {index['unique']}")
    
# Analyses structure and quality of the data
quality_report = []
for table in tables:
   
    df = pd.read_sql_table(table, con=engine)
    total_rows = len(df)
    for col in df.columns:
        missing_pct = df[col].isna().mean() * 100
        unique_vals = df[col].nunique(dropna=True)
        dtype = df[col].dtype

        quality_report.append ({
            "table": table,
            "column": col,
            "dtype": str(dtype),
            "missing_%": round(missing_pct, 2),
            "n_unique": unique_vals,
            "n_total": total_rows
        })

# DataFrame final
df_quality = pd.DataFrame(quality_report)
# Affichage
print(df_quality)
