import logging
from typing import Optional

logger = logging.getLogger(__name__)


# =========================
# PROFITABILITY RATIOS
# =========================

def net_profit_margin(net_profit: float, sales: float) -> Optional[float]:
    """
    Net Profit Margin = (net_profit / sales) * 100

    Returns:
        None if sales == 0
    """
    if sales == 0:
        return None

    return (net_profit / sales) * 100


def operating_profit_margin(
    operating_profit: float,
    sales: float,
    reported_opm: Optional[float] = None,
    company_id: Optional[int] = None,
    year: Optional[int] = None
) -> Optional[float]:
    """
    Operating Profit Margin (OPM) = (operating_profit / sales) * 100

    Cross-check:
        Logs warning if difference between computed and reported OPM > 1%
    """
    if sales == 0:
        return None

    computed_opm = (operating_profit / sales) * 100

    if reported_opm is not None:
        diff = abs(computed_opm - reported_opm)

        if diff > 1:
            logger.warning(
                "OPM mismatch | Company: %s, Year: %s, Computed: %.2f, Reported: %.2f",
                company_id,
                year,
                computed_opm,
                reported_opm
            )

    return computed_opm


def return_on_equity(
    net_profit: float,
    equity_capital: float,
    reserves: float
) -> Optional[float]:
    """
    ROE = net_profit / (equity_capital + reserves) * 100

    Returns:
        None if equity <= 0
    """
    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return (net_profit / equity) * 100


def return_on_capital_employed(
    ebit: float,
    equity_capital: float,
    reserves: float,
    borrowings: float,
    sector: Optional[str] = None
) -> Optional[float]:
    """
    ROCE = EBIT / (equity + reserves + borrowings) * 100

    Note:
        Financials sector handled downstream (benchmark-based evaluation)
    """
    capital = equity_capital + reserves + borrowings

    if capital <= 0:
        return None

    return (ebit / capital) * 100


def return_on_assets(net_profit: float, total_assets: float) -> Optional[float]:
    """
    ROA = net_profit / total_assets * 100

    Returns:
        None if total_assets == 0
    """
    if total_assets == 0:
        return None

    return (net_profit / total_assets) * 100


# =========================
# LEVERAGE RATIOS
# =========================

def debt_to_equity(
    borrowings: float,
    equity_capital: float,
    reserves: float
) -> Optional[float]:
    """
    Debt-to-Equity Ratio = borrowings / (equity_capital + reserves)

    Rules:
        - borrowings == 0 → 0 (debt-free)
        - equity <= 0 → None
    """
    equity = equity_capital + reserves

    if borrowings == 0:
        return 0.0

    if equity <= 0:
        return None

    return borrowings / equity


def high_leverage_flag(
    de_ratio: Optional[float],
    sector: Optional[str] = None
) -> bool:
    """
    High leverage flag:
        - True if D/E > 5 and sector != Financials
    """
    if de_ratio is None:
        return False

    if sector == "Financials":
        return False

    return de_ratio > 5


# =========================
# COVERAGE RATIOS
# =========================

def interest_coverage_ratio(
    operating_profit: float,
    other_income: float,
    interest: float
) -> Optional[float]:
    """
    ICR = (operating_profit + other_income) / interest

    Returns:
        None if interest == 0 (debt-free)
    """
    if interest == 0:
        return None

    return (operating_profit + other_income) / interest


def icr_label(icr: Optional[float]) -> Optional[str]:
    """
    Label for ICR:
        - None → "Debt Free"
    """
    if icr is None:
        return "Debt Free"

    return None


def icr_risk_flag(icr: Optional[float]) -> bool:
    """
    Risk flag:
        - True if ICR < 1.5
    """
    if icr is None:
        return False

    return icr < 1.5


# =========================
# ADDITIONAL METRICS
# =========================

def net_debt(borrowings: float, investments: float) -> float:
    """
    Net Debt = borrowings - investments
    """
    return borrowings - investments


def asset_turnover(sales: float, total_assets: float) -> Optional[float]:
    """
    Asset Turnover = sales / total_assets

    Returns:
        None if total_assets == 0
    """
    if total_assets == 0:
        return None

    return sales / total_assets