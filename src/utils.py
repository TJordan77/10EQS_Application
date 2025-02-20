import re
import datetime

def clean_price(price_str):
    """
    Cleans the price string and returns a float value.
    Handles cases like '$12.99', '14.99', or empty values.
    Returns None if the price is not convertible to float.
    """
    if not price_str:
        return None
    # Remove $ or other non-numeric characters except dot
    clean_str = re.sub(r'[^\d\.]', '', price_str)
    try:
        return float(clean_str)
    except ValueError:
        return None

def clean_stock(stock_str):
    """
    Converts the stock string to an integer.
    If 'out of stock', returns 0.
    Returns None if unconvertible and not 'out of stock'.
    """
    if isinstance(stock_str, str) and stock_str.lower() == 'out of stock':
        return 0
    try:
        return int(stock_str)
    except ValueError:
        return None

def clean_category(cat_str):
    """
    Normalizes category strings by capitalizing first letter,
    or uses a predefined map if you want consistent categories.
    """
    if not cat_str:
        return None
    return cat_str.strip().capitalize()

def clean_date(date_str):
    """
    Attempts to parse the date in multiple formats into YYYY-MM-DD.
    Returns a string in the format YYYY-MM-DD or None if parsing fails.
    """
    if not date_str:
        return None

    possible_formats = ["%Y-%m-%d", "%m/%d/%Y", "%Y-%m-%dT%H:%M:%S"]
    for fmt in possible_formats:
        try:
            parsed_date = datetime.datetime.strptime(date_str, fmt)
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None
