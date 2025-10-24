# src/cli.py
"""
Command-line interface for the Binance Futures CLI Bot.
Usage examples:
  python -m src.cli market BTCUSDT BUY 0.001
  python -m src.cli limit BTCUSDT SELL 0.01 62000
"""

import argparse
#from src.market_orders import place_market
from market_orders import place_market
from limit_orders import place_limit
from logger_config import get_logger

logger = get_logger("cli")

def main():
    parser = argparse.ArgumentParser(description="Binance Futures CLI Bot")
    sub = parser.add_subparsers(dest="command", required=True)

    # Market order command
    p_market = sub.add_parser("market", help="Place a market order")
    p_market.add_argument("symbol", type=str)
    p_market.add_argument("side", type=str, choices=["BUY", "SELL"])
    p_market.add_argument("quantity", type=float)
    p_market.add_argument("--dry-run", action="store_true", default=True)
    p_market.add_argument("--no-dry-run", dest="dry_run", action="store_false")

    # Limit order command
    p_limit = sub.add_parser("limit", help="Place a limit order")
    p_limit.add_argument("symbol", type=str)
    p_limit.add_argument("side", type=str, choices=["BUY", "SELL"])
    p_limit.add_argument("quantity", type=float)
    p_limit.add_argument("price", type=float)
    p_limit.add_argument("--timeInForce", type=str, default="GTC")
    p_limit.add_argument("--dry-run", action="store_true", default=True)
    p_limit.add_argument("--no-dry-run", dest="dry_run", action="store_false")

    args = parser.parse_args()

    try:
        if args.command == "market":
            res = place_market(args.symbol, args.side, args.quantity, dry_run=args.dry_run)
            print("Result:", res)
        elif args.command == "limit":
            res = place_limit(args.symbol, args.side, args.quantity, args.price, args.timeInForce, args.dry_run)
            print("Result:", res)
    except Exception as e:
        logger.exception("Error executing command")
        print("Error:", str(e))

if __name__ == "__main__":
    main()
