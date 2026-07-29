import pytest

from src.analytics.cashflow_kpis import (
    free_cash_flow,
    fcf_conversion_rate,
    cfo_quality_score,
    capex_intensity,
    capital_allocation_pattern
)


def test_fcf():
    assert free_cash_flow(500, -200) == 300


def test_fcf_conversion():
    assert round(fcf_conversion_rate(300, 600), 2) == 50.00


def test_fcf_conversion_zero_op():
    assert fcf_conversion_rate(300, 0) is None


def test_cfo_quality_high():
    ratio, label = cfo_quality_score([100, 120], [80, 100])
    assert label == "HIGH_QUALITY"


def test_cfo_quality_moderate():
    ratio, label = cfo_quality_score([50, 60], [100, 100])
    assert label == "MODERATE"


def test_cfo_quality_accrual():
    ratio, label = cfo_quality_score([20, 30], [100, 100])
    assert label == "ACCRUAL_RISK"


def test_capex_intensity_asset_light():
    _, label = capex_intensity(-10, 1000)
    assert label == "ASSET_LIGHT"


def test_capital_pattern_reinvestor():
    _, _, _, label = capital_allocation_pattern(100, -50, -20)
    assert label == "REINVESTOR"


def test_capital_pattern_shareholder():
    _, _, _, label = capital_allocation_pattern(100, -50, -20, cfo_pat_ratio=1.5)
    assert label == "SHAREHOLDER_RETURNS"


def test_capital_pattern_distress():
    _, _, _, label = capital_allocation_pattern(-100, 50, 50)
    assert label == "DISTRESS_SIGNAL"