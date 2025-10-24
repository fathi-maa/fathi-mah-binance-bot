# src/advanced/oco.py
"""
Simulated OCO (One Cancels the Other) order logic.
"""

import time
from binance_client import BinanceClient
from validation import validate_symbol, validate_side, validate_positive_number
from logger_config import get_logger

logger = get_logger("oco")

def place_oco(symbol, side, quantity, limit_price, stop_price, dry_run=True):
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    quantity = validate_positive_number(quantity, "quantity")
    limit_price = validate_positive_number(limit_price, "limit_price")
    stop_price = validate_positive_number(stop_price, "stop_price")

    client = BinanceClient(dry_run=dry_run)

    logger.info("Creating OCO orders", extra={"symbol": symbol, "side": side,
                                              "limit_price": limit_price, "stop_price": stop_price})

    limit_order = client.place_limit_order(symbol, side, quantity, limit_price)
    stop_order = {
        "symbol": symbol, "side": side, "type": "STOP_LIMIT",
        "stopPrice": stop_price, "status": "NEW",
        "orderId": int(time.time() * 1000) % 1000000000
    }

    if dry_run:
        logger.info("Dry-run: Simulating OCO trigger and cancellation")
        limit_order["status"] = "CANCELED"
        stop_order["status"] = "FILLED"

    logger.info("OCO complete", extra={"limit_order": limit_order, "stop_order": stop_order})
    return {"limit_order": limit_order, "stop_order": stop_order}
