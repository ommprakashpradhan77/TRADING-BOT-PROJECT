def validate_symbol(symbol: str):
    if not symbol.isalnum() or len(symbol) < 3:
        raise ValueError("Invalid symbol format. Use e.g. BTCUSDT")

def validate_side(side: str):
    if side not in ["BUY", "SELL"]:
        raise ValueError("Side must be BUY or SELL")
        
def validate_order_type(order_type: str):
    if order_type not in ["MARKET", "LIMIT", "STOP_MARKET"]:
        raise ValueError("Order type must be MARKET, LIMIT, or STOP_MARKET")

def validate_quantity(quantity: float):
    if quantity <= 0:
        raise ValueError("Quantity must be strictly positive")
