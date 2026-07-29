import pandas as pd
from typing import Optional
from src.analytics.cashflow_kpis import capital_allocation_pattern


def safe_ratio(numerator: float, denominator: float) -> Optional[float]:
    """
    Safe division helper
    """
    if denominator in (0, None) or pd.isna(denominator):
        return None
    return numerator / denominator


def generate_capital_allocation(df: pd.DataFrame, output_path: str):
    rows = []

    for _, r in df.iterrows():
        cfo = r.get("operating_activity")
        cfi = r.get("investing_activity")
        cff = r.get("financing_activity")
        net_profit = r.get("net_profit")

        # Handle NaN safely
        if pd.isna(cfo):
            cfo = 0
        if pd.isna(cfi):
            cfi = 0
        if pd.isna(cff):
            cff = 0

        cfo_pat_ratio = safe_ratio(cfo, net_profit)

        s_cfo, s_cfi, s_cff, label = capital_allocation_pattern(
            cfo, cfi, cff, cfo_pat_ratio
        )

        rows.append({
            "company_id": r.get("company_id"),
            "year": r.get("year"),
            "cfo_sign": s_cfo,
            "cfi_sign": s_cfi,
            "cff_sign": s_cff,
            "pattern_label": label
        })

    pd.DataFrame(rows).to_csv(output_path, index=False)


# =========================
# ENTRY POINT
# =========================

if __name__ == "__main__":

    input_path = "data/processed/cashflow.csv"
    output_path = "output/capital_allocation.csv"

    df = pd.read_csv(input_path)

    generate_capital_allocation(df, output_path)

    print(f"✅ File generated at: {output_path}")