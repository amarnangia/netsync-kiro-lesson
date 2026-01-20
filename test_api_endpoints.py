"""
Test different API endpoint formats to find the correct one
This helps identify the correct Massive API URL structure
"""

import os
import time
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

def test_endpoint(base_url, endpoint_format, ticker="AAPL"):
    """Test a specific API endpoint format"""
    api_key = os.getenv("MASSIVE_API_KEY")
    
    # Build URL
    url = f"{base_url}/{endpoint_format.format(ticker=ticker)}"
    
    print(f"\nTesting: {url}")
    
    # Try different parameter formats
    param_formats = [
        {"apikey": api_key},  # Some APIs use 'apikey'
        {"api_key": api_key},  # Others use 'api_key'
        {"token": api_key},    # Some use 'token'
        {"key": api_key},      # Some use 'key'
    ]
    
    for params in param_formats:
        try:
            response = requests.get(url, params=params, timeout=5)
            print(f"  Params: {list(params.keys())[0]} -> Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"  ✓ SUCCESS with params: {list(params.keys())[0]}")
                return True, url, params
            elif response.status_code == 401:
                print(f"    (401 - Auth issue, but endpoint exists)")
            elif response.status_code == 404:
                print(f"    (404 - Endpoint not found)")
                
        except Exception as e:
            print(f"  Error: {e}")
    
    return False, url, None

def main():
    print("=" * 70)
    print("Massive API Endpoint Discovery")
    print("=" * 70)
    
    api_key = os.getenv("MASSIVE_API_KEY")
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        print("❌ API key not configured properly")
        return
    
    print(f"✓ API key loaded: {api_key[:8]}...{api_key[-4:]}")
    print("\nTrying different endpoint formats...")
    print("(This will make multiple API calls - respecting rate limits)")
    
    # Common API base URLs and endpoint formats
    test_cases = [
        ("https://api.massive.com/v1", "stock/{ticker}"),
        ("https://api.massive.com/v1", "stocks/{ticker}"),
        ("https://api.massive.com/v1", "quote/{ticker}"),
        ("https://api.massive.com/v1", "{ticker}"),
        ("https://api.massive.com", "v1/stock/{ticker}"),
        ("https://api.massive.com", "stock/{ticker}"),
        ("https://massive.com/api/v1", "stock/{ticker}"),
    ]
    
    for i, (base_url, endpoint_format) in enumerate(test_cases):
        if i > 0:
            print("\nWaiting 3 seconds (rate limit)...")
            time.sleep(3)
        
        success, url, params = test_endpoint(base_url, endpoint_format)
        if success:
            print("\n" + "=" * 70)
            print("✓ FOUND WORKING ENDPOINT!")
            print("=" * 70)
            print(f"Base URL: {base_url}")
            print(f"Endpoint: {endpoint_format}")
            print(f"Full URL: {url}")
            print(f"Params: {params}")
            print("\nUpdate stock_explorer.py with:")
            print(f'  API_BASE_URL = "{base_url}"')
            return
    
    print("\n" + "=" * 70)
    print("Could not find working endpoint")
    print("=" * 70)
    print("\nPlease provide the correct API documentation URL")
    print("The Massive API documentation should specify:")
    print("  1. Base URL (e.g., https://api.massive.com)")
    print("  2. Endpoint format (e.g., /v1/stock/{symbol})")
    print("  3. Parameter name for API key (e.g., 'apikey' or 'token')")

if __name__ == "__main__":
    main()
