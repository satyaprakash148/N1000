import pandas as pd
import os
import random

os.makedirs("data/raw", exist_ok=True)

NUM_COMPANIES = 92
YEARS = list(range(2010, 2024))  # 14 years

#      SECTORS     
sectors = [{"sector_id": i, "sector_name": f"Sector_{i}"} for i in range(1, 6)]
pd.DataFrame(sectors).to_excel("data/raw/sectors.xlsx", index=False)

#      COMPANIES     
companies = []
for i in range(1, NUM_COMPANIES + 1):
    companies.append({
        "company_id": i,
        "company_name": f"Company_{i}",
        "ticker": f"CMP{i}",
        "sector_id": random.randint(1, 5)
    })
pd.DataFrame(companies).to_excel("data/raw/companies.xlsx", index=False)

#      PROFIT & LOSS     
pl = []
for c in companies:
    base_sales = random.randint(500, 1500)

    for y in YEARS:
        growth = random.uniform(0.05, 0.15)
        base_sales *= (1 + growth)

        op = base_sales * random.uniform(0.15, 0.25)
        net = op * random.uniform(0.6, 0.8)

        pl.append({
            "company_id": c["company_id"],
            "year": y,
            "sales": round(base_sales, 2),
            "operating_profit": round(op, 2),
            "opm": round((op / base_sales) * 100, 2),
            "net_profit": round(net, 2),
            "eps": round(random.uniform(5, 20), 2),
            "dividend": round(net * 0.2, 2),
            "tax_rate": round(random.uniform(15, 30), 2)
        })

pd.DataFrame(pl).to_excel("data/raw/profitandloss.xlsx", index=False)

#      BALANCE SHEET     
bs = []
for c in companies:
    assets = random.randint(1000, 3000)

    for y in YEARS:
        assets *= random.uniform(1.05, 1.15)
        equity = assets * random.uniform(0.4, 0.6)
        liabilities = assets - equity

        bs.append({
            "company_id": c["company_id"],
            "year": y,
            "total_assets": round(assets, 2),
            "total_liabilities": round(liabilities, 2),
            "equity": round(equity, 2)
        })

pd.DataFrame(bs).to_excel("data/raw/balancesheet.xlsx", index=False)

#      CASHFLOW     
cf = []
for c in companies:
    for y in YEARS:
        op = random.randint(100, 400)
        inv = random.randint(-250, -50)
        fin = random.randint(-100, 150)

        cf.append({
            "company_id": c["company_id"],
            "year": y,
            "cash_from_operating": op,
            "cash_from_investing": inv,
            "cash_from_financing": fin,
            "net_cash": op + inv + fin
        })

pd.DataFrame(cf).to_excel("data/raw/cashflow.xlsx", index=False)

#      STOCK PRICES     
prices = []
for c in companies:
    for i in range(60):
        prices.append({
            "company_id": c["company_id"],
            "date": f"2023-01-{(i % 28) + 1}",
            "close_price": round(random.uniform(100, 1000), 2)
        })

pd.DataFrame(prices).to_excel("data/raw/stock_prices.xlsx", index=False)

#      RATIOS     
ratios = []
for c in companies:
    for y in YEARS:
        ratios.append({
            "company_id": c["company_id"],
            "year": y,
            "roe": round(random.uniform(5, 25), 2)
        })

pd.DataFrame(ratios).to_excel("data/raw/financial_ratios.xlsx", index=False)

#      DOCUMENTS     
docs = []
for c in companies:
    docs.append({
        "company_id": c["company_id"],
        "url": f"http://company{c['company_id']}.com"
    })
pd.DataFrame(docs).to_excel("data/raw/documents.xlsx", index=False)

#      PROS & CONS     
pc = []
for c in companies:
    pc.append({
        "company_id": c["company_id"],
        "pros": "Strong growth",
        "cons": "High competition"
    })
pd.DataFrame(pc).to_excel("data/raw/prosandcons.xlsx", index=False)

#      PEER GROUPS     
pg = []
for c in companies:
    pg.append({
        "company_id": c["company_id"],
        "peer_id": random.randint(1, NUM_COMPANIES)
    })
pd.DataFrame(pg).to_excel("data/raw/peer_groups.xlsx", index=False)

#      ANALYSIS     
analysis = []
for c in companies:
    analysis.append({
        "company_id": c["company_id"],
        "analysis": "Stable performance"
    })
pd.DataFrame(analysis).to_excel("data/raw/analysis.xlsx", index=False)

print(" ALL 12 FILES GENERATED (FINAL VERSION)")