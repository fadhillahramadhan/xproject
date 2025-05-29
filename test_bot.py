#!/usr/bin/env python3
"""
Test script for Murphy's Crypto Trading Bot
Run this to verify all components work before deployment
"""

import sys
import os
from dotenv import load_dotenv

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import pandas as pd
        print("✅ pandas imported successfully")
        
        import numpy as np
        print("✅ numpy imported successfully")
        
        import ccxt
        print("✅ ccxt imported successfully")
        
        import ta
        print("✅ ta (technical analysis) imported successfully")
        
        import matplotlib.pyplot as plt
        print("✅ matplotlib imported successfully")
        
        from telegram import Update
        from telegram.ext import Application
        print("✅ python-telegram-bot imported successfully")
        
        from technical_analyzer import MurphyTechnicalAnalyzer
        print("✅ Custom technical analyzer imported successfully")
        
        from chart_generator import TechnicalChartGenerator
        print("✅ Custom chart generator imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_exchange_connection():
    """Test if we can connect to exchange"""
    print("\n🔍 Testing exchange connection...")
    
    try:
        import ccxt
        exchange = ccxt.binance()
        
        # Test public endpoint
        ticker = exchange.fetch_ticker('BTC/USDT')
        print(f"✅ Exchange connection successful - BTC/USDT: ${ticker['last']}")
        return True
        
    except Exception as e:
        print(f"❌ Exchange connection failed: {e}")
        return False

def test_technical_analysis():
    """Test technical analysis functionality"""
    print("\n🔍 Testing technical analysis...")
    
    try:
        from technical_analyzer import MurphyTechnicalAnalyzer
        
        analyzer = MurphyTechnicalAnalyzer()
        
        # Test data fetch
        df = analyzer.get_ohlcv_data('BTC/USDT', '1d', 50)
        if not df.empty:
            print(f"✅ Data fetch successful - {len(df)} candles retrieved")
            
            # Test indicators
            df = analyzer.calculate_indicators(df)
            print("✅ Technical indicators calculated")
            
            # Test signals
            signals = analyzer.generate_signals(df)
            print(f"✅ Signal generation successful - Signal: {signals['signal']}")
            
            return True
        else:
            print("❌ No data retrieved")
            return False
            
    except Exception as e:
        print(f"❌ Technical analysis test failed: {e}")
        return False

def test_chart_generation():
    """Test chart generation"""
    print("\n🔍 Testing chart generation...")
    
    try:
        from technical_analyzer import MurphyTechnicalAnalyzer
        from chart_generator import TechnicalChartGenerator
        
        analyzer = MurphyTechnicalAnalyzer()
        chart_gen = TechnicalChartGenerator()
        
        # Get sample data
        df = analyzer.get_ohlcv_data('BTC/USDT', '4h', 100)
        df = analyzer.calculate_indicators(df)
        signals = analyzer.generate_signals(df)
        
        # Generate chart
        chart_buffer = chart_gen.create_analysis_chart(df, signals, 'BTC/USDT')
        
        if chart_buffer:
            print("✅ Chart generation successful")
            return True
        else:
            print("❌ Chart generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Chart generation test failed: {e}")
        return False

def test_config():
    """Test configuration loading"""
    print("\n🔍 Testing configuration...")
    
    try:
        load_dotenv('config.env')
        
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        if bot_token and bot_token != 'YOUR_TELEGRAM_BOT_TOKEN_HERE':
            print("✅ Telegram bot token configured")
        else:
            print("⚠️  Telegram bot token not configured (use config.env)")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Murphy's Crypto Trading Bot - Component Tests\n")
    
    tests = [
        test_imports,
        test_exchange_connection,
        test_technical_analysis,
        test_chart_generation,
        test_config
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            failed += 1
    
    print(f"\n📊 Test Results:")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 All tests passed! Your bot is ready for deployment.")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please fix issues before deployment.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 