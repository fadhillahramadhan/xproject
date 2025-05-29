"""
Test script for analyzing a single Indonesian stock
Enhanced with sell signal testing and comprehensive analysis
"""

import asyncio
import sys
from trading_bot import IndonesianStockBot
from config import INDONESIAN_STOCKS, SIGNAL_BUY, SIGNAL_SELL, SIGNAL_STRONG_SELL, ENABLE_WATCHLIST, WATCHLIST_STOCKS

# Test stocks that work with Yahoo Finance
TEST_STOCKS = {
    "US": ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"],
    "Indonesian": INDONESIAN_STOCKS
}


async def test_single_stock(symbol: str = "BBCA.JK"):
    """Test the bot with a single stock and display enhanced analysis"""
    try:
        print(f"🔍 Testing Enhanced Trading Bot with {symbol}...")
        print("=" * 60)
        
        bot = IndonesianStockBot()
        
        # Analyze single stock
        signal_info = await bot.analyze_stock(symbol)
        
        if signal_info:
            print(f"\n📊 ENHANCED ANALYSIS RESULTS FOR {symbol}")
            print("-" * 50)
            
            # Basic Info
            print(f"📅 Date: {signal_info['date']}")
            print(f"💰 Current Price: {signal_info['current_price']:,}")
            print(f"📈 Price Change: {signal_info['price_change']:+.2f}%")
            print(f"📊 Volume: {signal_info['volume']:,}")
            print(f"📊 Volume Ratio: {signal_info['volume_ratio']:.2f}x")
            
            # Signal Information
            print(f"\n🎯 SIGNAL INFORMATION")
            print("-" * 30)
            signal_emoji = {
                SIGNAL_BUY: "🟢",
                SIGNAL_SELL: "🔴", 
                SIGNAL_STRONG_SELL: "🚨"
            }
            emoji = signal_emoji.get(signal_info['signal'], "🟡")
            print(f"{emoji} Signal: {signal_info['signal']}")
            print(f"🎯 Reason: {signal_info['signal_reason']}")
            print(f"✅ Valid: {signal_info['valid']}")
            print(f"💪 Strength: {signal_info['strength']}")
            
            # Technical Indicators
            print(f"\n📊 TECHNICAL INDICATORS")
            print("-" * 30)
            print(f"📉 SMA 10: {signal_info['sma_short']:,}")
            print(f"📉 SMA 20: {signal_info['sma_long']:,}")
            print(f"📊 RSI: {signal_info['rsi']:.1f}")
            
            # RSI Status
            if signal_info['rsi'] > 70:
                rsi_status = "🔴 OVERBOUGHT (Sell Zone)"
            elif signal_info['rsi'] < 30:
                rsi_status = "🟢 OVERSOLD (Buy Zone)"
            else:
                rsi_status = "🟡 NEUTRAL"
            print(f"📊 RSI Status: {rsi_status}")
            
            # Trading Levels
            print(f"\n🎯 TRADING LEVELS")
            print("-" * 30)
            print(f"🛑 Stop Loss: {signal_info['stop_loss_price']:,} (-5%)")
            print(f"🎯 Take Profit: {signal_info['take_profit_price']:,} (+10%)")
            print(f"📈 Recent High: {signal_info['recent_high']:,}")
            print(f"📉 Recent Low: {signal_info['recent_low']:,}")
            
            # Volume Analysis
            print(f"\n📊 VOLUME ANALYSIS")
            print("-" * 30)
            if signal_info['volume_ratio'] > 2.0:
                volume_status = "🔴 HIGH VOLUME ALERT!"
            elif signal_info['volume_ratio'] > 1.5:
                volume_status = "🟡 Above Average Volume"
            else:
                volume_status = "🟢 Normal Volume"
            print(f"📊 Volume Status: {volume_status}")
            
            # Action Recommendations
            print(f"\n💡 ACTION RECOMMENDATIONS")
            print("-" * 30)
            if signal_info['signal'] == SIGNAL_BUY and signal_info['valid']:
                print("🟢 CONSIDER BUYING")
                print(f"   • Entry: Around {signal_info['current_price']:,}")
                print(f"   • Stop Loss: {signal_info['stop_loss_price']:,}")
                print(f"   • Take Profit: {signal_info['take_profit_price']:,}")
            elif signal_info['signal'] == SIGNAL_SELL and signal_info['valid']:
                print("🔴 CONSIDER SELLING")
                print(f"   • Current holders should consider taking profits")
                print(f"   • Avoid new long positions")
            elif signal_info['signal'] == SIGNAL_STRONG_SELL and signal_info['valid']:
                print("🚨 STRONG SELL SIGNAL!")
                print(f"   • Exit positions immediately")
                print(f"   • Consider short positions (if available)")
                print(f"   • High risk of further decline")
            else:
                print("🟡 HOLD/WAIT")
                print(f"   • No clear signal at this time")
                print(f"   • Monitor for better entry/exit points")
            
            # ChatGPT Confirmation (if available)
            if 'chatgpt_confirmation' in signal_info:
                confirmation = signal_info['chatgpt_confirmation']
                print(f"\n🤖 CHATGPT CONFIRMATION")
                print("-" * 30)
                
                # Recommendation emoji
                rec_emoji = {
                    'CONFIRM': "✅",
                    'REJECT': "❌",
                    'MODIFY': "⚠️",
                    'PROCEED_WITH_CAUTION': "⚠️"
                }.get(confirmation.get('recommendation', 'UNKNOWN'), "❓")
                
                # Confidence color
                confidence = confirmation.get('confidence', 0.5)
                conf_emoji = "🟢" if confidence >= 0.8 else "🟡" if confidence >= 0.6 else "🔴"
                
                # Risk color
                risk_emoji = {
                    'LOW': "🟢",
                    'MEDIUM': "🟡", 
                    'HIGH': "🔴",
                    'UNKNOWN': "❓"
                }.get(confirmation.get('risk_assessment', 'MEDIUM'), "❓")
                
                print(f"{rec_emoji} Recommendation: {confirmation.get('recommendation', 'N/A')}")
                print(f"{conf_emoji} Confidence: {confidence:.1%}")
                print(f"{risk_emoji} Risk Assessment: {confirmation.get('risk_assessment', 'MEDIUM')}")
                print(f"💭 Analysis: {confirmation.get('analysis', 'No analysis available')}")
                
                if confirmation.get('key_factors'):
                    print(f"🔑 Key Factors:")
                    for factor in confirmation.get('key_factors', []):
                        print(f"   • {factor}")
                
                if confirmation.get('additional_notes'):
                    print(f"📝 Notes: {confirmation.get('additional_notes')}")
                
                # Sentiment Analysis (if available)
                if confirmation.get('sentiment_analysis'):
                    sentiment = confirmation['sentiment_analysis']
                    print(f"\n📊 SENTIMENT ANALYSIS")
                    print("-" * 25)
                    
                    # Overall sentiment with emoji
                    sentiment_emoji = {
                        'VERY_POSITIVE': "🚀",
                        'POSITIVE': "📈", 
                        'NEUTRAL': "➡️",
                        'NEGATIVE': "📉",
                        'VERY_NEGATIVE': "💥"
                    }.get(sentiment.get('overall_sentiment', 'NEUTRAL'), "❓")
                    
                    sentiment_score = sentiment.get('sentiment_score', 0.5)
                    score_emoji = "🟢" if sentiment_score >= 0.7 else "🟡" if sentiment_score >= 0.4 else "🔴"
                    
                    print(f"{sentiment_emoji} Overall: {sentiment.get('overall_sentiment', 'NEUTRAL')}")
                    print(f"{score_emoji} Score: {sentiment_score:.1%}")
                    print(f"🏢 Sector: {sentiment.get('sector_sentiment', 'N/A')}")
                    print(f"🌍 Global Impact: {sentiment.get('global_influence', 'N/A')}")
                    print(f"📰 News Impact: {sentiment.get('news_impact', 'N/A')}")
                    print(f"🏛️ Economic Factors: {sentiment.get('economic_factors', 'N/A')}")
                    print(f"📈 Market Mood: {sentiment.get('market_mood', 'N/A')}")
                    
                    if sentiment.get('sentiment_reasoning'):
                        print(f"💭 Reasoning: {sentiment.get('sentiment_reasoning')}")
                
                # Signal filtering status
                if signal_info.get('chatgpt_filtered', False):
                    print(f"\n🚫 SIGNAL FILTERED BY CHATGPT")
                    print(f"   This signal was not sent to Telegram due to ChatGPT analysis")
            
            # Watchlist status
            if ENABLE_WATCHLIST:
                is_watchlist = symbol in WATCHLIST_STOCKS
                print(f"\n📋 WATCHLIST STATUS")
                print("-" * 20)
                if is_watchlist:
                    print(f"⭐ {symbol} is in your WATCHLIST")
                    print(f"   • Lower confidence threshold (50% vs 70%)")
                    print(f"   • Priority alerts and monitoring")
                    print(f"   • Enhanced tracking and notifications")
                else:
                    print(f"📋 {symbol} is NOT in your watchlist")
                    print(f"   • Standard confidence threshold (70%)")
                    print(f"   • Regular analysis only")
            
            print("\n" + "=" * 60)
            print("⚠️  DISCLAIMER: This is for educational purposes only.")
            print("    Always do your own research before trading!")
            
        else:
            print(f"❌ No analysis results for {symbol}")
            print("\n🔧 TROUBLESHOOTING:")
            print("   • Yahoo Finance may not have data for this symbol")
            print("   • Indonesian stocks often have data issues with Yahoo Finance")
            print("   • Try testing with US stocks first:")
            print("     - python test_single_stock.py AAPL")
            print("     - python test_single_stock.py MSFT")
            print("     - python test_single_stock.py GOOGL")
            print("\n💡 SOLUTIONS:")
            print("   • Use alternative data sources (Alpha Vantage, IEX Cloud)")
            print("   • Try different Indonesian stock symbols")
            print("   • Check if symbols need different format")
            
    except Exception as e:
        print(f"❌ Error testing {symbol}: {e}")
        print("\n🔧 TROUBLESHOOTING:")
        print("• Check your .env file has correct Telegram credentials")
        print("• Verify internet connection")
        print("• Try with a US stock symbol (AAPL, MSFT, GOOGL)")
        print("• Indonesian stocks may need alternative data sources")


async def test_working_stocks():
    """Test with stocks that are known to work with Yahoo Finance"""
    print("🧪 TESTING WITH KNOWN WORKING STOCKS")
    print("=" * 60)
    
    working_stocks = ["AAPL", "MSFT", "GOOGL"]
    
    for stock in working_stocks:
        print(f"\n🔍 Testing {stock}...")
        await test_single_stock(stock)
        print("\n" + "-" * 40)


def main():
    """Main function with enhanced help"""
    print("🇮🇩 INDONESIAN STOCK TRADING BOT - ENHANCED TESTING")
    print("=" * 60)
    
    # Default to BBCA.JK if no symbol provided
    symbol = sys.argv[1] if len(sys.argv) > 1 else "BBCA.JK"
    
    # Special command to test working stocks
    if symbol.lower() == "test":
        asyncio.run(test_working_stocks())
        return
    
    if symbol not in INDONESIAN_STOCKS and not symbol in TEST_STOCKS["US"]:
        print(f"⚠️  Warning: {symbol} is not in the predefined stock lists")
        print(f"\n📋 Available Indonesian stocks:")
        for i, stock in enumerate(INDONESIAN_STOCKS, 1):
            print(f"   {i:2d}. {stock}")
        print(f"\n📋 Test US stocks (known to work):")
        for i, stock in enumerate(TEST_STOCKS["US"], 1):
            print(f"   {i:2d}. {stock}")
        print(f"\n🔄 Proceeding with {symbol} anyway...\n")
    else:
        if symbol in INDONESIAN_STOCKS:
            print(f"✅ Testing with {symbol} (Indonesian stock)")
        else:
            print(f"✅ Testing with {symbol} (US stock)")
        print()
    
    asyncio.run(test_single_stock(symbol))


if __name__ == "__main__":
    main() 