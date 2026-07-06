import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode
import os
from dotenv import load_dotenv

load_dotenv()

class BinanceFuturesClient:
    BASE_URL = os.getenv(
    "BASE_URL",
    "https://testnet.binancefuture.com")     

    def __init__(self, logger):
        self.api_key = os.getenv("BINANCE_API_KEY")
        self.api_secret = os.getenv("BINANCE_API_SECRET")
        self.logger = logger
        
        if not self.api_key or not self.api_secret:
            self.logger.error("API Key or Secret missing from environment variables.")
            raise ValueError("API credentials missing.")

    def _generate_signature(self, query_string: str) -> str:
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None):
        endpoint = "/fapi/v1/order"
        url = f"{self.BASE_URL}{endpoint}"
        
        # Base payload required for all orders
        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": order_type.upper(),
            "quantity": quantity,
            "timestamp": int(time.time() * 1000)
        }
        
        if order_type.upper() == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC"  # Good Till Cancelled (Required for Limit)

        # Generate Signature
        query_string = urlencode(params)
        signature = self._generate_signature(query_string)
        params["signature"] = signature

        headers = {
            "X-MBX-APIKEY": self.api_key
        }

        self.logger.info(f"Sending Request: {order_type} {side} {quantity} {symbol}")

        try:
            response = requests.post(url, headers=headers, data=params, timeout=10)
            response_json = response.json()
            
            if response.status_code == 200:
                self.logger.info(f"Order Success! OrderID: {response_json.get('orderId')}")
                return True, response_json
            else:
                self.logger.error(f"API Error ({response.status_code}): {response_json.get('msg')}")
                return False, response_json
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Network / Connection error occurred: {str(e)}")
            return False, {"error": "Network error", "details": str(e)}