"""
Test script for Enhanced ChatGPT Analysis with Vision Capabilities
Demonstrates both statistical and visual chart analysis
"""

import asyncio
import sys
from trading_bot import IndonesianStockBot
from config import (
    ENABLE_CHATGPT_CONFIRMATION, ENABLE_CHATGPT_VISION, 
    ENABLE_CHART_PATTERN_ANALYSIS, CHATGPT_MODEL, CHATGPT_VISION_MODEL
)


async def test_enhanced_chatgpt_analysis(symbol: str = "BBCA.JK"):
    """Test the enhanced ChatGPT analysis with both statistical and visual capabilities"""
    try:
        print(f"🤖 TESTING ENHANCED CHATGPT ANALYSIS")
        print("=" * 70)
        print(f"📊 Symbol: {symbol}")
        print(f"🤖 ChatGPT Confirmation: {'ENABLED' if ENABLE_CHATGPT_CONFIRMATION else 'DISABLED'}")
        print(f"👁️ Vision Analysis: {'ENABLED' if ENABLE_CHATGPT_VISION else 'DISABLED'}")
        print(f"📈 Chart Pattern Analysis: {'ENABLED' if ENABLE_CHART_PATTERN_ANALYSIS else 'DISABLED'}")
        print(f"📊 Text Model: {CHATGPT_MODEL}")
        print(f"👁️ Vision Model: {CHATGPT_VISION_MODEL}")
        print("-" * 70)
        
        bot = IndonesianStockBot()
        
        # Check if OpenAI client is available
        if not bot.openai_client:
            print("❌ ERROR: OpenAI client not initialized!")
            print("   Please check your OPENAI_API_KEY in .env file")
            return
        
        # Analyze single stock
        print(f"\n🔍 Analyzing {symbol}...")
        signal_info = await bot.analyze_stock(symbol)
        
        if signal_info:
            print(f"\n📊 BASIC SIGNAL INFORMATION")
            print("-" * 40)
            print(f"📅 Date: {signal_info['date']}")
            print(f"🎯 Signal: {signal_info['signal']}")
            print(f"💰 Price: {signal_info['current_price']:,} IDR ({signal_info['price_change']:+.2f}%)")
            print(f"📊 RSI: {signal_info['rsi']:.1f}")
            print(f"📈 Volume Ratio: {signal_info['volume_ratio']:.2f}x")
            print(f"✅ Valid: {signal_info['valid']}")
            
            # Display ChatGPT analysis if available
            if 'chatgpt_confirmation' in signal_info:
                confirmation = signal_info['chatgpt_confirmation']
                
                print(f"\n🤖 ENHANCED CHATGPT ANALYSIS RESULTS")
                print("=" * 50)
                
                # Analysis type and metadata
                analysis_type = confirmation.get('analysis_type', 'Unknown')
                vision_enabled = confirmation.get('vision_enabled', False)
                analysis_emoji = "👁️📊" if vision_enabled else "📊"
                
                print(f"{analysis_emoji} **Analysis Type**: {analysis_type}")
                print(f"🎯 **Recommendation**: {confirmation.get('recommendation', 'N/A')}")
                print(f"💪 **Confidence**: {confirmation.get('confidence', 0.5):.1%}")
                print(f"⚠️ **Risk Assessment**: {confirmation.get('risk_assessment', 'MEDIUM')}")
                
                # Main analysis
                print(f"\n💭 **COMPREHENSIVE ANALYSIS**")
                print("-" * 30)
                analysis_text = confirmation.get('analysis', 'No analysis available')
                # Wrap long text
                words = analysis_text.split()
                lines = []
                current_line = []
                for word in words:
                    if len(' '.join(current_line + [word])) <= 80:
                        current_line.append(word)
                    else:
                        if current_line:
                            lines.append(' '.join(current_line))
                        current_line = [word]
                if current_line:
                    lines.append(' '.join(current_line))
                
                for line in lines:
                    print(f"   {line}")
                
                # Key factors
                print(f"\n🔑 **KEY FACTORS**")
                print("-" * 20)
                key_factors = confirmation.get('key_factors', [])
                if key_factors:
                    for i, factor in enumerate(key_factors, 1):
                        print(f"   {i}. {factor}")
                else:
                    print("   • No specific factors identified")
                
                # Statistical analysis breakdown
                if 'statistical_analysis' in confirmation:
                    stats = confirmation['statistical_analysis']
                    print(f"\n📊 **STATISTICAL ANALYSIS BREAKDOWN**")
                    print("-" * 35)
                    print(f"   🎯 Technical Score: {stats.get('technical_score', 0.5):.1%}")
                    print(f"   📈 Volume Confirmation: {stats.get('volume_confirmation', 'N/A')}")
                    print(f"   📊 RSI Assessment: {stats.get('rsi_assessment', 'N/A')}")
                    print(f"   📈 SMA Trend: {stats.get('sma_trend', 'N/A')}")
                    print(f"   🎯 Signal Reliability: {stats.get('signal_reliability', 'N/A')}")
                
                # Visual analysis (if available)
                if vision_enabled and 'visual_analysis' in confirmation:
                    visual = confirmation['visual_analysis']
                    print(f"\n👁️ **VISUAL CHART ANALYSIS**")
                    print("-" * 30)
                    print(f"   📈 Chart Pattern: {visual.get('chart_pattern', 'No pattern identified')}")
                    print(f"   📊 Trend Direction: {visual.get('trend_direction', 'N/A')}")
                    print(f"   🎯 Support/Resistance: {visual.get('support_resistance', 'No levels identified')}")
                    print(f"   ✅ Visual Confirmation: {visual.get('visual_confirmation', 'N/A')}")
                    print(f"   💪 Chart Strength: {visual.get('chart_strength', 'N/A')}")
                elif ENABLE_CHATGPT_VISION:
                    print(f"\n👁️ **VISUAL ANALYSIS**: Not available (chart encoding may have failed)")
                
                # Sentiment analysis
                if 'sentiment_analysis' in confirmation:
                    sentiment = confirmation['sentiment_analysis']
                    print(f"\n📊 **SENTIMENT ANALYSIS**")
                    print("-" * 25)
                    
                    sentiment_emoji = {
                        'VERY_POSITIVE': "🚀",
                        'POSITIVE': "📈",
                        'NEUTRAL': "➡️",
                        'NEGATIVE': "📉",
                        'VERY_NEGATIVE': "💥"
                    }.get(sentiment.get('overall_sentiment', 'NEUTRAL'), "❓")
                    
                    print(f"   {sentiment_emoji} Overall: {sentiment.get('overall_sentiment', 'NEUTRAL')}")
                    print(f"   📊 Score: {sentiment.get('sentiment_score', 0.5):.1%}")
                    print(f"   🏢 Sector: {sentiment.get('sector_sentiment', 'N/A')}")
                    print(f"   🌍 Global Impact: {sentiment.get('global_influence', 'N/A')}")
                    print(f"   📰 News Impact: {sentiment.get('news_impact', 'N/A')}")
                
                # Trading recommendations
                if 'trading_recommendation' in confirmation:
                    trading_rec = confirmation['trading_recommendation']
                    print(f"\n💼 **ENHANCED TRADING STRATEGY**")
                    print("-" * 35)
                    print(f"   🎯 Entry: {trading_rec.get('entry_strategy', 'Standard entry')}")
                    print(f"   🚪 Exit: {trading_rec.get('exit_strategy', 'Standard exit')}")
                    print(f"   📏 Position Size: {trading_rec.get('position_sizing', 'Standard sizing')}")
                    print(f"   ⚠️ Risk Mgmt: {trading_rec.get('risk_management', 'Standard risk management')}")
                
                # Additional notes
                additional_notes = confirmation.get('additional_notes', '')
                if additional_notes:
                    print(f"\n📝 **ADDITIONAL INSIGHTS**")
                    print("-" * 25)
                    # Wrap additional notes
                    words = additional_notes.split()
                    lines = []
                    current_line = []
                    for word in words:
                        if len(' '.join(current_line + [word])) <= 80:
                            current_line.append(word)
                        else:
                            if current_line:
                                lines.append(' '.join(current_line))
                            current_line = [word]
                    if current_line:
                        lines.append(' '.join(current_line))
                    
                    for line in lines:
                        print(f"   {line}")
                
                # Signal status
                if signal_info.get('chatgpt_filtered', False):
                    print(f"\n🚫 **SIGNAL STATUS**: FILTERED BY CHATGPT")
                    print(f"   This signal was NOT sent to Telegram")
                else:
                    print(f"\n✅ **SIGNAL STATUS**: CONFIRMED AND SENT")
                    print(f"   This signal was sent to Telegram with AI endorsement")
                
            else:
                print(f"\n❌ No ChatGPT confirmation available")
                print(f"   ChatGPT analysis may be disabled or failed")
            
            print("\n" + "=" * 70)
            print("🎯 ANALYSIS COMPLETE!")
            print("⚠️  This is for educational purposes only. Always DYOR!")
            
        else:
            print(f"❌ No analysis results for {symbol}")
            print("\n🔧 TROUBLESHOOTING:")
            print("   • Check if symbol exists and has sufficient data")
            print("   • Verify internet connection")
            print("   • Try with a different stock symbol")
            
    except Exception as e:
        print(f"❌ Error testing enhanced ChatGPT analysis: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main function"""
    print("🤖 ENHANCED CHATGPT ANALYSIS TESTER")
    print("=" * 70)
    
    # Get symbol from command line or use default
    symbol = sys.argv[1] if len(sys.argv) > 1 else "BBCA.JK"
    
    print(f"Testing enhanced ChatGPT analysis with {symbol}")
    print("This will demonstrate both statistical and visual analysis capabilities")
    print()
    
    asyncio.run(test_enhanced_chatgpt_analysis(symbol))


if __name__ == "__main__":
    main() 