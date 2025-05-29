#!/usr/bin/env python3
"""
Production Runner for Indonesian Trading Bot
Optimized for server deployment with enhanced error handling and monitoring
"""

import asyncio
import logging
import signal
import sys
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
import schedule
import traceback
from trading_bot import IndonesianStockBot

# Setup production logging
def setup_production_logging():
    """Setup comprehensive logging for production environment"""
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configure logging with multiple handlers
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Clear existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # File handler for general logs
    file_handler = logging.FileHandler('logs/trading_bot.log')
    file_handler.setLevel(logging.INFO)
    
    # File handler for errors only
    error_handler = logging.FileHandler('logs/trading_bot_errors.log')
    error_handler.setLevel(logging.ERROR)
    
    # Console handler for immediate feedback
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Apply formatter to all handlers
    file_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)
    
    return logger

class ProductionTradingBot:
    """Production wrapper for the trading bot with enhanced monitoring and error handling"""
    
    def __init__(self):
        self.logger = setup_production_logging()
        self.bot = None
        self.running = False
        self.last_successful_run = None
        self.error_count = 0
        self.max_errors = 5
        self.restart_delay = 300  # 5 minutes
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        self.logger.info("🇮🇩 Indonesian Trading Bot - Production Mode Started")
        self.logger.info(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        self.logger.info(f"📡 Received signal {signum}, shutting down gracefully...")
        self.running = False
        sys.exit(0)
    
    async def initialize_bot(self):
        """Initialize the trading bot with error handling"""
        try:
            self.logger.info("🤖 Initializing trading bot...")
            self.bot = IndonesianStockBot()
            
            # Test bot initialization
            if not self.bot.bot_token or not self.bot.chat_id:
                raise ValueError("Telegram credentials not found in environment")
            
            if not self.bot.openai_client:
                self.logger.warning("⚠️ OpenAI client not initialized - ChatGPT confirmation disabled")
            else:
                self.logger.info("✅ OpenAI client initialized successfully")
            
            self.logger.info("✅ Trading bot initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize trading bot: {e}")
            self.logger.error(traceback.format_exc())
            return False
    
    async def run_daily_analysis_safe(self):
        """Run daily analysis with comprehensive error handling"""
        try:
            self.logger.info("🔍 Starting daily analysis...")
            start_time = datetime.now()
            
            if not self.bot:
                if not await self.initialize_bot():
                    raise Exception("Bot initialization failed")
            
            # Run the analysis
            await self.bot.run_daily_analysis()
            
            # Record successful run
            self.last_successful_run = datetime.now()
            self.error_count = 0  # Reset error count on success
            
            duration = (datetime.now() - start_time).total_seconds()
            self.logger.info(f"✅ Daily analysis completed successfully in {duration:.1f} seconds")
            
            # Send health check message
            await self.send_health_check()
            
        except Exception as e:
            self.error_count += 1
            self.logger.error(f"❌ Daily analysis failed (error {self.error_count}/{self.max_errors}): {e}")
            self.logger.error(traceback.format_exc())
            
            # Send error notification
            await self.send_error_notification(e)
            
            # Check if we've exceeded max errors
            if self.error_count >= self.max_errors:
                self.logger.critical(f"🚨 Maximum error count ({self.max_errors}) reached. Stopping bot.")
                await self.send_critical_error_notification()
                self.running = False
    
    async def send_health_check(self):
        """Send periodic health check message"""
        try:
            if self.bot and self.last_successful_run:
                uptime = datetime.now() - self.last_successful_run
                
                # Send health check every 24 hours
                if uptime.total_seconds() < 3600:  # Only if recent run
                    health_message = f"""
🤖 **Trading Bot Health Check** 🤖

✅ Status: Running normally
📅 Last successful run: {self.last_successful_run.strftime('%Y-%m-%d %H:%M:%S')}
⏱️ Uptime: {uptime.days} days, {uptime.seconds//3600} hours
🔄 Error count: {self.error_count}/{self.max_errors}
💻 Server time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🇮🇩 Indonesian Stock Bot - Production Mode
                    """
                    
                    await self.bot.send_telegram_message(health_message.strip())
                    
        except Exception as e:
            self.logger.warning(f"⚠️ Failed to send health check: {e}")
    
    async def send_error_notification(self, error):
        """Send error notification to Telegram"""
        try:
            if self.bot:
                error_message = f"""
🚨 **Trading Bot Error Alert** 🚨

❌ Error occurred during analysis
📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🔢 Error count: {self.error_count}/{self.max_errors}
📝 Error: {str(error)[:200]}...

🔄 Bot will retry on next scheduled run
⚠️ If errors persist, manual intervention may be required
                """
                
                await self.bot.send_telegram_message(error_message.strip())
                
        except Exception as e:
            self.logger.error(f"❌ Failed to send error notification: {e}")
    
    async def send_critical_error_notification(self):
        """Send critical error notification when max errors reached"""
        try:
            if self.bot:
                critical_message = f"""
🚨🚨 **CRITICAL: Trading Bot Stopped** 🚨🚨

❌ Maximum error count reached ({self.max_errors})
📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🛑 Bot has been stopped to prevent further issues

🔧 **Required Actions:**
1. Check server logs for detailed error information
2. Verify internet connection and API credentials
3. Restart the bot service manually after fixing issues

📋 **Server Commands:**
• Check logs: sudo journalctl -u trading-bot -n 50
• Restart service: sudo systemctl restart trading-bot
• Check status: sudo systemctl status trading-bot
                """
                
                await self.bot.send_telegram_message(critical_message.strip())
                
        except Exception as e:
            self.logger.error(f"❌ Failed to send critical error notification: {e}")
    
    def schedule_daily_analysis(self):
        """Schedule daily analysis at market close time"""
        # Schedule for 5:00 PM Jakarta time (after market close)
        schedule.every().day.at("17:00").do(
            lambda: asyncio.create_task(self.run_daily_analysis_safe())
        )
        
        # Also schedule a health check at 8:00 AM
        schedule.every().day.at("08:00").do(
            lambda: asyncio.create_task(self.send_health_check())
        )
        
        self.logger.info("📅 Scheduled daily analysis at 17:00 Jakarta time")
        self.logger.info("📅 Scheduled health check at 08:00 Jakarta time")
    
    async def run_production(self):
        """Main production loop"""
        self.running = True
        
        # Initialize bot
        if not await self.initialize_bot():
            self.logger.critical("🚨 Failed to initialize bot, exiting...")
            return
        
        # Schedule tasks
        self.schedule_daily_analysis()
        
        # Send startup notification
        try:
            startup_message = f"""
🚀 **Trading Bot Started** 🚀

✅ Production mode activated
📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
⏰ Next analysis: Today at 17:00 Jakarta time
🤖 ChatGPT Vision: {'Enabled' if self.bot.openai_client else 'Disabled'}
📋 Watchlist: {len(self.bot.watchlist_data) if hasattr(self.bot, 'watchlist_data') else 'N/A'} stocks

🇮🇩 Indonesian Stock Bot - Ready for trading!
            """
            
            await self.bot.send_telegram_message(startup_message.strip())
            
        except Exception as e:
            self.logger.warning(f"⚠️ Failed to send startup notification: {e}")
        
        # Main loop
        self.logger.info("🔄 Entering main production loop...")
        
        while self.running:
            try:
                # Run scheduled tasks
                schedule.run_pending()
                
                # Sleep for 1 minute before checking again
                await asyncio.sleep(60)
                
            except KeyboardInterrupt:
                self.logger.info("📡 Received keyboard interrupt, shutting down...")
                break
                
            except Exception as e:
                self.logger.error(f"❌ Error in main loop: {e}")
                self.logger.error(traceback.format_exc())
                
                # Wait before retrying
                await asyncio.sleep(self.restart_delay)
        
        self.logger.info("🛑 Production loop ended")
    
    async def test_run(self):
        """Run a test analysis immediately (for testing deployment)"""
        self.logger.info("🧪 Running test analysis...")
        
        if not await self.initialize_bot():
            self.logger.error("❌ Test failed: Bot initialization failed")
            return False
        
        try:
            # Test with a single stock
            test_symbol = "BBCA.JK"
            self.logger.info(f"🔍 Testing with {test_symbol}...")
            
            signal_info = await self.bot.analyze_stock(test_symbol)
            
            if signal_info:
                self.logger.info(f"✅ Test successful: {test_symbol} analysis completed")
                
                # Send test notification
                test_message = f"""
🧪 **Trading Bot Test Successful** 🧪

✅ Server deployment working correctly
📊 Test symbol: {test_symbol}
🎯 Signal: {signal_info['signal']}
💰 Price: {signal_info['current_price']:,} IDR
📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🚀 Bot is ready for production!
                """
                
                await self.bot.send_telegram_message(test_message.strip())
                return True
                
            else:
                self.logger.error("❌ Test failed: No analysis results")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Test failed: {e}")
            self.logger.error(traceback.format_exc())
            return False

async def main():
    """Main entry point"""
    production_bot = ProductionTradingBot()
    
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Run test mode
        success = await production_bot.test_run()
        sys.exit(0 if success else 1)
    else:
        # Run production mode
        await production_bot.run_production()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Trading bot stopped by user")
    except Exception as e:
        print(f"🚨 Critical error: {e}")
        traceback.print_exc()
        sys.exit(1) 