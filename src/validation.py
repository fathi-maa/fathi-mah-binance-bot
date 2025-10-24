# src/validation.py
"""
Validation helpers for user inputs like symbol, side, quantity, price.
"""

import re

VALID_SIDES = {"BUY", "SELL"}

def validate_symbol(symbol: str):
    if not symbol or not isinstance(symbol, str):
        raise ValueError("Symbol must be a non-empty string (e.g., BTCUSDT).")
    if not re.match(r"^[A-Z0-9]{3,12}$", symbol):
        raise ValueError("Invalid symbol format. Example: BTCUSDT")
    return symbol.upper()

def validate_side(side: str):
    if not side:
        raise ValueError("Side is required (BUY or SELL).")
    side = side.upper()
    if side not in VALID_SIDES:
        raise ValueError("Side must be BUY or SELL.")
    return side

def validate_positive_number(value, name="value"):
    try:
        val = float(value)
    except Exception:
        raise ValueError(f"{name} must be a number.")
    if val <= 0:
        raise ValueError(f"{name} must be greater than zero.")
    return val
