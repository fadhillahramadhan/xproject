#!/usr/bin/env python3
"""
Startup script for Interactive Telegram Trading Bot
"""

import asyncio
import sys
from interactive_telegram_bot import InteractiveTradingBot

def main():
    """Start the interactive bot"""
    print("🚀 Starting Interactive Telegram Trading Bot...")
    print("=" * 50)
    print("Features:")
    print("📊 /analyze <symbol> - Analyze crypto/stocks")
    print("📈 /signals - Get watchlist signals") 
    print("🔍 /watchlist - Manage watchlist")
    print("🔔 /notifications - Notification settings")
    print("📚 /help - Show help")
    print()
    print("💡 Just type symbols like 'BTC' or 'ANTM.JK' for quick analysis!")
    print()
    print("Press Ctrl+C to stop the bot")
    print("=" * 50)
    
    try:
        # Run the interactive bot
        asyncio.run(InteractiveTradingBot().run())
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure you have:")
        print("- TELEGRAM_BOT_TOKEN in .env file")
        print("- TELEGRAM_CHAT_ID in .env file")
        print("- Required dependencies installed")

if __name__ == "__main__":
    main() 