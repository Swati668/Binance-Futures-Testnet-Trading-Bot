def validate_inputs(symbol: str, side: str, order_type: str, quantity: float, price: float = None):
    """Basic validation rules for CLI inputs."""
    if not symbol.isalnum():
        raise ValueError("Symbol must be alphanumeric (e.g., BTCUSDT).")
        
    if side.upper() not in ["BUY", "SELL"]:
        raise ValueError("Side must be either 'BUY' or 'SELL'.")
        
    if order_type.upper() not in ["MARKET", "LIMIT"]:
        raise ValueError("Order type must be either 'MARKET' or 'LIMIT'.")
        
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0.")
        
    if order_type.upper() == "LIMIT" and (price is None or price <= 0):
        raise ValueError("Price is required and must be greater than 0 for LIMIT orders.")