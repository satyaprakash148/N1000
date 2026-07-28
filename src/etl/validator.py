import sqlite3
import pandas as pd
import os


DB_PATH = "db/nifty100.db"
OUTPUT_PATH = "output"


os.makedirs(
    OUTPUT_PATH,
    exist_ok=True
)


conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()


failures = []



def log(rule, severity, message):

    failures.append({

        "rule": rule,

        "severity": severity,

        "message": message

    })



def table_exists(table):

    cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name=?
        """,
        (table,)
    )

    return cursor.fetchone() is not None



def run_check(rule, severity, query, message):

    try:

        cursor.execute(query)

        result = cursor.fetchall()


        if result:

            log(
                rule,
                severity,
                message
            )


    except sqlite3.Error as e:

        log(
            rule,
            "CRITICAL",
            f"SQL Error: {e}"
        )



  
# SCHEMA CHECK
  


required_tables = [

    "companies",

    "profitandloss",

    "balancesheet",

    "cashflow",

    "stock_prices",

    "financial_ratios",

    "analysis",

    "documents",

    "prosandcons",

    "peer_groups",

    "sectors"

]


for table in required_tables:

    if not table_exists(table):

        log(
            "SCHEMA",
            "CRITICAL",
            f"Missing table: {table}"
        )



if any(
    x["rule"] == "SCHEMA"
    for x in failures
):

    pd.DataFrame(failures).to_csv(
        "output/validation_failures.csv",
        index=False
    )

    print("Schema incomplete")

    conn.close()

    exit()



  
# DQ-01
  

run_check(
    "DQ-01",
    "CRITICAL",
    """
    SELECT company_id,COUNT(*)
    FROM companies
    GROUP BY company_id
    HAVING COUNT(*)>1
    """,
    "Duplicate company_id"
)



# DQ-02

run_check(
    "DQ-02",
    "CRITICAL",
    """
    SELECT company_id,year,COUNT(*)
    FROM profitandloss
    GROUP BY company_id,year
    HAVING COUNT(*)>1
    """,
    "Duplicate company-year"
)



# DQ-03

run_check(
    "DQ-03",
    "CRITICAL",
    """
    PRAGMA foreign_key_check
    """,
    "Foreign key violation"
)



# DQ-04

run_check(
    "DQ-04",
    "WARNING",
    """
    SELECT company_id,year
    FROM balancesheet
    WHERE total_assets>0
    AND ABS(
    total_assets-(total_liabilities+equity)
    )/total_assets >0.01
    """,
    "Balance sheet mismatch"
)



# DQ-05 SALES

run_check(
    "DQ-05",
    "CRITICAL",
    """
    SELECT company_id,year
    FROM profitandloss
    WHERE sales<=0
    """,
    "Negative sales"
)



# DQ-06 OPM

run_check(
    "DQ-06",
    "WARNING",
    """
    SELECT company_id,year
    FROM profitandloss
    WHERE operating_profit>sales
    """,
    "OPM greater than sales"
)



# DQ-07

run_check(
    "DQ-07",
    "WARNING",
    """
    SELECT company_id,year
    FROM cashflow
    WHERE net_cash IS NULL
    """,
    "Missing cashflow"
)



# DQ-08

run_check(
    "DQ-08",
    "CRITICAL",
    """
    SELECT *
    FROM stock_prices
    WHERE close_price<=0
    """,
    "Invalid stock price"
)



# DQ-09

run_check(
    "DQ-09",
    "WARNING",
    """
    SELECT company_id,year
    FROM financial_ratios
    WHERE roe<-100
    OR roe>100
    """,
    "ROE out of range"
)



# DQ-10

cursor.execute(
    "SELECT COUNT(*) FROM analysis"
)

count = cursor.fetchone()[0]


if count != 92:

    log(
        "DQ-10",
        "CRITICAL",
        f"Analysis rows !=92 ({count})"
    )



# DQ-11

run_check(
    "DQ-11",
    "WARNING",
    """
    SELECT company_id,year
    FROM profitandloss
    WHERE dividend<0
    """,
    "Negative dividend"
)



# DQ-12

run_check(
    "DQ-12",
    "WARNING",
    """
    SELECT company_id,year
    FROM profitandloss
    WHERE tax_rate<0
    OR tax_rate>50
    """,
    "Invalid tax rate"
)



# DQ-13

run_check(
    "DQ-13",
    "WARNING",
    """
    SELECT company_id,year
    FROM profitandloss
    WHERE eps IS NULL
    """,
    "Missing EPS"
)



# DQ-14

run_check(
    "DQ-14",
    "WARNING",
    """
    SELECT *
    FROM documents
    WHERE url NOT LIKE 'http%'
    """,
    "Invalid URL"
)



# DQ-15

run_check(
    "DQ-15",
    "WARNING",
    """
    SELECT company_id,year
    FROM cashflow
    WHERE net_cash<0
    """,
    "Negative net cash"
)



# DQ-16

run_check(
    "DQ-16",
    "WARNING",
    """
    SELECT company_id
    FROM profitandloss
    GROUP BY company_id
    HAVING COUNT(DISTINCT year)<5
    """,
    "Less than 5 years coverage"
)



  
# SAVE REPORT
  


df = pd.DataFrame(failures)


output_file = os.path.join(
    OUTPUT_PATH,
    "validation_failures.csv"
)


df.to_csv(
    output_file,
    index=False
)



print("\n== DQ CHECK COMPLETE ===")

print(
    "Failures:",
    len(df)
)

print(
    "Saved:",
    output_file
)



if len(df)==0:

    print(
        " ALL DATA QUALITY CHECKS PASSED"
    )

else:

    critical = df[
        df["severity"]=="CRITICAL"
    ]

    if len(critical)==0:

        print(
            " NO CRITICAL FAILURES"
        )

    else:

        print(
            "CRITICAL FAILURES FOUND"
        )

        print(critical)



conn.close()