import math
from typing import List, Tuple, Optional


# =========================
# CORE CAGR FUNCTION
# =========================

def calculate_cagr(start: float, end: float, years: int) -> Tuple[Optional[float], str]:
    """
    Returns (cagr_value, flag)

    Flags:
    - NORMAL
    - DECLINE_TO_LOSS
    - TURNAROUND
    - BOTH_NEGATIVE
    - ZERO_BASE
    - INSUFFICIENT
    """

    # Insufficient years
    if years <= 0:
        return None, "INSUFFICIENT"

    # Zero base
    if start == 0:
        return None, "ZERO_BASE"

    # Positive → Positive
    if start > 0 and end > 0:
        cagr = (math.pow(end / start, 1 / years) - 1) * 100
        return cagr, "NORMAL"

    # Positive → Negative
    if start > 0 and end < 0:
        return None, "DECLINE_TO_LOSS"

    # Negative → Positive
    if start < 0 and end > 0:
        return None, "TURNAROUND"

    # Negative → Negative
    if start < 0 and end < 0:
        return None, "BOTH_NEGATIVE"

    return None, "INSUFFICIENT"


# =========================
# SERIES CAGR (GENERIC)
# =========================

def compute_cagr_series(values: List[float], years: int) -> Tuple[Optional[float], str]:
    """
    values: ordered list (oldest → latest)
    years: 3 / 5 / 10
    """

    if not values or len(values) <= years:
        return None, "INSUFFICIENT"

    start = values[-(years + 1)]
    end = values[-1]

    return calculate_cagr(start, end, years)


# =========================
# METRIC-SPECIFIC HELPERS
# =========================

def revenue_cagr(values: List[float], years: int):
    return compute_cagr_series(values, years)


def pat_cagr(values: List[float], years: int):
    return compute_cagr_series(values, years)


def eps_cagr(values: List[float], years: int):
    return compute_cagr_series(values, years)