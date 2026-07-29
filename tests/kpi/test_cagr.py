import pytest

from src.analytics.cagr import calculate_cagr, compute_cagr_series


# =========================
# CORE CAGR TESTS
# =========================

def test_cagr_normal():
    value, flag = calculate_cagr(100, 200, 3)
    assert flag == "NORMAL"
    assert round(value, 2) > 0


def test_cagr_decline_to_loss():
    value, flag = calculate_cagr(100, -50, 3)
    assert value is None
    assert flag == "DECLINE_TO_LOSS"


def test_cagr_turnaround():
    value, flag = calculate_cagr(-100, 50, 3)
    assert value is None
    assert flag == "TURNAROUND"


def test_cagr_both_negative():
    value, flag = calculate_cagr(-100, -50, 3)
    assert value is None
    assert flag == "BOTH_NEGATIVE"


def test_cagr_zero_base():
    value, flag = calculate_cagr(0, 100, 3)
    assert value is None
    assert flag == "ZERO_BASE"


def test_cagr_insufficient_years():
    value, flag = calculate_cagr(100, 200, 0)
    assert value is None
    assert flag == "INSUFFICIENT"


# =========================
# SERIES TESTS
# =========================

def test_series_cagr_3yr():
    values = [100, 120, 140, 200]  # 3-year gap
    value, flag = compute_cagr_series(values, 3)
    assert flag == "NORMAL"
    assert value is not None


def test_series_insufficient_data():
    values = [100, 120]  # not enough
    value, flag = compute_cagr_series(values, 3)
    assert value is None
    assert flag == "INSUFFICIENT"


def test_series_turnaround():
    values = [-100, -50, 20, 80]
    value, flag = compute_cagr_series(values, 3)
    assert value is None
    assert flag == "TURNAROUND"


def test_series_decline_to_loss():
    values = [100, 80, 40, -10]
    value, flag = compute_cagr_series(values, 3)
    assert value is None
    assert flag == "DECLINE_TO_LOSS"