from .client import BinanceFuturesClient

def place_order(client: BinanceFuturesClient, symbol: str, side: str, order_type: str, quantity: float, price: float = None, stop_price: float = None):
    endpoint = '/fapi/v1/order'
    
    params = {
        'symbol': symbol,
        'side': side,
        'type': order_type,
        'quantity': quantity
    }
    
    if order_type == 'LIMIT':
        if price is None:
            raise ValueError("Price is required for LIMIT orders")
        params['price'] = price
        params['timeInForce'] = 'GTC'
        
    elif order_type == 'STOP_MARKET':
        if stop_price is None:
            raise ValueError("stopPrice is required for STOP_MARKET orders")
        params['stopPrice'] = stop_price
        # Note: STOP_MARKET evaluates to standard market execution when stop is hit
    
    return client._request('POST', endpoint, params)
