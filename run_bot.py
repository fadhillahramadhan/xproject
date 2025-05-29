"""
Production script to run the Indonesian Stock Trading Bot
with scheduled daily analysis
"""

from trading_bot import IndonesianStockBot
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    """Run the bot in production mode with scheduling"""
    try:
        print("🇮🇩 Starting Indonesian Stock Trading Bot...")
        print("📅 Scheduled to run daily at 17:00 Jakarta time")
        print("⏹️  Press Ctrl+C to stop the bot")
        print("-" * 50)
        
        bot = IndonesianStockBot()
        bot.run_bot()  # This runs the scheduled version
        
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error running bot: {e}")
        logging.error(f"Error in main: {e}")

if __name__ == "__main__":
    main() 