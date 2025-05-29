#!/usr/bin/env python3
"""
Interactive Telegram Trading Bot
Responds to commands for real-time crypto and stock analysis
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telegram.error import TelegramError
import os
from dotenv import load_dotenv

from trading_bot import IndonesianStockBot
from config import WATCHLIST_STOCKS

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class InteractiveTradingBot:
    """Interactive Telegram bot for real-time trading analysis"""
    
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if not self.bot_token:
            raise ValueError("Please set TELEGRAM_BOT_TOKEN in .env file")
        
        self.trading_bot = IndonesianStockBot()
        self.user_watchlists = {}  # Store user-specific watchlists
        
        # Initialize Telegram application
        self.application = Application.builder().token(self.bot_token).build()
        
        # Add command handlers
        self.setup_handlers()
        
        logger.info("Interactive Trading Bot initialized")
    
    def setup_handlers(self):
        """Setup command handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("analyze", self.analyze_command))
        self.application.add_handler(CommandHandler("signals", self.signals_command))
        self.application.add_handler(CommandHandler("watchlist", self.watchlist_command))
        self.application.add_handler(CommandHandler("notifications", self.notifications_command))
        
        # Handle regular messages (for symbols without commands)
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_message = """
🚀 **Welcome to Smart Trading Bot!**

Your AI-powered crypto & stock analysis companion is ready!

📊 **Available Commands:**
📈 /analyze <symbol> - Analyze crypto or stock (e.g., /analyze BTC or /analyze ANTM.JK)
📊 /signals - Get signals for watchlist assets
🔍 /watchlist - Manage your personal watchlist
🔔 /notifications - Notification settings
📚 /help - Show detailed help

💡 **Quick Examples:**
• `/analyze BTC` - Analyze Bitcoin
• `/analyze ETH-USD` - Analyze Ethereum  
• `/analyze ANTM.JK` - Analyze Indonesian stock
• Just type `BTC` for quick analysis

🎯 **Features:**
✅ Long-term trend analysis (20/50 SMA)
✅ RSI with 80+ overbought threshold
✅ AI-powered ChatGPT confirmation
✅ 15% stop loss, 25% take profit
✅ Support for 100+ cryptocurrencies
✅ Indonesian stock market support

Ready to start? Try `/analyze BTC` or `/help` for more info!
        """
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_message = """
📚 **SMART TRADING BOT - HELP GUIDE**

🔧 **ANALYSIS COMMANDS:**
📊 `/analyze <symbol>` - Comprehensive analysis
   Examples:
   • `/analyze BTC` → Bitcoin analysis
   • `/analyze ETH-USD` → Ethereum analysis
   • `/analyze ANTM.JK` → Indonesian stock
   • `/analyze SUNI.JK` → Another Indonesian stock

📈 `/signals` - Get signals for all watchlist assets
   Shows buy/sell/hold signals for your tracked assets

🔍 **WATCHLIST COMMANDS:**
📋 `/watchlist` - Show current watchlist
📋 `/watchlist add BTC` - Add Bitcoin to watchlist
📋 `/watchlist remove ETH` - Remove Ethereum
📋 `/watchlist clear` - Clear all watchlist items

🔔 **NOTIFICATION COMMANDS:**
🔔 `/notifications` - Show notification settings
🔔 `/notifications on` - Enable all notifications
🔔 `/notifications off` - Disable notifications

💡 **QUICK ANALYSIS:**
Just type any symbol directly (without /) for instant analysis:
• `BTC` → Quick Bitcoin analysis
• `ETH` → Quick Ethereum analysis
• `ANTM.JK` → Quick stock analysis

🎯 **SUPPORTED ASSETS:**
📈 **Cryptocurrencies:** BTC, ETH, BNB, ADA, SOL, DOGE, XRP, DOT, AVAX, MATIC, and 100+ more
📊 **Indonesian Stocks:** ANTM.JK, BBCA.JK, TLKM.JK, SUNI.JK, and all IDX stocks

🔍 **ANALYSIS FEATURES:**
✅ Long-term trend following (20/50 SMA)
✅ Conservative RSI thresholds (80+ overbought)
✅ AI-powered ChatGPT confirmation with vision
✅ Professional risk management (15% SL, 25% TP)
✅ Real-time price data
✅ Volume analysis
✅ Chart pattern recognition

Need help? Just ask! 🤖
        """
        await update.message.reply_text(help_message, parse_mode='Markdown')
    
    def format_symbol(self, symbol: str) -> str:
        """Format symbol for analysis"""
        symbol = symbol.upper().strip()
        
        # Auto-format common crypto symbols
        crypto_pairs = {
            'BTC': 'BTC-USD', 'ETH': 'ETH-USD', 'BNB': 'BNB-USD',
            'ADA': 'ADA-USD', 'SOL': 'SOL-USD', 'DOGE': 'DOGE-USD',
            'XRP': 'XRP-USD', 'DOT': 'DOT-USD', 'AVAX': 'AVAX-USD',
            'MATIC': 'MATIC-USD', 'LINK': 'LINK-USD', 'UNI': 'UNI-USD',
            'LTC': 'LTC-USD', 'BCH': 'BCH-USD', 'ATOM': 'ATOM-USD',
            'FTT': 'FTT-USD', 'NEAR': 'NEAR-USD', 'ALGO': 'ALGO-USD',
            'VET': 'VET-USD', 'ICP': 'ICP-USD', 'FIL': 'FIL-USD',
            'TRX': 'TRX-USD', 'ETC': 'ETC-USD', 'XLM': 'XLM-USD',
            'MANA': 'MANA-USD', 'SAND': 'SAND-USD', 'CRO': 'CRO-USD'
        }
        
        if symbol in crypto_pairs:
            return crypto_pairs[symbol]
        elif not symbol.endswith('.JK') and not symbol.endswith('-USD') and not symbol.endswith('-USDT'):
            # If it's not already formatted and not obviously crypto, assume Indonesian stock
            if any(char.isalpha() for char in symbol) and len(symbol) <= 6:
                return symbol + '.JK'
        
        return symbol
    
    def is_crypto(self, symbol: str) -> bool:
        """Check if symbol is a cryptocurrency"""
        crypto_symbols = ['BTC', 'ETH', 'ADA', 'DOT', 'MATIC', 'SOL', 'AVAX', 'LINK', 'UNI', 'AAVE', 'COMP', 'MKR', 'SNX', 'YFI', 'CRV', 'BAL', 'SUSHI', 'LTC', 'BCH', 'XRP', 'BNB', 'DOGE', 'SHIB', 'ATOM']
        return symbol.endswith('-USD') or symbol in crypto_symbols
    
    def get_asset_type(self, symbol: str) -> str:
        """Get asset type description for display"""
        if self.is_crypto(symbol):
            return "Cryptocurrency"
        elif symbol.endswith('.JK'):
            return "Indonesian Stock"
        else:
            return "Stock"
    
    async def analyze_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /analyze command"""
        if not context.args:
            await update.message.reply_text(
                "Please provide a symbol to analyze!\n\n"
                "Examples:\n"
                "• `/analyze BTC` - Bitcoin\n"
                "• `/analyze ETH-USD` - Ethereum\n"
                "• `/analyze ANTM.JK` - Indonesian stock",
                parse_mode='Markdown'
            )
            return
        
        symbol = ' '.join(context.args)
        formatted_symbol = self.format_symbol(symbol)
        
        is_crypto = self.is_crypto(formatted_symbol)
        asset_type = self.get_asset_type(formatted_symbol)
        
        # Send "analyzing" message
        analyzing_msg = await update.message.reply_text(
            f"🔍 Analyzing {formatted_symbol} ({asset_type})...\n"
            f"⏳ Fetching data and running AI analysis..."
        )
        
        try:
            # Perform analysis
            signal_info = await self.trading_bot.analyze_stock(formatted_symbol)
            
            if signal_info:
                # Format result message
                signal_emoji = {
                    'BUY': "🟢",
                    'SELL': "🔴", 
                    'STRONG_SELL': "🚨",
                    'HOLD': "🟡"
                }.get(signal_info['signal'], "⚪")
                
                strength_emoji = {
                    'VERY_STRONG': "🚨🚨",
                    'STRONG': "💪",
                    'MODERATE': "👍",
                    'WEAK': "👎"
                }.get(signal_info['strength'], "")
                
                # Currency formatting
                if is_crypto:
                    price_format = f"${signal_info['current_price']:,.2f}"
                    sl_format = f"${signal_info['stop_loss_price']:,.2f}"
                    tp_format = f"${signal_info['take_profit_price']:,.2f}"
                else:
                    price_format = f"{signal_info['current_price']:,} IDR"
                    sl_format = f"{signal_info['stop_loss_price']:,} IDR"
                    tp_format = f"{signal_info['take_profit_price']:,} IDR"
                
                result_message = f"""
{signal_emoji} **{formatted_symbol} ANALYSIS** {strength_emoji}

📊 **Signal:** {signal_info['signal']}
📝 **Reason:** {signal_info['signal_reason']}
💰 **Price:** {price_format} ({signal_info['price_change']:+.2f}%)
📈 **RSI:** {signal_info['rsi']:.1f} ({'Overbought' if signal_info['rsi'] > 80 else 'Oversold' if signal_info['rsi'] < 20 else 'Neutral'})

📊 **Technical Levels:**
🎯 **Stop Loss:** {sl_format} (-15%)
🎯 **Take Profit:** {tp_format} (+25%)
📈 **SMA 20:** {f"${signal_info['sma_short']:,.2f}" if is_crypto else f"{signal_info['sma_short']:,} IDR"}
📈 **SMA 50:** {f"${signal_info['sma_long']:,.2f}" if is_crypto else f"{signal_info['sma_long']:,} IDR"}

✅ **Valid Signal:** {'Yes' if signal_info['valid'] else 'No'}
💪 **Strength:** {signal_info['strength']}

⚠️ *This is educational analysis. DYOR before trading!*
                """
                
                # Edit the analyzing message with results
                await analyzing_msg.edit_text(result_message, parse_mode='Markdown')
                
                logger.info(f"Analysis sent for {formatted_symbol}: {signal_info['signal']}")
                
            else:
                await analyzing_msg.edit_text(
                    f"❌ Could not analyze {formatted_symbol}\n\n"
                    f"Please check if the symbol is correct:\n"
                    f"• Crypto: BTC, ETH-USD, BNB-USD\n"
                    f"• Stocks: ANTM.JK, BBCA.JK, TLKM.JK"
                )
                
        except Exception as e:
            logger.error(f"Error analyzing {formatted_symbol}: {e}")
            await analyzing_msg.edit_text(
                f"❌ Error analyzing {formatted_symbol}\n"
                f"Please try again or check the symbol format."
            )
    
    async def signals_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /signals command"""
        await update.message.reply_text("🔄 Getting signals for watchlist assets...")
        
        # Get user's watchlist or use default
        user_id = update.effective_user.id
        watchlist = self.user_watchlists.get(user_id, WATCHLIST_STOCKS[:3])  # Default to first 3
        
        if not watchlist:
            await update.message.reply_text(
                "📋 Your watchlist is empty!\n"
                "Use `/watchlist add BTC` to add assets."
            )
            return
        
        signals = []
        for symbol in watchlist:
            try:
                signal_info = await self.trading_bot.analyze_stock(symbol)
                if signal_info:
                    signals.append(signal_info)
            except Exception as e:
                logger.error(f"Error getting signal for {symbol}: {e}")
        
        if signals:
            message = "📊 **WATCHLIST SIGNALS**\n\n"
            
            for signal in signals:
                signal_emoji = {
                    'BUY': "🟢", 'SELL': "🔴", 
                    'STRONG_SELL': "🚨", 'HOLD': "🟡"
                }.get(signal['signal'], "⚪")
                
                is_crypto = self.is_crypto(signal['symbol'])
                price_format = f"${signal['current_price']:,.2f}" if is_crypto else f"{signal['current_price']:,} IDR"
                
                message += f"{signal_emoji} **{signal['symbol']}**: {signal['signal']}\n"
                message += f"💰 {price_format} ({signal['price_change']:+.2f}%) | RSI: {signal['rsi']:.0f}\n\n"
            
            message += "Use `/analyze <symbol>` for detailed analysis!"
            await update.message.reply_text(message, parse_mode='Markdown')
        else:
            await update.message.reply_text("❌ Could not get signals. Please try again.")
    
    async def watchlist_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /watchlist command"""
        user_id = update.effective_user.id
        
        if not context.args:
            # Show current watchlist
            watchlist = self.user_watchlists.get(user_id, WATCHLIST_STOCKS[:5])
            
            message = "📋 **YOUR WATCHLIST**\n\n"
            for i, symbol in enumerate(watchlist, 1):
                asset_type = "🪙" if self.is_crypto(symbol) else "📊"
                message += f"{i}. {asset_type} {symbol}\n"
            
            message += f"\n📊 Total: {len(watchlist)} assets\n\n"
            message += "**Commands:**\n"
            message += "• `/watchlist add BTC` - Add asset\n"
            message += "• `/watchlist remove ETH` - Remove asset\n"
            message += "• `/watchlist clear` - Clear all"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        elif context.args[0].lower() == 'add' and len(context.args) > 1:
            # Add to watchlist
            symbol = self.format_symbol(context.args[1])
            
            if user_id not in self.user_watchlists:
                self.user_watchlists[user_id] = []
            
            if symbol not in self.user_watchlists[user_id]:
                self.user_watchlists[user_id].append(symbol)
                asset_type = "cryptocurrency" if self.is_crypto(symbol) else "stock"
                await update.message.reply_text(f"✅ Added {symbol} ({asset_type}) to your watchlist!")
            else:
                await update.message.reply_text(f"ℹ️ {symbol} is already in your watchlist.")
                
        elif context.args[0].lower() == 'remove' and len(context.args) > 1:
            # Remove from watchlist
            symbol = self.format_symbol(context.args[1])
            
            if user_id in self.user_watchlists and symbol in self.user_watchlists[user_id]:
                self.user_watchlists[user_id].remove(symbol)
                await update.message.reply_text(f"✅ Removed {symbol} from your watchlist!")
            else:
                await update.message.reply_text(f"ℹ️ {symbol} is not in your watchlist.")
                
        elif context.args[0].lower() == 'clear':
            # Clear watchlist
            self.user_watchlists[user_id] = []
            await update.message.reply_text("✅ Cleared your watchlist!")
            
        else:
            await update.message.reply_text(
                "Usage:\n"
                "• `/watchlist` - Show watchlist\n"
                "• `/watchlist add BTC` - Add asset\n"
                "• `/watchlist remove ETH` - Remove asset\n"
                "• `/watchlist clear` - Clear all"
            )
    
    async def notifications_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /notifications command"""
        message = """
🔔 **NOTIFICATION SETTINGS**

📊 **Current Status:** Enabled ✅
🎯 **Signal Alerts:** On
📈 **Price Alerts:** On (5%+ moves)
📊 **Volume Alerts:** On (2x+ volume)

**Available Commands:**
• `/notifications on` - Enable all notifications
• `/notifications off` - Disable notifications
• `/notifications signals` - Only signal notifications
• `/notifications price` - Only price alerts

💡 All analysis includes AI confirmation with 70%+ confidence threshold.
        """
        await update.message.reply_text(message, parse_mode='Markdown')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular messages (symbols without commands)"""
        text = update.message.text.strip()
        
        # Check if it looks like a symbol
        if len(text) <= 10 and text.replace('-', '').replace('.', '').isalnum():
            # Treat as symbol for quick analysis
            formatted_symbol = self.format_symbol(text)
            
            # Quick analysis message
            quick_msg = await update.message.reply_text(f"🔍 Quick analysis: {formatted_symbol}...")
            
            try:
                signal_info = await self.trading_bot.analyze_stock(formatted_symbol)
                
                if signal_info:
                    signal_emoji = {'BUY': "🟢", 'SELL': "🔴", 'STRONG_SELL': "🚨", 'HOLD': "🟡"}.get(signal_info['signal'], "⚪")
                    is_crypto = self.is_crypto(formatted_symbol)
                    price = f"${signal_info['current_price']:,.2f}" if is_crypto else f"{signal_info['current_price']:,} IDR"
                    
                    quick_result = f"""
{signal_emoji} **{formatted_symbol}**: {signal_info['signal']}
💰 {price} ({signal_info['price_change']:+.2f}%)
📊 RSI: {signal_info['rsi']:.0f}

Use `/analyze {text}` for detailed analysis!
                    """
                    await quick_msg.edit_text(quick_result, parse_mode='Markdown')
                else:
                    await quick_msg.edit_text(f"❌ Could not analyze {formatted_symbol}")
                    
            except Exception as e:
                await quick_msg.edit_text(f"❌ Error analyzing {formatted_symbol}")
        else:
            # Not a symbol, provide help
            await update.message.reply_text(
                "💡 Send a symbol for quick analysis (e.g., `BTC`, `ETH`, `ANTM.JK`) or use `/help` for commands!"
            )
    
    async def run(self):
        """Run the interactive bot"""
        logger.info("Starting Interactive Trading Bot...")
        
        # Send startup message
        if self.chat_id:
            try:
                startup_msg = """
🚀 **Interactive Trading Bot Started!**

Ready to analyze crypto & stocks with AI-powered insights!

Type `/help` to see all commands or just send a symbol like `BTC` for quick analysis.
                """
                await Bot(self.bot_token).send_message(
                    chat_id=self.chat_id,
                    text=startup_msg,
                    parse_mode='Markdown'
                )
            except Exception as e:
                logger.error(f"Could not send startup message: {e}")
        
        # Start the bot
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling(drop_pending_updates=True)
        
        try:
            # Keep running
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        finally:
            await self.application.stop()

async def main():
    """Main function"""
    try:
        bot = InteractiveTradingBot()
        await bot.run()
    except Exception as e:
        logger.error(f"Error running bot: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 