"""
Watchlist Manager for Indonesian Stock Trading Bot
Manage your stock watchlist with real-time monitoring
"""

import asyncio
import sys
from datetime import datetime, timedelta
from trading_bot import IndonesianStockBot
from config import WATCHLIST_STOCKS, INDONESIAN_STOCKS

class WatchlistManager:
    """Manage and monitor stock watchlist"""
    
    def __init__(self):
        self.bot = IndonesianStockBot()
    
    async def monitor_watchlist(self, duration_minutes: int = 60):
        """Monitor watchlist stocks for specified duration"""
        print(f"🔍 WATCHLIST MONITORING STARTED")
        print("=" * 50)
        print(f"📋 Monitoring {len(WATCHLIST_STOCKS)} stocks for {duration_minutes} minutes")
        print(f"📊 Stocks: {', '.join(WATCHLIST_STOCKS)}")
        print()
        
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=duration_minutes)
        check_interval = 5  # Check every 5 minutes
        
        while datetime.now() < end_time:
            print(f"🕐 {datetime.now().strftime('%H:%M:%S')} - Checking watchlist...")
            
            for symbol in WATCHLIST_STOCKS:
                try:
                    signal_info = await self.bot.analyze_stock(symbol)
                    if signal_info:
                        # Check for significant changes
                        if signal_info['signal'] in ['BUY', 'SELL', 'STRONG_SELL']:
                            print(f"🚨 ALERT: {symbol} - {signal_info['signal']} signal detected!")
                        
                        # Check for price movements
                        if abs(signal_info['price_change']) >= 3.0:
                            direction = "📈" if signal_info['price_change'] > 0 else "📉"
                            print(f"{direction} {symbol}: {signal_info['price_change']:+.2f}% → {signal_info['current_price']:,} IDR")
                        
                        # Check for high volume
                        if signal_info.get('volume_ratio', 1) > 2.0:
                            print(f"📊 {symbol}: High volume {signal_info['volume_ratio']:.1f}x normal")
                
                except Exception as e:
                    print(f"❌ Error monitoring {symbol}: {e}")
                
                # Small delay between stocks
                await asyncio.sleep(1)
            
            print(f"✅ Watchlist check complete. Next check in {check_interval} minutes.\n")
            
            # Wait for next check
            await asyncio.sleep(check_interval * 60)
        
        print(f"🏁 Watchlist monitoring completed after {duration_minutes} minutes")
    
    async def analyze_watchlist(self):
        """Analyze all watchlist stocks and show detailed results"""
        print(f"📊 COMPREHENSIVE WATCHLIST ANALYSIS")
        print("=" * 60)
        print(f"📅 Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📋 Analyzing {len(WATCHLIST_STOCKS)} watchlist stocks...")
        print()
        
        results = []
        
        for i, symbol in enumerate(WATCHLIST_STOCKS, 1):
            print(f"🔍 Analyzing {symbol} ({i}/{len(WATCHLIST_STOCKS)})...")
            
            try:
                signal_info = await self.bot.analyze_stock(symbol)
                if signal_info:
                    results.append(signal_info)
                    
                    # Display basic info
                    signal_emoji = {
                        'BUY': "🟢",
                        'SELL': "🔴",
                        'STRONG_SELL': "🚨",
                        'HOLD': "🟡"
                    }.get(signal_info['signal'], "⚪")
                    
                    print(f"   {signal_emoji} Signal: {signal_info['signal']}")
                    print(f"   💰 Price: {signal_info['current_price']:,} IDR ({signal_info['price_change']:+.2f}%)")
                    print(f"   📊 RSI: {signal_info['rsi']:.1f}")
                    print(f"   📈 Volume: {signal_info['volume_ratio']:.1f}x normal")
                    
                    # ChatGPT confirmation if available
                    if 'chatgpt_confirmation' in signal_info:
                        conf = signal_info['chatgpt_confirmation']
                        conf_emoji = "🟢" if conf.get('confidence', 0) >= 0.8 else "🟡" if conf.get('confidence', 0) >= 0.6 else "🔴"
                        print(f"   🤖 ChatGPT: {conf.get('recommendation', 'N/A')} ({conf_emoji} {conf.get('confidence', 0):.1%})")
                    
                    print()
                else:
                    print(f"   ❌ No data available for {symbol}")
                    print()
                
            except Exception as e:
                print(f"   ❌ Error analyzing {symbol}: {e}")
                print()
            
            # Delay between analyses
            await asyncio.sleep(2)
        
        # Summary
        print("📋 WATCHLIST SUMMARY")
        print("-" * 30)
        
        if results:
            buy_signals = len([r for r in results if r['signal'] == 'BUY'])
            sell_signals = len([r for r in results if r['signal'] == 'SELL'])
            strong_sell_signals = len([r for r in results if r['signal'] == 'STRONG_SELL'])
            hold_signals = len([r for r in results if r['signal'] == 'HOLD'])
            
            print(f"🟢 Buy Signals: {buy_signals}")
            print(f"🔴 Sell Signals: {sell_signals}")
            print(f"🚨 Strong Sell Signals: {strong_sell_signals}")
            print(f"🟡 Hold/No Signal: {hold_signals}")
            
            # Top movers
            price_changes = [(r['symbol'], r['price_change']) for r in results if abs(r['price_change']) >= 1.0]
            if price_changes:
                print(f"\n📈 TOP MOVERS:")
                for symbol, change in sorted(price_changes, key=lambda x: abs(x[1]), reverse=True)[:5]:
                    direction = "📈" if change > 0 else "📉"
                    print(f"   {direction} {symbol}: {change:+.2f}%")
        else:
            print("❌ No analysis results available")
    
    def show_watchlist_info(self):
        """Display current watchlist configuration"""
        print(f"📋 CURRENT WATCHLIST CONFIGURATION")
        print("=" * 50)
        print(f"📊 Total Stocks: {len(WATCHLIST_STOCKS)}")
        print(f"🔔 Alerts Enabled: {'Yes' if True else 'No'}")  # From config
        print(f"📈 Price Alert Threshold: 5.0%")  # From config
        print(f"📊 Volume Alert Threshold: 2.0x normal")  # From config
        print()
        
        print(f"📋 WATCHLIST STOCKS:")
        print("-" * 20)
        for i, symbol in enumerate(WATCHLIST_STOCKS, 1):
            # Get company name from mapping
            company_names = {
                'BBCA.JK': 'Bank Central Asia',
                'BBRI.JK': 'Bank Rakyat Indonesia', 
                'BMRI.JK': 'Bank Mandiri',
                'TLKM.JK': 'Telkom Indonesia',
                'ASII.JK': 'Astra International',
                'UNVR.JK': 'Unilever Indonesia',
                'ICBP.JK': 'Indofood CBP',
                'GGRM.JK': 'Gudang Garam',
                'INDF.JK': 'Indofood Sukses Makmur',
                'KLBF.JK': 'Kalbe Farma'
            }
            company = company_names.get(symbol, 'Unknown Company')
            print(f"   {i:2d}. {symbol} - {company}")
        
        print()
        print(f"💡 Available Commands:")
        print(f"   • python watchlist_manager.py monitor [minutes] - Monitor watchlist")
        print(f"   • python watchlist_manager.py analyze - Analyze all watchlist stocks")
        print(f"   • python watchlist_manager.py info - Show this information")

async def main():
    """Main function"""
    manager = WatchlistManager()
    
    if len(sys.argv) < 2:
        manager.show_watchlist_info()
        return
    
    command = sys.argv[1].lower()
    
    if command == "monitor":
        duration = int(sys.argv[2]) if len(sys.argv) > 2 else 60
        await manager.monitor_watchlist(duration)
    
    elif command == "analyze":
        await manager.analyze_watchlist()
    
    elif command == "info":
        manager.show_watchlist_info()
    
    else:
        print(f"❌ Unknown command: {command}")
        print(f"💡 Available commands: monitor, analyze, info")

if __name__ == "__main__":
    asyncio.run(main()) 