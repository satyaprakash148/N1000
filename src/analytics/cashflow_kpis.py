from typing import List, Optional, Tuple


# =========================
# BASIC METRICS
# =========================

def free_cash_flow(cfo: float, cfi: float) -> float:
    """
    FCF = Operating Activity + Investing Activity
    (Note: investing_activity is usually negative)
    """
    return cfo + cfi


def fcf_conversion_rate(fcf: float, operating_profit: float) -> Optional[float]:
    if operating_profit == 0:
        return None
    return (fcf / operating_profit) * 100


# =========================
# CFO QUALITY
# =========================

def cfo_quality_score(cfo_list: List[float], pat_list: List[float]) -> Tuple[Optional[float], str]:
    """
    Average (CFO / PAT) over 5 years
    """

    if not cfo_list or not pat_list or len(cfo_list) != len(pat_list):
        return None, "INSUFFICIENT"

    ratios = []

    for cfo, pat in zip(cfo_list, pat_list):
        if pat == 0:
            return None, "INVALID_PAT"
        ratios.append(cfo / pat)

    avg_ratio = sum(ratios) / len(ratios)

    if avg_ratio > 1.0:
        label = "HIGH_QUALITY"
    elif avg_ratio >= 0.5:
        label = "MODERATE"
    else:
        label = "ACCRUAL_RISK"

    return avg_ratio, label


# =========================
# CAPEX INTENSITY
# =========================

def capex_intensity(investing_activity: float, sales: float) -> Tuple[Optional[float], str]:
    if sales == 0:
        return None, "INSUFFICIENT"

    intensity = abs(investing_activity) / sales * 100

    if intensity < 3:
        label = "ASSET_LIGHT"
    elif intensity <= 8:
        label = "MODERATE"
    else:
        label = "CAPITAL_INTENSIVE"

    return intensity, label


# =========================
# CAPITAL ALLOCATION PATTERN
# =========================

def _sign(value: float) -> str:
    if value > 0:
        return "+"
    if value < 0:
        return "-"
    return "0"


def capital_allocation_pattern(
    cfo: float,
    cfi: float,
    cff: float,
    cfo_pat_ratio: Optional[float] = None
) -> Tuple[str, str, str, str]:
    """
    Returns:
    (cfo_sign, cfi_sign, cff_sign, pattern_label)
    """

    s_cfo = _sign(cfo)
    s_cfi = _sign(cfi)
    s_cff = _sign(cff)

    pattern = (s_cfo, s_cfi, s_cff)

    # Mapping logic
    if pattern == ("+", "-", "-"):
        if cfo_pat_ratio is not None and cfo_pat_ratio > 1:
            label = "SHAREHOLDER_RETURNS"
        else:
            label = "REINVESTOR"

    elif pattern == ("+", "+", "-"):
        label = "LIQUIDATING_ASSETS"

    elif pattern == ("-", "+", "+"):
        label = "DISTRESS_SIGNAL"

    elif pattern == ("-", "-", "+"):
        label = "GROWTH_FUNDED_BY_DEBT"

    elif pattern == ("+", "+", "+"):
        label = "CASH_ACCUMULATOR"

    elif pattern == ("-", "-", "-"):
        label = "PRE_REVENUE"

    elif pattern == ("+", "-", "+"):
        label = "MIXED"

    else:
        label = "UNKNOWN"

    return s_cfo, s_cfi, s_cff, label