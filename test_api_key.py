"""
Test script to verify API key is working correctly
This script makes a single API call to test the configuration
"""

import os
import time
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

def test_api_key():
    """Test if the API key is configured and working"""
    
    print("=" * 60)
    print("API Key Configuration Test")
    print("=" * 60)
    
    # Check if API key is loaded
    api_key = os.getenv("MASSIVE_API_KEY")
    
    if not api_key:
        print("❌ ERROR: MASSIVE_API_KEY not found in environment")
        print("   Make sure .env file exists and contains MASSIVE_API_KEY")
        return False
    
    if api_key == "YOUR_API_KEY_HERE":
        print("❌ ERROR: API key is still the placeholder value")
        print("   Edit .env file and replace YOUR_API_KEY_HERE with your actual key")
        return False
    
    print(f"✓ API key loaded from .env file")
    print(f"  Key length: {len(api_key)} characters")
    print(f"  Key preview: {api_key[:8]}...{api_key[-4:]}")
    print()
    
    # Test API call
    print("Testing API connection...")
    print("Making 1 API call (respecting rate limit)...")
    print()
    
    # API configuration
    API_BASE_URL = "https://api.massive.com"
    ticker = "AAPL"
    
    # Calculate date range (up to 2 years)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)
    
    # Build request using Massive aggregates endpoint
    # Format: /v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{from}/{to}
    url = f"{API_BASE_URL}/v2/aggs/ticker/{ticker}/range/1/day/{start_date.strftime('%Y-%m-%d')}/{end_date.strftime('%Y-%m-%d')}"
    params = {
        "apiKey": api_key  # Massive uses 'apiKey' parameter
    }
    
    print(f"Request URL: {url}")
    print(f"Ticker: {ticker}")
    print(f"Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    print()
    
    try:
        # Make the API call
        start_time = time.time()
        response = requests.get(url, params=params, timeout=10)
        elapsed_time = time.time() - start_time
        
        print(f"Response received in {elapsed_time:.2f} seconds")
        print(f"Status code: {response.status_code}")
        print()
        
        # Check response
        if response.status_code == 200:
            print("✓ SUCCESS: API call successful!")
            print()
            
            # Try to parse JSON
            try:
                data = response.json()
                print("✓ Response is valid JSON")
                print(f"  Response keys: {list(data.keys())}")
                
                # Show a preview of the data
                if isinstance(data, dict):
                    print()
                    print("Response preview:")
                    print("-" * 60)
                    import json
                    print(json.dumps(data, indent=2)[:500] + "...")
                    print("-" * 60)
                
                print()
                print("✓ Your API key is working correctly!")
                print("✓ The application is ready to use")
                return True
                
            except Exception as e:
                print(f"⚠ Warning: Could not parse JSON response: {e}")
                print(f"  Raw response: {response.text[:200]}...")
                return False
                
        elif response.status_code == 401:
            print("❌ ERROR: Authentication failed (401 Unauthorized)")
            print("   Your API key may be invalid or expired")
            print("   Please check your API key in the .env file")
            return False
            
        elif response.status_code == 403:
            print("❌ ERROR: Access forbidden (403 Forbidden)")
            print("   Your API key may not have permission to access this endpoint")
            return False
            
        elif response.status_code == 429:
            print("⚠ WARNING: Rate limit exceeded (429 Too Many Requests)")
            print("   You've made too many requests. Wait 60 seconds and try again")
            return False
            
        elif response.status_code == 404:
            print("⚠ WARNING: Endpoint not found (404 Not Found)")
            print("   The API URL may be incorrect")
            print("   Note: This test uses a placeholder URL - update API_BASE_URL in stock_explorer.py")
            print("   with the actual Massive API URL from their documentation")
            return False
            
        else:
            print(f"⚠ WARNING: Unexpected status code: {response.status_code}")
            print(f"  Response: {response.text[:200]}...")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Connection failed")
        print("   Could not connect to the API server")
        print("   Check your internet connection")
        print("   Note: The API URL may need to be updated with the actual Massive API endpoint")
        return False
        
    except requests.exceptions.Timeout:
        print("❌ ERROR: Request timed out")
        print("   The API server took too long to respond")
        return False
        
    except Exception as e:
        print(f"❌ ERROR: Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_api_key()
    print()
    print("=" * 60)
    if success:
        print("✓ Test completed successfully!")
        print()
        print("Next steps:")
        print("  1. Run the application: streamlit run stock_explorer.py")
        print("  2. Select a stock ticker")
        print("  3. View real API data in Stage 2 section")
        print()
        print("Remember: Rate limit is 5 calls per minute (12 seconds between calls)")
    else:
        print("✗ Test failed - please fix the issues above")
        print()
        print("Common solutions:")
        print("  1. Check that .env file exists and contains your API key")
        print("  2. Verify your API key is correct (check with API provider)")
        print("  3. Update API_BASE_URL in stock_explorer.py with actual endpoint")
        print("  4. Check your internet connection")
    print("=" * 60)
