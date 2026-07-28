import re


def normalize_year(year):
    """
    Normalize different year formats into integer year.

    Supported:
    2020
    "2020"
    2020.0
    "FY20"
    "FY2021"
    "2020-03-31"
    "2020/03/31"
    "19" -> 2019
    """

    if year is None:
        raise ValueError("Year cannot be None")

    year_str = str(year).strip()

    if year_str == "":
        raise ValueError("Year cannot be empty")


    # Remove FY prefix
    if year_str.upper().startswith("FY"):
        year_str = year_str[2:]


    # Float year
    if re.match(r"^\d+\.\d+$", year_str):
        return int(float(year_str))


    # Date formats
    if "-" in year_str or "/" in year_str:
        first_part = year_str[:4]

        if first_part.isdigit():
            return int(first_part)


    # Two digit year handling
    if re.match(r"^\d{2}$", year_str):

        year = int(year_str)

        if year >= 50:
            return 1900 + year

        return 2000 + year


    # Four digit year
    if re.match(r"^\d{4}$", year_str):
        return int(year_str)


    raise ValueError(f"Invalid year format: {year}")



def normalize_ticker(ticker):
    """
    Normalize company ticker symbol.

    Examples:
    infy -> INFY
    infy.ns -> INFY
    INFY123 -> INFY
    TCS@# -> TCS
    """

    if ticker is None:
        raise ValueError("Ticker cannot be None")


    ticker_str = str(ticker).strip()


    if ticker_str == "":
        raise ValueError("Ticker cannot be empty")


    # Remove exchange suffix
    ticker_str = ticker_str.split(".")[0]


    # Keep only alphabets
    ticker_str = re.sub(
        r"[^A-Za-z]",
        "",
        ticker_str
    )


    if ticker_str == "":
        raise ValueError("Invalid ticker")


    return ticker_str.upper()