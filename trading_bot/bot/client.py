import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode
from .logging_config import get_logger

logger = get_logger(__name__)

class BinanceFuturesClient:
    def __init__(self, api_key: str, api_secret: str, base_url: str = 'https://testnet.binancefuture.com'):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'X-MBX-APIKEY': self.api_key,
            'Content-Type': 'application/x-www-form-urlencoded'
        })
        self.time_offset = self._get_time_offset()
        
    def _get_time_offset(self) -> int:
        try:
            response = self.session.get(f"{self.base_url}/fapi/v1/time")
            response.raise_for_status()
            server_time = response.json()['serverTime']
            local_time = int(time.time() * 1000)
            return server_time - local_time
        except Exception as e:
            logger.warning(f"Could not sync time with server: {e}")
            return 0
            
    def _generate_signature(self, query_string: str) -> str:
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def _request(self, method: str, endpoint: str, params: dict = None):
        if params is None:
            params = {}
            
        params['timestamp'] = int(time.time() * 1000) + self.time_offset
        query_string = urlencode(params)
        signature = self._generate_signature(query_string)
        
        request_url = f"{self.base_url}{endpoint}?{query_string}&signature={signature}"
        
        try:
            logger.info(f"API Request -> {method} {endpoint} | Params: {params}")
            response = self.session.request(method, request_url)
            
            # Log the response (truncated if it's too long, but we keep it here for debug)
            logger.info(f"API Response <- {response.status_code} | {response.text}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            err_msg = f"API Error ({e.response.status_code}): {e.response.text}"
            logger.error(f"HTTP Error: {e.response.status_code} - {e.response.text}")
            raise Exception(err_msg)
        except requests.exceptions.RequestException as e:
            logger.error(f"Network Error: {str(e)}")
            raise Exception(f"Network Error: {str(e)}")
