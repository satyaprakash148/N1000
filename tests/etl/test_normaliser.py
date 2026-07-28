import pytest

from src.etl.normaliser import (
    normalize_year,
    normalize_ticker
)



   
# YEAR TESTS (20+)
   


def test_year_int():
    assert normalize_year(2020) == 2020


def test_year_string():
    assert normalize_year("2021") == 2021


def test_year_float():
    assert normalize_year(2022.0) == 2022


def test_year_float_string():
    assert normalize_year("2022.0") == 2022


def test_year_with_space():
    assert normalize_year(" 2020 ") == 2020


def test_year_with_newline():
    assert normalize_year("\n2021") == 2021


def test_year_fy():
    assert normalize_year("FY20") == 2020


def test_year_fy_caps():
    assert normalize_year("FY21") == 2021


def test_year_fy_full():
    assert normalize_year("FY2023") == 2023


def test_year_2_digit():
    assert normalize_year("19") == 2019


def test_year_old_2_digit():
    assert normalize_year("99") == 1999


def test_year_slash_format():
    assert normalize_year("2020/03/31") == 2020


def test_year_dash_format():
    assert normalize_year("2021-03-31") == 2021


def test_year_invalid_string():
    with pytest.raises(ValueError):
        normalize_year("abc")


def test_year_invalid_format():
    with pytest.raises(ValueError):
        normalize_year("20AB")


def test_year_none():
    with pytest.raises(ValueError):
        normalize_year(None)


def test_year_empty():
    with pytest.raises(ValueError):
        normalize_year("")


def test_year_symbols():
    with pytest.raises(ValueError):
        normalize_year("@@@")



   
# TICKER TESTS (15+)
   


def test_ticker_basic():
    assert normalize_ticker("infy") == "INFY"


def test_ticker_upper():
    assert normalize_ticker("TCS") == "TCS"


def test_ticker_mixed():
    assert normalize_ticker("ReLiAnCe") == "RELIANCE"


def test_ticker_space():
    assert normalize_ticker(" hdfc ") == "HDFC"


def test_ticker_dot():
    assert normalize_ticker("infy.bo") == "INFY"


def test_ticker_dash():
    assert normalize_ticker("tcs.ns") == "TCS"


def test_ticker_numbers_removed():
    assert normalize_ticker("INFY123") == "INFY"


def test_ticker_special_chars():
    assert normalize_ticker("TCS@#") == "TCS"


def test_ticker_middle_symbols():
    assert normalize_ticker("T@C#S") == "TCS"


def test_ticker_exchange():
    assert normalize_ticker("RELIANCE.NS") == "RELIANCE"


def test_ticker_invalid():
    with pytest.raises(ValueError):
        normalize_ticker("")


def test_ticker_none():
    with pytest.raises(ValueError):
        normalize_ticker(None)


def test_ticker_only_symbols():
    with pytest.raises(ValueError):
        normalize_ticker("@@@")


def test_ticker_numeric_only():
    with pytest.raises(ValueError):
        normalize_ticker("12345")


def test_year_future():
    assert normalize_year("2025") == 2025


def test_ticker_lower_with_spaces():
    assert normalize_ticker("  reliance  ") == "RELIANCE"


def test_ticker_dot_exchange_lower():
    assert normalize_ticker("tcs.ns") == "TCS"