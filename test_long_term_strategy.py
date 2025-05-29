#!/usr/bin/env python3
"""
Test script to demonstrate the long-term trading strategy
Shows how ANTM.JK would be analyzed with the new configuration
"""

import sys
import asyncio
from trading_bot import IndonesianStockBot

async def test_long_term_strategy(symbol="ANTM.JK"):
    """Test the long-term strategy on any symbol (stocks or crypto)"""
    print("🚀 Testing Long-Term Trading Strategy")
    print("=" * 50)
    
    # Determine if it's crypto or stock
    is_crypto = any(crypto in symbol.upper() for crypto in ['BTC', 'ETH', 'BNB', 'ADA', 'SOL', 'DOGE', 'XRP', 'DOT', 'AVAX', 'MATIC'])
    asset_type = "Cryptocurrency" if is_crypto else "Indonesian Stock"
    
    try:
        # Initialize the bot
        bot = IndonesianStockBot()
        
        print(f"📊 Analyzing {symbol} ({asset_type}) with long-term parameters...")
        
        # Fetch and analyze the asset
        signal_info = await bot.analyze_stock(symbol)
        
        if signal_info:
            print(f"\n✅ Analysis Complete for {symbol}")
            print("-" * 30)
            print(f"Asset Type: {asset_type}")
            print(f"Signal: {signal_info['signal']}")
            print(f"Reason: {signal_info['signal_reason']}")
            
            # Different currency format for crypto vs stocks
            if is_crypto:
                print(f"Current Price: ${signal_info['current_price']:,.2f} USD")
                print(f"Stop Loss: ${signal_info['stop_loss_price']:,.2f} USD (-15%)")
                print(f"Take Profit: ${signal_info['take_profit_price']:,.2f} USD (+25%)")
                print(f"SMA 20: ${signal_info['sma_short']:,.2f}")
                print(f"SMA 50: ${signal_info['sma_long']:,.2f}")
            else:
                print(f"Current Price: {signal_info['current_price']:,} IDR")
                print(f"Stop Loss: {signal_info['stop_loss_price']:,} IDR (-15%)")
                print(f"Take Profit: {signal_info['take_profit_price']:,} IDR (+25%)")
                print(f"SMA 20: {signal_info['sma_short']:,}")
                print(f"SMA 50: {signal_info['sma_long']:,}")
            
            print(f"Price Change: {signal_info['price_change']:+.2f}%")
            print(f"RSI: {signal_info['rsi']:.1f}")
            print(f"Signal Strength: {signal_info['strength']}")
            print(f"Valid Signal: {'Yes' if signal_info['valid'] else 'No'}")
            
            # Explain the difference
            print(f"\n🎯 Long-Term Strategy Analysis:")
            print(f"• RSI Threshold: 80+ (vs old 70+) - More conservative")
            print(f"• SMA Periods: 20/50 (vs old 10/20) - Smoother trends")
            print(f"• Stop Loss: 15% (vs old 5%) - More room for volatility")
            print(f"• Take Profit: 25% (vs old 10%) - Bigger gains target")
            
            if is_crypto:
                print(f"• Crypto markets: 24/7 trading, higher volatility expected")
            
            if signal_info['rsi'] < 80:
                print(f"✅ With RSI at {signal_info['rsi']:.1f}, this is NOT overbought in long-term view")
            else:
                print(f"⚠️ With RSI at {signal_info['rsi']:.1f}, this is overbought even in long-term view")
                
        else:
            print(f"❌ Could not analyze {symbol}")
            print(f"💡 Make sure the symbol is correct:")
            if is_crypto:
                print(f"   Crypto examples: BTC-USD, ETH-USD, BNB-USD")
            else:
                print(f"   Stock examples: ANTM.JK, BBCA.JK, TLKM.JK")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure you have the required environment variables set:")
        print("- TELEGRAM_BOT_TOKEN")
        print("- TELEGRAM_CHAT_ID")

if __name__ == "__main__":
    print("🔧 Long-Term Trading Strategy Test")
    print("This script tests the new long-term configuration")
    print("that's more suitable for trend following.")
    print("Works with both Indonesian stocks and cryptocurrencies!\n")
    
    # Get symbol from command line argument or use default
    symbol = "ANTM.JK"  # default
    if len(sys.argv) > 1:
        symbol = sys.argv[1].upper()
        
        # Auto-format common crypto symbols
        crypto_pairs = {
            'BTC': 'BTC-USD',
            'ETH': 'ETH-USD', 
            'BNB': 'BNB-USD',
            'ADA': 'ADA-USD',
            'SOL': 'SOL-USD',
            'DOGE': 'DOGE-USD',
            'XRP': 'XRP-USD',
            'DOT': 'DOT-USD',
            'AVAX': 'AVAX-USD',
            'MATIC': 'MATIC-USD'
        }
        
        if symbol in crypto_pairs:
            symbol = crypto_pairs[symbol]
        elif not symbol.endswith('.JK') and not symbol.endswith('-USD'):
            # If it's not crypto and not .JK, assume Indonesian stock
            symbol += '.JK'
            
        print(f"📊 Testing with symbol: {symbol}")
    else:
        print(f"📊 No symbol provided, using default: {symbol}")
        print(f"💡 Usage examples:")
        print(f"   Stocks: python test_long_term_strategy.py SUNI.JK")
        print(f"   Crypto: python test_long_term_strategy.py BTC-USD")
        print(f"   Crypto (short): python test_long_term_strategy.py BTC")
    
    # Run the test
    asyncio.run(test_long_term_strategy(symbol)) 