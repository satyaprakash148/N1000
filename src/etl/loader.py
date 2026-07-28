import pandas as pd
import sqlite3
import os


DB_PATH = "db/nifty100.db"
RAW_PATH = "data/raw"
OUTPUT_PATH = "output"

os.makedirs(OUTPUT_PATH, exist_ok=True)


 
# DATABASE CONNECTION
 

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Enable FK checking
cursor.execute(
    "PRAGMA foreign_keys = ON;"
)


 
# LOAD SCHEMA
 

with open("db/schema.sql", "r") as file:
    schema_sql = file.read()


# Clean rebuild for Sprint testing
cursor.executescript("""
DROP TABLE IF EXISTS peer_groups;
DROP TABLE IF EXISTS prosandcons;
DROP TABLE IF EXISTS documents;
DROP TABLE IF EXISTS analysis;
DROP TABLE IF EXISTS financial_ratios;
DROP TABLE IF EXISTS stock_prices;
DROP TABLE IF EXISTS cashflow;
DROP TABLE IF EXISTS balancesheet;
DROP TABLE IF EXISTS profitandloss;
DROP TABLE IF EXISTS companies;
DROP TABLE IF EXISTS sectors;
""")


cursor.executescript(schema_sql)



 
# AUDIT
 

audit = []



def load_table(file_name, table_name):

    file_path = os.path.join(
        RAW_PATH,
        file_name
    )


    rows_loaded = 0
    rows_rejected = 0
    errors = []


    try:

        df = pd.read_excel(file_path)


        for index, row in df.iterrows():

            try:

                row.to_frame().T.to_sql(
                    table_name,
                    conn,
                    if_exists="append",
                    index=False
                )

                rows_loaded += 1


            except Exception as e:

                rows_rejected += 1

                errors.append(
                    f"Row {index}: {str(e)}"
                )



    except Exception as e:

        errors.append(
            f"File error: {str(e)}"
        )



    audit.append({

        "table": table_name,

        "rows_loaded": rows_loaded,

        "rows_rejected": rows_rejected,

        "errors":
            " | ".join(errors[:5])

    })


    print(
        f"{table_name}: "
        f"loaded={rows_loaded}, "
        f"rejected={rows_rejected}"
    )



 
# LOAD ORDER
 

tables = [

    ("sectors.xlsx", "sectors"),

    ("companies.xlsx", "companies"),

    ("profitandloss.xlsx", "profitandloss"),

    ("balancesheet.xlsx", "balancesheet"),

    ("cashflow.xlsx", "cashflow"),

    ("stock_prices.xlsx", "stock_prices"),

    ("financial_ratios.xlsx", "financial_ratios"),

    ("analysis.xlsx", "analysis"),

    ("documents.xlsx", "documents"),

    ("prosandcons.xlsx", "prosandcons"),

    ("peer_groups.xlsx", "peer_groups")

]



for file_name, table_name in tables:

    load_table(
        file_name,
        table_name
    )



 
# SAVE LOAD AUDIT
 

audit_df = pd.DataFrame(audit)


audit_file = os.path.join(
    OUTPUT_PATH,
    "load_audit.csv"
)


audit_df.to_csv(
    audit_file,
    index=False
)



 
# FOREIGN KEY CHECK
 

cursor.execute(
    "PRAGMA foreign_key_check;"
)


fk_errors = cursor.fetchall()



conn.commit()
conn.close()



print("\n========== LOAD COMPLETE ==========")

print(
    "Database:",
    os.path.abspath(DB_PATH)
)

print(
    "FK Errors:",
    len(fk_errors)
)

print(
    "Audit:",
    audit_file
)