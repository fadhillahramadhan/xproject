"""
Simple test script to diagnose Yahoo Finance connectivity issues
"""

import yfinance as yf
import pandas as pd
import requests
from datetime import datetime

def test_internet_connection():
    """Test basic internet connectivity"""
    try:
        response = requests.get("https://www.google.com", timeout=5)
        print("✅ Internet connection: OK")
        return True
    except:
        print("❌ Internet connection: FAILED")
        return False

def test_yahoo_finance_direct():
    """Test Yahoo Finance API directly"""
    try:
        # Test with a simple request
        url = "https://query1.finance.yahoo.com/v8/finance/chart/AAPL"
        response = requests.get(url, timeout=10)
        print(f"✅ Yahoo Finance API response: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Yahoo Finance API: FAILED - {e}")
        return False

def test_yfinance_library():
    """Test yfinance library with different approaches"""
    print("\n🧪 TESTING YFINANCE LIBRARY")
    print("-" * 40)
    
    # Test 1: Simple ticker
    try:
        print("Test 1: Creating ticker object...")
        ticker = yf.Ticker("AAPL")
        print("✅ Ticker object created")
        
        print("Test 2: Getting basic info...")
        info = ticker.info
        print(f"✅ Basic info retrieved: {len(info)} fields")
        
        print("Test 3: Getting historical data...")
        data = ticker.history(period="5d")
        print(f"✅ Historical data: {len(data)} days")
        print(f"Latest close: ${data['Close'].iloc[-1]:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ yfinance test failed: {e}")
        return False

def test_different_symbols():
    """Test different stock symbols"""
    print("\n🧪 TESTING DIFFERENT SYMBOLS")
    print("-" * 40)
    
    symbols = ["AAPL", "MSFT", "GOOGL", "^GSPC", "BBCA.JK"]
    
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="5d")
            if not data.empty:
                print(f"✅ {symbol}: {len(data)} days, Latest: {data['Close'].iloc[-1]:.2f}")
            else:
                print(f"❌ {symbol}: No data")
        except Exception as e:
            print(f"❌ {symbol}: Error - {e}")

def test_alternative_periods():
    """Test different time periods"""
    print("\n🧪 TESTING DIFFERENT PERIODS")
    print("-" * 40)
    
    periods = ["1d", "5d", "1mo", "3mo"]
    
    for period in periods:
        try:
            ticker = yf.Ticker("AAPL")
            data = ticker.history(period=period)
            if not data.empty:
                print(f"✅ Period {period}: {len(data)} days")
            else:
                print(f"❌ Period {period}: No data")
        except Exception as e:
            print(f"❌ Period {period}: Error - {e}")

def main():
    """Run all diagnostic tests"""
    print("🔍 YAHOO FINANCE DIAGNOSTIC TOOL")
    print("=" * 50)
    print(f"📅 Test time: {datetime.now()}")
    print()
    
    # Test 1: Internet connection
    print("1️⃣ TESTING INTERNET CONNECTION")
    print("-" * 30)
    internet_ok = test_internet_connection()
    print()
    
    if not internet_ok:
        print("❌ Cannot proceed without internet connection")
        return
    
    # Test 2: Yahoo Finance API
    print("2️⃣ TESTING YAHOO FINANCE API")
    print("-" * 30)
    api_ok = test_yahoo_finance_direct()
    print()
    
    # Test 3: yfinance library
    yfinance_ok = test_yfinance_library()
    print()
    
    # Test 4: Different symbols
    test_different_symbols()
    print()
    
    # Test 5: Different periods
    test_alternative_periods()
    print()
    
    # Summary
    print("📋 DIAGNOSTIC SUMMARY")
    print("-" * 30)
    print(f"Internet: {'✅' if internet_ok else '❌'}")
    print(f"Yahoo API: {'✅' if api_ok else '❌'}")
    print(f"yfinance: {'✅' if yfinance_ok else '❌'}")
    
    if not yfinance_ok:
        print("\n💡 POSSIBLE SOLUTIONS:")
        print("• Update yfinance: pip install --upgrade yfinance")
        print("• Check firewall/proxy settings")
        print("• Try alternative data sources")
        print("• Use VPN if Yahoo Finance is blocked")

if __name__ == "__main__":
    main() 