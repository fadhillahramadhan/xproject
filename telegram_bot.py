import os
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List
import json

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode
import pandas as pd
from dotenv import load_dotenv

from technical_analyzer import MurphyTechnicalAnalyzer
from chart_generator import TechnicalChartGenerator

# Load environment variables
load_dotenv('config.env')

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class CryptoTradingBot:
    """Telegram bot for crypto technical analysis based on Murphy's principles"""
    
    def __init__(self):
        self.analyzer = MurphyTechnicalAnalyzer()
        self.chart_generator = TechnicalChartGenerator()
        self.default_symbols = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'ADA/USDT', 'SOL/USDT']
        self.user_watchlists = {}  # Store user-specific watchlists
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start command handler"""
        welcome_message = """
🚀 **Murphy's Crypto Trading Bot** 🚀

Based on John J. Murphy's Technical Analysis principles!

**Available Commands:**
📊 `/analyze <symbol>` - Analyze a specific crypto (e.g., /analyze BTC/USDT)
📈 `/signals` - Get signals for all watchlist coins
🔍 `/watchlist` - Manage your watchlist
⚙️ `/settings` - Bot settings
📚 `/help` - Show this help message

**Features:**
✅ Murphy's Technical Analysis Methods
✅ RSI, MACD, Bollinger Bands
✅ Support/Resistance Levels
✅ Chart Pattern Detection
✅ Risk/Reward Calculations
✅ Visual Charts

Type `/signals` to get started with default crypto analysis!
        """
        
        await update.message.reply_text(welcome_message, parse_mode=ParseMode.MARKDOWN)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Help command handler"""
        help_text = """
📚 **Murphy's Crypto Bot - Help**

**Commands:**
• `/start` - Welcome message
• `/analyze BTC/USDT` - Analyze specific symbol
• `/signals` - Get all watchlist signals
• `/watchlist` - Manage watchlist
• `/settings` - Configure bot settings

**Analysis Features:**
🔹 **Trend Analysis** - Moving averages, MACD
🔹 **Momentum** - RSI, Stochastic indicators  
🔹 **Pattern Detection** - Head & Shoulders, Triangles, Double tops/bottoms
🔹 **Support/Resistance** - Key levels identification
🔹 **Volume Analysis** - Volume confirmation
🔹 **Risk Management** - Stop loss and take profit levels

**Signal Strength:**
🟢 **STRONG** - High confidence (80%+)
🟡 **MEDIUM** - Moderate confidence (60-80%)
🔴 **WEAK** - Low confidence (<60%)

Based on John J. Murphy's "Technical Analysis of Financial Markets"
        """
        
        await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)
    
    async def analyze_symbol(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Analyze a specific symbol"""
        try:
            if not context.args:
                await update.message.reply_text("Please provide a symbol. Example: `/analyze BTC/USDT`", 
                                               parse_mode=ParseMode.MARKDOWN)
                return
            
            symbol = context.args[0].upper()
            
            # Send "analyzing" message
            analyzing_msg = await update.message.reply_text(f"🔍 Analyzing {symbol}...")
            
            # Perform analysis
            signals = self.analyzer.analyze_symbol(symbol)
            
            if signals['signal'] == 'NO_DATA':
                await analyzing_msg.edit_text(f"❌ Unable to fetch data for {symbol}. Please check the symbol format.")
                return
            
            # Generate chart
            df = self.analyzer.get_ohlcv_data(symbol)
            if not df.empty:
                chart_buffer = self.chart_generator.create_analysis_chart(df, signals, symbol)
                
                # Send chart
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=chart_buffer,
                    caption=self.format_signal_message(signals)
                )
            else:
                # Send text-only analysis
                await analyzing_msg.edit_text(self.format_signal_message(signals), 
                                            parse_mode=ParseMode.MARKDOWN)
            
            # Delete analyzing message
            await analyzing_msg.delete()
            
        except Exception as e:
            logger.error(f"Error in analyze_symbol: {e}")
            await update.message.reply_text(f"❌ Error analyzing {symbol}: {str(e)}")
    
    async def get_signals(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Get signals for all watchlist symbols"""
        try:
            user_id = update.effective_user.id
            symbols = self.user_watchlists.get(user_id, self.default_symbols)
            
            signals_msg = await update.message.reply_text("🔍 Analyzing watchlist symbols...")
            
            all_signals = []
            for symbol in symbols[:5]:  # Limit to 5 symbols to avoid spam
                signals = self.analyzer.analyze_symbol(symbol)
                if signals['signal'] != 'NO_DATA':
                    all_signals.append(signals)
            
            if not all_signals:
                await signals_msg.edit_text("❌ No data available for watchlist symbols.")
                return
            
            # Create summary message
            summary = self.format_signals_summary(all_signals)
            
            # Create keyboard for detailed analysis
            keyboard = []
            for signals in all_signals:
                if signals['signal'] in ['BUY', 'SELL']:
                    emoji = "🟢" if signals['signal'] == 'BUY' else "🔴"
                    keyboard.append([InlineKeyboardButton(
                        f"{emoji} {signals['symbol']} - {signals['signal']}",
                        callback_data=f"detail_{signals['symbol']}"
                    )])
            
            reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None
            
            await signals_msg.edit_text(summary, parse_mode=ParseMode.MARKDOWN, 
                                      reply_markup=reply_markup)
            
        except Exception as e:
            logger.error(f"Error in get_signals: {e}")
            await update.message.reply_text(f"❌ Error getting signals: {str(e)}")
    
    async def manage_watchlist(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manage user watchlist"""
        user_id = update.effective_user.id
        current_watchlist = self.user_watchlists.get(user_id, self.default_symbols)
        
        keyboard = [
            [InlineKeyboardButton("➕ Add Symbol", callback_data="watchlist_add")],
            [InlineKeyboardButton("➖ Remove Symbol", callback_data="watchlist_remove")],
            [InlineKeyboardButton("🔄 Reset to Default", callback_data="watchlist_reset")]
        ]
        
        watchlist_text = f"""
📋 **Your Watchlist:**
{chr(10).join([f"• {symbol}" for symbol in current_watchlist])}

**Manage your watchlist:**
        """
        
        await update.message.reply_text(watchlist_text, parse_mode=ParseMode.MARKDOWN,
                                       reply_markup=InlineKeyboardMarkup(keyboard))
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data.startswith("detail_"):
            symbol = data.replace("detail_", "")
            await self.send_detailed_analysis(query, symbol)
        elif data.startswith("watchlist_"):
            await self.handle_watchlist_action(query, data)
    
    async def send_detailed_analysis(self, query, symbol: str):
        """Send detailed analysis for a specific symbol"""
        try:
            # Perform analysis
            signals = self.analyzer.analyze_symbol(symbol)
            
            if signals['signal'] == 'NO_DATA':
                await query.edit_message_text(f"❌ Unable to fetch data for {symbol}")
                return
            
            # Generate and send chart
            df = self.analyzer.get_ohlcv_data(symbol)
            if not df.empty:
                chart_buffer = self.chart_generator.create_analysis_chart(df, signals, symbol)
                
                await query.message.reply_photo(
                    photo=chart_buffer,
                    caption=self.format_detailed_signal_message(signals)
                )
            else:
                await query.edit_message_text(self.format_detailed_signal_message(signals),
                                            parse_mode=ParseMode.MARKDOWN)
                
        except Exception as e:
            logger.error(f"Error in detailed analysis: {e}")
            await query.edit_message_text(f"❌ Error analyzing {symbol}: {str(e)}")
    
    async def handle_watchlist_action(self, query, data: str):
        """Handle watchlist management actions"""
        user_id = query.from_user.id
        
        if data == "watchlist_reset":
            self.user_watchlists[user_id] = self.default_symbols.copy()
            await query.edit_message_text("✅ Watchlist reset to default symbols!")
        elif data == "watchlist_add":
            await query.edit_message_text("""
➕ **Add Symbol to Watchlist**

Send me the symbol you want to add (e.g., DOT/USDT)
Use format: SYMBOL/USDT

Reply with the symbol or type /cancel to cancel.
            """, parse_mode=ParseMode.MARKDOWN)
        elif data == "watchlist_remove":
            current_watchlist = self.user_watchlists.get(user_id, self.default_symbols)
            keyboard = []
            for symbol in current_watchlist:
                keyboard.append([InlineKeyboardButton(
                    f"➖ {symbol}",
                    callback_data=f"remove_{symbol}"
                )])
            keyboard.append([InlineKeyboardButton("❌ Cancel", callback_data="watchlist_cancel")])
            
            await query.edit_message_text("Select symbol to remove:",
                                        reply_markup=InlineKeyboardMarkup(keyboard))
    
    def format_signal_message(self, signals: Dict) -> str:
        """Format signal data into readable message"""
        signal_emoji = {
            'BUY': '🟢',
            'SELL': '🔴',
            'HOLD': '🟡',
            'NO_DATA': '⚫'
        }
        
        strength_emoji = {
            'STRONG': '🔥',
            'MEDIUM': '⚡',
            'WEAK': '💧',
            'NONE': '❓'
        }
        
        message = f"""
{signal_emoji.get(signals['signal'], '❓')} **{signals.get('symbol', 'Unknown')} Signal**

🎯 **Signal:** {signals['signal']} {strength_emoji.get(signals['strength'], '')}
💪 **Strength:** {signals['strength']}
🎲 **Confidence:** {signals['confidence']}%
💰 **Price:** ${signals['price']:.4f}

**📊 Technical Indicators:**
📈 RSI: {signals['indicators'].get('rsi', 'N/A')}
📊 SMA20: ${signals['indicators'].get('sma_20', 'N/A')}
📊 SMA50: ${signals['indicators'].get('sma_50', 'N/A')}

**💼 Trade Setup:**
🎯 Entry: ${signals['entry_price']:.4f}
🛡️ Stop Loss: ${signals['stop_loss']:.4f}  
🎯 Take Profit: ${signals['take_profit']:.4f}
📊 Risk/Reward: 1:{signals['risk_reward']}

**🔍 Pattern Analysis:**
"""
        
        # Add pattern information
        patterns = signals.get('patterns', {})
        active_patterns = [f"{k.replace('_', ' ').title()}: {v}" for k, v in patterns.items() if v != 'NONE']
        if active_patterns:
            message += "\n".join(active_patterns)
        else:
            message += "No significant patterns detected"
        
        message += f"\n\n⏰ Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return message
    
    def format_detailed_signal_message(self, signals: Dict) -> str:
        """Format detailed signal message"""
        base_message = self.format_signal_message(signals)
        
        # Add detailed analysis
        analysis = signals.get('analysis', {})
        detailed_info = "\n\n**🔬 Detailed Analysis:**\n"
        
        for category, signals_list in analysis.items():
            if signals_list:
                detailed_info += f"• **{category.replace('_', ' ').title()}:** {', '.join(signals_list)}\n"
        
        return base_message + detailed_info
    
    def format_signals_summary(self, all_signals: List[Dict]) -> str:
        """Format summary of multiple signals"""
        summary = "📊 **Watchlist Signals Summary**\n\n"
        
        buy_signals = []
        sell_signals = []
        hold_signals = []
        
        for signals in all_signals:
            symbol = signals['symbol']
            signal = signals['signal']
            confidence = signals['confidence']
            strength = signals['strength']
            
            signal_text = f"{symbol}: {signal} ({strength}, {confidence}%)"
            
            if signal == 'BUY':
                buy_signals.append(f"🟢 {signal_text}")
            elif signal == 'SELL':
                sell_signals.append(f"🔴 {signal_text}")
            else:
                hold_signals.append(f"🟡 {signal_text}")
        
        if buy_signals:
            summary += "**🟢 BUY Signals:**\n" + "\n".join(buy_signals) + "\n\n"
        if sell_signals:
            summary += "**🔴 SELL Signals:**\n" + "\n".join(sell_signals) + "\n\n"
        if hold_signals:
            summary += "**🟡 HOLD/NEUTRAL:**\n" + "\n".join(hold_signals) + "\n\n"
        
        summary += "📈 Click on any signal for detailed analysis and chart!"
        
        return summary
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle general messages"""
        text = update.message.text.upper()
        
        # Check if it's a symbol format
        if '/' in text and len(text.split('/')) == 2:
            # Treat as symbol analysis
            context.args = [text]
            await self.analyze_symbol(update, context)
        else:
            await update.message.reply_text(
                "Send me a crypto symbol (e.g., BTC/USDT) or use /help for available commands."
            )

def main():
    """Start the bot"""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        print("❌ Please set TELEGRAM_BOT_TOKEN in config.env file")
        return
    
    # Create bot instance
    bot = CryptoTradingBot()
    
    # Create application
    application = Application.builder().token(token).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CommandHandler("help", bot.help_command))
    application.add_handler(CommandHandler("analyze", bot.analyze_symbol))
    application.add_handler(CommandHandler("signals", bot.get_signals))
    application.add_handler(CommandHandler("watchlist", bot.manage_watchlist))
    application.add_handler(CallbackQueryHandler(bot.button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))
    
    # Start the bot
    print("🚀 Murphy's Crypto Trading Bot is starting...")
    print("📊 Based on John J. Murphy's Technical Analysis principles")
    
    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except KeyboardInterrupt:
        print("\n⛔ Bot stopped by user")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")

if __name__ == '__main__':
    main() 