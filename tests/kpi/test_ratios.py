import pytest

from src.analytics.ratios import (
    # Leverage & Coverage
    debt_to_equity,
    high_leverage_flag,
    interest_coverage_ratio,
    icr_label,
    icr_risk_flag,
    net_debt,
    asset_turnover,

    # Profitability
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets
)


# =========================
# LEVERAGE TESTS
# =========================

def test_debt_to_equity_normal():
    assert round(debt_to_equity(500, 200, 300), 2) == 1.00


def test_debt_to_equity_debt_free():
    assert debt_to_equity(0, 200, 300) == 0


def test_debt_to_equity_negative_equity():
    assert debt_to_equity(500, -200, 100) is None


def test_high_leverage_flag_true():
    assert high_leverage_flag(6, sector="Manufacturing") is True


def test_high_leverage_flag_financials():
    assert high_leverage_flag(6, sector="Financials") is False


def test_high_leverage_flag_none():
    assert high_leverage_flag(None, sector="Manufacturing") is False


# =========================
# COVERAGE TESTS
# =========================

def test_icr_interest_zero():
    assert interest_coverage_ratio(200, 50, 0) is None


def test_icr_label_debt_free():
    assert icr_label(None) == "Debt Free"


def test_icr_risk_flag():
    assert icr_risk_flag(1.2) is True


def test_icr_risk_flag_safe():
    assert icr_risk_flag(2.0) is False


# =========================
# PROFITABILITY TESTS
# =========================

def test_net_profit_margin_normal():
    assert round(net_profit_margin(100, 1000), 2) == 10.00


def test_net_profit_margin_zero_sales():
    assert net_profit_margin(100, 0) is None


def test_operating_profit_margin_normal():
    result = operating_profit_margin(200, 1000)
    assert round(result, 2) == 20.00


def test_operating_profit_margin_mismatch():
    result = operating_profit_margin(200, 1000, reported_opm=10)
    assert round(result, 2) == 20.00


def test_opm_logging(caplog):
    operating_profit_margin(
        200,
        1000,
        reported_opm=10,
        company_id=1,
        year=2022
    )
    assert "OPM mismatch" in caplog.text


def test_roe_normal():
    result = return_on_equity(100, 200, 300)
    assert round(result, 2) == 20.00


def test_roe_negative_equity():
    assert return_on_equity(100, -200, 100) is None


def test_roce_normal():
    result = return_on_capital_employed(100, 200, 300, 500)
    assert round(result, 2) == 10.00


def test_roa_zero_assets():
    assert return_on_assets(100, 0) is None


# =========================
# ADDITIONAL METRICS
# =========================

def test_net_debt():
    assert net_debt(500, 200) == 300


def test_asset_turnover_normal():
    assert round(asset_turnover(1000, 500), 2) == 2.00


def test_asset_turnover_zero_assets():
    assert asset_turnover(1000, 0) is None