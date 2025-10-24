# src/advanced/twap.py
"""
TWAP (Time-Weighted Average Price) strategy simulation.
Splits a total quantity into smaller market orders over time.
"""

import time
from binance_client import BinanceClient
from validation import validate_symbol, validate_side, validate_positive_number
from logger_config import get_logger

logger = get_logger("twap")

def place_twap(symbol, side, total_quantity, slices=5, interval=5, dry_run=True):
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    total_quantity = validate_positive_number(total_quantity, "total_quantity")
    slices = int(validate_positive_number(slices, "slices"))
    interval = int(validate_positive_number(interval, "interval_seconds"))

    client = BinanceClient(dry_run=dry_run)
    qty_per_slice = round(total_quantity / slices, 6)

    logger.info("Starting TWAP strategy", extra={"symbol": symbol, "side": side,
                                                 "total_quantity": total_quantity,
                                                 "slices": slices, "interval": interval})

    results = []
    for i in range(slices):
        logger.info(f"TWAP slice {i+1}/{slices}", extra={"quantity": qty_per_slice})
        res = client.place_market_order(symbol, side, qty_per_slice)
        results.append(res)
        if i < slices - 1:
            time.sleep(interval)

    logger.info("TWAP execution finished", extra={"total_orders": len(results)})
    return results
