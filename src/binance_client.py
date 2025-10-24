# src/binance_client.py
"""
Binance Futures API wrapper with dry-run support for testing.
"""

import os
import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode
from logger_config import get_logger

logger = get_logger("binance_client")

class BinanceClient:
    def __init__(self, api_key=None, api_secret=None, base_url=None, dry_run=True):
        self.api_key = api_key or os.getenv("BINANCE_API_KEY")
        self.api_secret = api_secret or os.getenv("BINANCE_API_SECRET")
        self.base_url = base_url or os.getenv("BINANCE_BASE_URL", "https://testnet.binancefuture.com")
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        if self.api_key:
            self.session.headers.update({"X-MBX-APIKEY": self.api_key})
        self.dry_run = dry_run

    def _sign(self, params: dict):
        query = urlencode(params)
        signature = hmac.new(self.api_secret.encode(), query.encode(), hashlib.sha256).hexdigest()
        return f"{query}&signature={signature}"

    def _request(self, method, path, params=None, signed=False):
        url = self.base_url.rstrip("/") + path
        params = params or {}
        if signed:
            if not self.api_secret:
                raise RuntimeError("API secret required for signed endpoints.")
            params["timestamp"] = int(time.time() * 1000)
            query = self._sign(params)
            url = f"{url}?{query}"
            resp = self.session.request(method, url)
        else:
            resp = self.session.request(method, url, params=params)

        try:
            data = resp.json()
        except Exception:
            resp.raise_for_status()

        if resp.status_code >= 400:
            logger.error("Binance API error", extra={"code": resp.status_code, "response": data})
            raise RuntimeError(f"Binance API error: {data}")
        return data

    def place_market_order(self, symbol, side, quantity):
        logger.info("Placing market order", extra={"symbol": symbol, "side": side, "quantity": quantity, "dry_run": self.dry_run})
        if self.dry_run:
            return {
                "symbol": symbol, "side": side, "type": "MARKET",
                "origQty": str(quantity), "status": "FILLED",
                "orderId": int(time.time() * 1000) % 1000000000
            }
        params = {"symbol": symbol, "side": side, "type": "MARKET", "quantity": str(quantity)}
        return self._request("POST", "/fapi/v1/order", params=params, signed=True)

    def place_limit_order(self, symbol, side, quantity, price, timeInForce="GTC"):
        logger.info("Placing limit order", extra={"symbol": symbol, "side": side, "quantity": quantity, "price": price, "dry_run": self.dry_run})
        if self.dry_run:
            return {
                "symbol": symbol, "side": side, "type": "LIMIT",
                "price": str(price), "origQty": str(quantity),
                "status": "NEW", "orderId": int(time.time() * 1000) % 1000000000
            }
        params = {"symbol": symbol, "side": side, "type": "LIMIT",
                  "timeInForce": timeInForce, "quantity": str(quantity),
                  "price": str(price)}
        return self._request("POST", "/fapi/v1/order", params=params, signed=True)
