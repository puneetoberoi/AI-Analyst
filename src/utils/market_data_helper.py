# src/utils/market_data_helper.py
import yfinance as yf
import time
import random
from functools import wraps
import finnhub
import os

def retry_with_backoff(retries=3, backoff_in_seconds=1):
    """Decorator for retrying with exponential backoff"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            x = backoff_in_seconds
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == retries - 1:
                        raise e
                    sleep_time = (x * 2 ** i + random.uniform(0, 1))
                    print(f"Rate limited, waiting {sleep_time:.2f}s...")
                    time.sleep(sleep_time)
            return None
        return wrapper
    return decorator

class MarketDataFetcher:
    def __init__(self):
        self.finnhub_client = finnhub.Client(api_key=os.environ.get('FINNHUB_KEY', ''))
        
    @retry_with_backoff(retries=3, backoff_in_seconds=2)
    def get_stock_price_yfinance(self, symbol):
        """Get stock price with retry logic"""
        ticker = yf.Ticker(symbol)
        # Use history instead of info (less rate limited)
        hist = ticker.history(period="1d")
        if not hist.empty:
            return {
                'symbol': symbol,
                'price': hist['Close'].iloc[-1],
                'volume': hist['Volume'].iloc[-1],
                'source': 'yfinance'
            }
        return None
    
    def get_stock_price_finnhub(self, symbol):
        """Fallback to Finnhub"""
        try:
            quote = self.finnhub_client.quote(symbol)
            return {
                'symbol': symbol,
                'price': quote['c'],  # current price
                'volume': quote['v'],  # volume
                'source': 'finnhub'
            }
        except Exception as e:
            print(f"Finnhub error: {e}")
            return None
    
    def get_stock_price(self, symbol):
        """Get price with fallback sources"""
        # Try yfinance first
        try:
            return self.get_stock_price_yfinance(symbol)
        except:
            pass
        
        # Fallback to finnhub
        try:
            return self.get_stock_price_finnhub(symbol)
        except:
            pass
        
        # Final fallback - return dummy data for testing
        return {
            'symbol': symbol,
            'price': 150.00,  # dummy price
            'volume': 1000000,
            'source': 'dummy',
            'note': 'Using dummy data due to API limits'
        }
