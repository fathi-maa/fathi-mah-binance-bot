# src/limit_orders.py
from binance_client import BinanceClient
from validation import validate_symbol, validate_side, validate_positive_number
from logger_config import get_logger

logger = get_logger("limit_orders")

def place_limit(symbol, side, quantity, price, timeInForce="GTC", dry_run=True):
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    quantity = validate_positive_number(quantity, "quantity")
    price = validate_positive_number(price, "price")

    client = BinanceClient(dry_run=dry_run)
    result = client.place_limit_order(symbol, side, quantity, price, timeInForce)

    logger.info("Limit order response", extra={"response": result})
    return result
