# src/market_orders.py
from binance_client import BinanceClient
from validation import validate_symbol, validate_side, validate_positive_number
from logger_config import get_logger

logger = get_logger("market_orders")

def place_market(symbol, side, quantity, dry_run=True):
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    quantity = validate_positive_number(quantity, "quantity")

    client = BinanceClient(dry_run=dry_run)
    result = client.place_market_order(symbol, side, quantity)

    logger.info("Market order response", extra={"response": result})
    return result
