import sqlite3

conn = sqlite3.connect("db/nifty100.db")
cursor = conn.cursor()

cursor.execute("""
SELECT company_id, year, net_cash
FROM cashflow
WHERE net_cash < 0;
""")

rows = cursor.fetchall()

if len(rows) == 0:
    print("0 rows")
else:
    for row in rows:
        print(row)

conn.close()