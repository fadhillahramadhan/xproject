"""
Indonesian Stock Trading Bot with SMA Crossover Strategy
End-of-Day (EOD) Trading Signals via Telegram
Enhanced with comprehensive SELL signal detection
"""

import yfinance as yf
import pandas as pd
import numpy as np
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import os
from dotenv import load_dotenv
from telegram import Bot
from telegram.error import TelegramError
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from io import BytesIO
import schedule
import time
import random
import json
import base64
from openai import AsyncOpenAI

# Import configuration
from config import (
    INDONESIAN_STOCKS, SMA_SHORT_PERIOD, SMA_LONG_PERIOD, DATA_PERIOD,
    MIN_VOLUME_THRESHOLD, MIN_PRICE_CHANGE, SIGNAL_BUY, SIGNAL_SELL, SIGNAL_STRONG_SELL, SIGNAL_HOLD,
    STOP_LOSS_PERCENTAGE, TAKE_PROFIT_PERCENTAGE, RSI_OVERBOUGHT_THRESHOLD, RSI_OVERSOLD_THRESHOLD,
    RSI_PERIOD, BEARISH_DIVERGENCE_THRESHOLD, HIGH_VOLUME_SELL_MULTIPLIER,
    ENABLE_CHATGPT_CONFIRMATION, CHATGPT_MODEL, CHATGPT_CONFIDENCE_THRESHOLD, CHATGPT_MAX_RETRIES,
    ENABLE_SENTIMENT_ANALYSIS, SENTIMENT_WEIGHT,
    ENABLE_CHATGPT_VISION, CHATGPT_VISION_MODEL, ENABLE_CHART_PATTERN_ANALYSIS, 
    ENABLE_TECHNICAL_INDICATOR_VALIDATION, CHART_IMAGE_QUALITY,
    ENABLE_WATCHLIST, WATCHLIST_STOCKS, WATCHLIST_ALERT_THRESHOLD, WATCHLIST_PRIORITY_MULTIPLIER,
    ENABLE_WATCHLIST_DAILY_SUMMARY, WATCHLIST_PRICE_ALERT_PERCENTAGE, ENABLE_WATCHLIST_VOLUME_ALERTS,
    ENABLE_HOLD_SIGNALS, HOLD_SIGNAL_CONFIDENCE_THRESHOLD, SEND_HOLD_SIGNALS_REGARDLESS_OF_CONFIDENCE
)

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class IndonesianStockBot:
    """Indonesian Stock Trading Bot with Enhanced SMA Crossover and Sell Signal Strategy"""
    
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        
        if not self.bot_token or not self.chat_id:
            raise ValueError("Please set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env file")
        
        # Initialize OpenAI client if API key is provided
        self.openai_client = None
        if self.openai_api_key and ENABLE_CHATGPT_CONFIRMATION:
            try:
                self.openai_client = AsyncOpenAI(api_key=self.openai_api_key)
                logger.info("OpenAI client initialized for ChatGPT confirmation")
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI client: {e}")
                logger.warning("ChatGPT confirmation will be disabled")
        elif not self.openai_api_key and ENABLE_CHATGPT_CONFIRMATION:
            logger.warning("OPENAI_API_KEY not found in .env file. ChatGPT confirmation disabled.")
        
        self.telegram_bot = Bot(token=self.bot_token)
        self.signals_history = []
        self.watchlist_data = {}  # Store watchlist stock data
        self.watchlist_alerts = []  # Store watchlist alerts
        
        logger.info("Indonesian Stock Trading Bot initialized with enhanced sell signals")
        if ENABLE_WATCHLIST:
            logger.info(f"Watchlist enabled with {len(WATCHLIST_STOCKS)} stocks: {', '.join(WATCHLIST_STOCKS)}")
    
    def fetch_stock_data(self, symbol: str) -> Optional[pd.DataFrame]:
        """Fetch stock data from Yahoo Finance with rate limiting and retry logic"""
        max_retries = 3
        base_delay = 2  # Base delay in seconds
        
        for attempt in range(max_retries):
            try:
                # Add random delay to avoid rate limiting
                if attempt > 0:
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                    logger.info(f"Retry {attempt + 1} for {symbol}, waiting {delay:.1f}s...")
                    time.sleep(delay)
                
                # Create ticker with session for better connection handling
                stock = yf.Ticker(symbol)
                
                # Try different periods if 60d fails
                periods_to_try = [DATA_PERIOD, "30d", "1mo", "3mo"]
                
                for period in periods_to_try:
                    try:
                        logger.info(f"Fetching {symbol} data for period: {period}")
                        data = stock.history(period=period)
                        
                        if not data.empty and len(data) >= max(SMA_LONG_PERIOD, RSI_PERIOD):
                            logger.info(f"Successfully fetched {len(data)} days of data for {symbol}")
                            return data
                        elif not data.empty:
                            logger.warning(f"Insufficient data for {symbol}: {len(data)} days (need {max(SMA_LONG_PERIOD, RSI_PERIOD)})")
                        else:
                            logger.warning(f"No data found for {symbol} with period {period}")
                            
                    except Exception as period_error:
                        logger.warning(f"Failed to fetch {symbol} with period {period}: {period_error}")
                        continue
                
                # If we get here, all periods failed
                logger.error(f"All periods failed for {symbol}")
                return None
                
            except Exception as e:
                error_msg = str(e).lower()
                
                if "429" in error_msg or "too many requests" in error_msg:
                    logger.warning(f"Rate limited for {symbol}, attempt {attempt + 1}/{max_retries}")
                    if attempt < max_retries - 1:
                        continue
                    else:
                        logger.error(f"Rate limit exceeded for {symbol} after {max_retries} attempts")
                        return None
                        
                elif "404" in error_msg or "not found" in error_msg:
                    logger.error(f"Symbol {symbol} not found")
                    return None
                    
                else:
                    logger.error(f"Error fetching data for {symbol}: {e}")
                    if attempt < max_retries - 1:
                        continue
                    else:
                        return None
        
        logger.error(f"Failed to fetch data for {symbol} after {max_retries} attempts")
        return None
    
    def calculate_rsi(self, data: pd.DataFrame, period: int = RSI_PERIOD) -> pd.Series:
        """Calculate Relative Strength Index (RSI)"""
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_technical_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate all technical indicators including SMAs and RSI"""
        data = data.copy()
        
        # Simple Moving Averages
        data[f'SMA_{SMA_SHORT_PERIOD}'] = data['Close'].rolling(window=SMA_SHORT_PERIOD).mean()
        data[f'SMA_{SMA_LONG_PERIOD}'] = data['Close'].rolling(window=SMA_LONG_PERIOD).mean()
        
        # RSI
        data['RSI'] = self.calculate_rsi(data)
        
        # Volume Moving Average for volume analysis
        data['Volume_MA'] = data['Volume'].rolling(window=20).mean()
        
        # Price change percentage
        data['Price_Change_Pct'] = data['Close'].pct_change() * 100
        
        # High and Low of recent periods for stop-loss/take-profit
        data['Recent_High'] = data['High'].rolling(window=10).max()
        data['Recent_Low'] = data['Low'].rolling(window=10).min()
        
        return data
    
    def generate_enhanced_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Generate enhanced trading signals with comprehensive sell logic"""
        data = data.copy()
        
        # Calculate technical indicators
        data = self.calculate_technical_indicators(data)
        
        # Initialize signals
        data['Signal'] = SIGNAL_HOLD
        data['Position'] = 0
        data['Signal_Reason'] = 'No Signal'
        data['Signal_Strength'] = 'WEAK'
        
        # Get technical indicator values
        sma_short = data[f'SMA_{SMA_SHORT_PERIOD}']
        sma_long = data[f'SMA_{SMA_LONG_PERIOD}']
        rsi = data['RSI']
        volume_ratio = data['Volume'] / data['Volume_MA']
        
        # BUY SIGNALS - LONG TERM FOCUSED
        # 1. SMA Crossover + RSI not extremely overbought
        buy_sma_cross = (sma_short > sma_long) & (sma_short.shift(1) <= sma_long.shift(1))
        buy_rsi_ok = rsi < RSI_OVERBOUGHT_THRESHOLD
        buy_condition = buy_sma_cross & buy_rsi_ok
        
        # 2. RSI Oversold Recovery (more conservative)
        rsi_oversold_recovery = (rsi > RSI_OVERSOLD_THRESHOLD) & (rsi.shift(1) <= RSI_OVERSOLD_THRESHOLD)
        buy_condition = buy_condition | (rsi_oversold_recovery & (sma_short > sma_long))
        
        # 3. Strong uptrend continuation (new for long-term)
        strong_uptrend = (sma_short > sma_long) & (data['Close'] > sma_short) & (rsi > 50) & (rsi < RSI_OVERBOUGHT_THRESHOLD)
        price_momentum = data['Close'] > data['Close'].shift(5)  # Price higher than 5 days ago
        buy_condition = buy_condition | (strong_uptrend & price_momentum)
        
        # SELL SIGNALS - LONG TERM FOCUSED (More Conservative)
        # 1. SMA Crossover (bearish) - Only if confirmed by multiple periods
        sell_sma_cross = (sma_short < sma_long) & (sma_short.shift(1) >= sma_long.shift(1))
        sma_cross_confirmed = sell_sma_cross & (sma_short.shift(2) >= sma_long.shift(2))  # Confirmation
        
        # 2. RSI Extremely Overbought (raised threshold)
        sell_rsi_overbought = rsi > RSI_OVERBOUGHT_THRESHOLD
        
        # 3. High volume sell-off (more conservative)
        sell_high_volume = (volume_ratio > HIGH_VOLUME_SELL_MULTIPLIER) & (data['Price_Change_Pct'] < -5)  # Increased from -2%
        
        # 4. Bearish divergence (more conservative for long-term)
        price_trend = data['Close'].rolling(10).mean() > data['Close'].rolling(10).mean().shift(10)  # Longer period
        rsi_trend = rsi < rsi.shift(10)  # Longer period
        sell_divergence = price_trend & rsi_trend & (rsi > 70)  # Higher RSI threshold
        
        # STRONG SELL SIGNALS - LONG TERM FOCUSED
        # 1. Multiple bearish indicators with confirmation
        strong_sell_multiple = sma_cross_confirmed & sell_rsi_overbought
        
        # 2. Extreme overbought with high volume (more conservative)
        strong_sell_extreme = (rsi > 85) & (volume_ratio > HIGH_VOLUME_SELL_MULTIPLIER)  # Raised from 80
        
        # 3. Large price drop with high volume (more conservative)
        strong_sell_crash = (data['Price_Change_Pct'] < -10) & (volume_ratio > HIGH_VOLUME_SELL_MULTIPLIER)  # Increased from -5%
        
        # Apply signals and reasons
        # Buy signals
        data.loc[buy_condition, 'Signal'] = SIGNAL_BUY
        data.loc[buy_condition, 'Position'] = 1
        data.loc[buy_sma_cross & buy_rsi_ok, 'Signal_Reason'] = 'Long-term SMA Crossover'
        data.loc[rsi_oversold_recovery & (sma_short > sma_long), 'Signal_Reason'] = 'RSI Oversold Recovery'
        data.loc[strong_uptrend & price_momentum, 'Signal_Reason'] = 'Strong Uptrend Continuation'
        
        # Regular sell signals (more conservative)
        regular_sell = (sma_cross_confirmed | sell_rsi_overbought | sell_high_volume | sell_divergence) & ~(strong_sell_multiple | strong_sell_extreme | strong_sell_crash)
        data.loc[regular_sell, 'Signal'] = SIGNAL_SELL
        data.loc[regular_sell, 'Position'] = -1
        
        # Strong sell signals
        strong_sell = strong_sell_multiple | strong_sell_extreme | strong_sell_crash
        data.loc[strong_sell, 'Signal'] = SIGNAL_STRONG_SELL
        data.loc[strong_sell, 'Position'] = -2
        
        # Set signal reasons for sells
        data.loc[sma_cross_confirmed, 'Signal_Reason'] = 'Confirmed SMA Bearish Crossover'
        data.loc[sell_rsi_overbought, 'Signal_Reason'] = 'RSI Extremely Overbought (80+)'
        data.loc[sell_high_volume, 'Signal_Reason'] = 'Major High Volume Sell-off'
        data.loc[sell_divergence, 'Signal_Reason'] = 'Long-term Bearish Divergence'
        data.loc[strong_sell_multiple, 'Signal_Reason'] = 'Multiple Confirmed Bearish Signals'
        data.loc[strong_sell_extreme, 'Signal_Reason'] = 'Extreme Overbought (85+)'
        data.loc[strong_sell_crash, 'Signal_Reason'] = 'Major Price Crash (-10%+)'
        
        return data
    
    def validate_signal(self, data: pd.DataFrame, symbol: str) -> Dict:
        """Validate and analyze the latest signal with enhanced sell information"""
        latest_data = data.iloc[-1]
        previous_data = data.iloc[-2] if len(data) > 1 else latest_data
        
        # Calculate stop-loss and take-profit levels for current position
        current_price = latest_data['Close']
        stop_loss_price = current_price * (1 - STOP_LOSS_PERCENTAGE)
        take_profit_price = current_price * (1 + TAKE_PROFIT_PERCENTAGE)
        
        signal_info = {
            'symbol': symbol,
            'date': latest_data.name.strftime('%Y-%m-%d'),
            'signal': latest_data['Signal'],
            'signal_reason': latest_data['Signal_Reason'],
            'current_price': round(latest_data['Close'], 2),
            'previous_close': round(previous_data['Close'], 2),
            'price_change': round(((latest_data['Close'] - previous_data['Close']) / previous_data['Close']) * 100, 2),
            'volume': int(latest_data['Volume']),
            'volume_ratio': round(latest_data['Volume'] / latest_data['Volume_MA'], 2) if not pd.isna(latest_data['Volume_MA']) else 1.0,
            'sma_short': round(latest_data[f'SMA_{SMA_SHORT_PERIOD}'], 2),
            'sma_long': round(latest_data[f'SMA_{SMA_LONG_PERIOD}'], 2),
            'rsi': round(latest_data['RSI'], 2) if not pd.isna(latest_data['RSI']) else 50,
            'stop_loss_price': round(stop_loss_price, 2),
            'take_profit_price': round(take_profit_price, 2),
            'recent_high': round(latest_data['Recent_High'], 2),
            'recent_low': round(latest_data['Recent_Low'], 2),
            'valid': False,
            'strength': 'WEAK'
        }
        
        # Validation criteria
        volume_valid = latest_data['Volume'] >= MIN_VOLUME_THRESHOLD
        price_change_significant = abs(signal_info['price_change']) >= MIN_PRICE_CHANGE * 100
        sma_valid = not (pd.isna(latest_data[f'SMA_{SMA_SHORT_PERIOD}']) or pd.isna(latest_data[f'SMA_{SMA_LONG_PERIOD}']))
        
        signal_info['valid'] = volume_valid and sma_valid
        
        # Determine signal strength
        if signal_info['signal'] == SIGNAL_STRONG_SELL:
            signal_info['strength'] = 'VERY_STRONG'
        elif signal_info['valid'] and price_change_significant:
            signal_info['strength'] = 'STRONG'
        elif signal_info['valid']:
            signal_info['strength'] = 'MODERATE'
        
        return signal_info
    
    def create_enhanced_chart(self, data: pd.DataFrame, symbol: str, signal_info: Dict) -> BytesIO:
        """Create an enhanced chart with RSI and sell signal indicators"""
        plt.style.use('dark_background')
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 12), height_ratios=[3, 1, 1])
        
        # Price and SMA plot
        ax1.plot(data.index, data['Close'], label='Close Price', color='white', linewidth=2)
        ax1.plot(data.index, data[f'SMA_{SMA_SHORT_PERIOD}'], label=f'SMA {SMA_SHORT_PERIOD}', color='orange', alpha=0.8)
        ax1.plot(data.index, data[f'SMA_{SMA_LONG_PERIOD}'], label=f'SMA {SMA_LONG_PERIOD}', color='blue', alpha=0.8)
        
        # Mark signals
        buy_signals = data[data['Signal'] == SIGNAL_BUY]
        sell_signals = data[data['Signal'] == SIGNAL_SELL]
        strong_sell_signals = data[data['Signal'] == SIGNAL_STRONG_SELL]
        
        if not buy_signals.empty:
            ax1.scatter(buy_signals.index, buy_signals['Close'], color='green', marker='^', s=100, label='Buy Signal', zorder=5)
        
        if not sell_signals.empty:
            ax1.scatter(sell_signals.index, sell_signals['Close'], color='red', marker='v', s=100, label='Sell Signal', zorder=5)
            
        if not strong_sell_signals.empty:
            ax1.scatter(strong_sell_signals.index, strong_sell_signals['Close'], color='darkred', marker='v', s=150, label='Strong Sell', zorder=5)
        
        # Add stop-loss and take-profit lines for current price
        current_price = signal_info['current_price']
        ax1.axhline(y=signal_info['stop_loss_price'], color='red', linestyle='--', alpha=0.7, label=f'Stop Loss ({signal_info["stop_loss_price"]})')
        ax1.axhline(y=signal_info['take_profit_price'], color='green', linestyle='--', alpha=0.7, label=f'Take Profit ({signal_info["take_profit_price"]})')
        
        ax1.set_title(f'{symbol} - Long-Term Trend Strategy\nCurrent: {signal_info["current_price"]} ({signal_info["price_change"]:+.2f}%) | RSI: {signal_info["rsi"]:.1f}', 
                     fontsize=14, fontweight='bold')
        ax1.set_ylabel('Price (IDR)', fontsize=12)
        ax1.legend(loc='upper left', fontsize=8)
        ax1.grid(True, alpha=0.3)
        
        # RSI plot
        ax2.plot(data.index, data['RSI'], label='RSI', color='yellow', linewidth=1.5)
        ax2.axhline(y=RSI_OVERBOUGHT_THRESHOLD, color='red', linestyle='--', alpha=0.7, label=f'Overbought ({RSI_OVERBOUGHT_THRESHOLD})')
        ax2.axhline(y=RSI_OVERSOLD_THRESHOLD, color='green', linestyle='--', alpha=0.7, label=f'Oversold ({RSI_OVERSOLD_THRESHOLD})')
        ax2.axhline(y=50, color='gray', linestyle='-', alpha=0.5)
        ax2.set_ylabel('RSI', fontsize=10)
        ax2.set_ylim(0, 100)
        ax2.legend(loc='upper left', fontsize=8)
        ax2.grid(True, alpha=0.3)
        
        # Volume plot with ratio
        colors = ['red' if ratio > HIGH_VOLUME_SELL_MULTIPLIER else 'gray' for ratio in data['Volume'] / data['Volume_MA']]
        ax3.bar(data.index, data['Volume'], color=colors, alpha=0.6)
        ax3.set_title('Volume (Red = High Volume Alert)', fontsize=10)
        ax3.set_ylabel('Volume', fontsize=10)
        ax3.grid(True, alpha=0.3)
        
        # Format x-axis
        ax3.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        ax3.xaxis.set_major_locator(mdates.WeekdayLocator())
        plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        
        # Save to BytesIO
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight', facecolor='black')
        img_buffer.seek(0)
        plt.close()
        
        return img_buffer
    
    def format_enhanced_signal_message(self, signal_info: Dict, chatgpt_confirmation: Optional[Dict] = None) -> str:
        """Format enhanced signal information for Telegram message"""
        emoji_map = {
            SIGNAL_BUY: "🟢",
            SIGNAL_SELL: "🔴",
            SIGNAL_STRONG_SELL: "🚨",
            SIGNAL_HOLD: "🟡"
        }
        
        strength_emoji = {
            'VERY_STRONG': "🚨🚨",
            'STRONG': "💪",
            'MODERATE': "👍",
            'WEAK': "👎"
        }
        
        signal_emoji = emoji_map.get(signal_info['signal'], "⚪")
        strength_emoji_icon = strength_emoji.get(signal_info['strength'], "")
        
        # RSI interpretation
        rsi_status = ""
        if signal_info['rsi'] > RSI_OVERBOUGHT_THRESHOLD:
            rsi_status = "🔴 OVERBOUGHT"
        elif signal_info['rsi'] < RSI_OVERSOLD_THRESHOLD:
            rsi_status = "🟢 OVERSOLD"
        else:
            rsi_status = "🟡 NEUTRAL"
        
        # Volume analysis
        volume_status = "🔴 HIGH VOLUME" if signal_info['volume_ratio'] > HIGH_VOLUME_SELL_MULTIPLIER else "🟡 NORMAL"
        
        # ChatGPT confirmation section
        chatgpt_section = ""
        if chatgpt_confirmation and ENABLE_CHATGPT_CONFIRMATION:
            confidence_emoji = "🟢" if chatgpt_confirmation['confidence'] >= 0.8 else "🟡" if chatgpt_confirmation['confidence'] >= 0.6 else "🔴"
            recommendation_emoji = {
                'CONFIRM': "✅",
                'REJECT': "❌", 
                'MODIFY': "⚠️",
                'PROCEED_WITH_CAUTION': "⚠️"
            }.get(chatgpt_confirmation.get('recommendation', 'CONFIRM'), "❓")
            
            risk_emoji = {
                'LOW': "🟢",
                'MEDIUM': "🟡",
                'HIGH': "🔴",
                'UNKNOWN': "❓"
            }.get(chatgpt_confirmation.get('risk_assessment', 'MEDIUM'), "❓")
            
            # Sentiment analysis section
            sentiment_section = ""
            if ENABLE_SENTIMENT_ANALYSIS and 'sentiment_analysis' in chatgpt_confirmation:
                sentiment_data = chatgpt_confirmation['sentiment_analysis']
                sentiment_emoji = {
                    'VERY_POSITIVE': "🚀",
                    'POSITIVE': "📈",
                    'NEUTRAL': "➡️",
                    'NEGATIVE': "📉",
                    'VERY_NEGATIVE': "💥"
                }.get(sentiment_data.get('overall_sentiment', 'NEUTRAL'), "❓")
                
                sentiment_score = sentiment_data.get('sentiment_score', 0.5)
                sentiment_color = "🟢" if sentiment_score >= 0.7 else "🟡" if sentiment_score >= 0.4 else "🔴"
                
                sentiment_section = f"\n📊 Sentiment: {sentiment_emoji} {sentiment_data.get('overall_sentiment', 'NEUTRAL')} ({sentiment_color} {sentiment_score:.0%})"
            
            # Analysis type indicator
            analysis_type_emoji = "👁️" if chatgpt_confirmation.get('vision_enabled', False) else "📊"
            analysis_type = chatgpt_confirmation.get('analysis_type', 'Statistical Only')
            
            chatgpt_section = f"""
🤖 **AI Summary:** {analysis_type_emoji} {analysis_type}
{recommendation_emoji} {chatgpt_confirmation.get('recommendation', 'N/A')} | {confidence_emoji} {chatgpt_confirmation.get('confidence', 0.5):.0%} | {risk_emoji} {chatgpt_confirmation.get('risk_assessment', 'MEDIUM')}{sentiment_section}
📋 Detailed analysis sent separately"""
        
        message = f"""
🇮🇩 **{signal_info['symbol']} Signal** 🇮🇩

{signal_emoji} **{signal_info['signal']}** {strength_emoji_icon} | {signal_info['signal_reason']}
💰 {signal_info['current_price']:,} IDR ({signal_info['price_change']:+.2f}%)
📊 Vol: {signal_info['volume_ratio']:.1f}x | RSI: {signal_info['rsi']:.0f} ({rsi_status.split()[1] if len(rsi_status.split()) > 1 else rsi_status})

📈 SMA: {signal_info['sma_short']:,} / {signal_info['sma_long']:,}
🎯 SL: {signal_info['stop_loss_price']:,} | TP: {signal_info['take_profit_price']:,}

✅ Valid: {'Yes' if signal_info['valid'] else 'No'} | 💪 {signal_info['strength']}{chatgpt_section}

⚠️ Educational purposes only. DYOR!
        """
        
        return message.strip()
    
    def format_detailed_ai_analysis(self, signal_info: Dict, chatgpt_confirmation: Dict) -> str:
        """Format detailed AI analysis as a separate comprehensive message"""
        
        # Recommendation emoji
        recommendation_emoji = {
            'CONFIRM': "✅",
            'REJECT': "❌",
            'MODIFY': "⚠️",
            'HOLD': "🟡",
            'PROCEED_WITH_CAUTION': "⚠️"
        }.get(chatgpt_confirmation.get('recommendation', 'UNKNOWN'), "❓")
        
        # Confidence color
        confidence = chatgpt_confirmation.get('confidence', 0.5)
        conf_emoji = "🟢" if confidence >= 0.8 else "🟡" if confidence >= 0.6 else "🔴"
        
        # Risk color
        risk_emoji = {
            'LOW': "🟢",
            'MEDIUM': "🟡", 
            'HIGH': "🔴",
            'UNKNOWN': "❓"
        }.get(chatgpt_confirmation.get('risk_assessment', 'MEDIUM'), "❓")
        
        # Analysis type information
        analysis_type_emoji = "👁️📊" if chatgpt_confirmation.get('vision_enabled', False) else "📊"
        analysis_type = chatgpt_confirmation.get('analysis_type', 'Statistical Only')
        
        # Start building the detailed message
        ai_message = f"""🤖 **COMPREHENSIVE AI ANALYSIS - {signal_info['symbol']}**
{analysis_type_emoji} **Analysis Type**: {analysis_type}

📊 **RECOMMENDATION SUMMARY**
{recommendation_emoji} **Recommendation**: {chatgpt_confirmation.get('recommendation', 'N/A')}
{conf_emoji} **Confidence**: {confidence:.1%}
{risk_emoji} **Risk Assessment**: {chatgpt_confirmation.get('risk_assessment', 'MEDIUM')}

💭 **COMPREHENSIVE ANALYSIS**
{chatgpt_confirmation.get('analysis', 'No detailed analysis available')}

🔑 **KEY FACTORS**"""
        
        # Add key factors
        key_factors = chatgpt_confirmation.get('key_factors', [])
        if key_factors:
            for i, factor in enumerate(key_factors, 1):
                ai_message += f"\n{i}. {factor}"
        else:
            ai_message += "\n• No specific key factors identified"
        
        # Add statistical analysis section if available
        if 'statistical_analysis' in chatgpt_confirmation:
            stats = chatgpt_confirmation['statistical_analysis']
            ai_message += f"""

📊 **STATISTICAL ANALYSIS BREAKDOWN**
🎯 **Technical Score**: {stats.get('technical_score', 0.5):.1%}
📈 **Volume Confirmation**: {stats.get('volume_confirmation', 'N/A')}
📊 **RSI Assessment**: {stats.get('rsi_assessment', 'N/A')}
📈 **SMA Trend**: {stats.get('sma_trend', 'N/A')}
🎯 **Signal Reliability**: {stats.get('signal_reliability', 'N/A')}"""
        
        # Add visual analysis section if available
        if chatgpt_confirmation.get('vision_enabled', False) and 'visual_analysis' in chatgpt_confirmation:
            visual = chatgpt_confirmation['visual_analysis']
            ai_message += f"""

👁️ **VISUAL CHART ANALYSIS**
📈 **Chart Pattern**: {visual.get('chart_pattern', 'No specific pattern identified')}
📊 **Trend Direction**: {visual.get('trend_direction', 'N/A')}
🎯 **Support/Resistance**: {visual.get('support_resistance', 'No clear levels identified')}
✅ **Visual Confirmation**: {visual.get('visual_confirmation', 'N/A')}
💪 **Chart Strength**: {visual.get('chart_strength', 'N/A')}"""
        
        # Add sentiment analysis if available
        if ENABLE_SENTIMENT_ANALYSIS and 'sentiment_analysis' in chatgpt_confirmation:
            sentiment = chatgpt_confirmation['sentiment_analysis']
            
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
            
            ai_message += f"""

📊 **COMPREHENSIVE SENTIMENT ANALYSIS**
{sentiment_emoji} **Overall Sentiment**: {sentiment.get('overall_sentiment', 'NEUTRAL')}
{score_emoji} **Sentiment Score**: {sentiment_score:.1%}

🏢 **Sector Analysis**
{sentiment.get('sector_sentiment', 'No sector analysis available')}

🌍 **Global Market Impact**
{sentiment.get('global_influence', 'No global impact analysis available')}

📰 **News & Events Impact**
{sentiment.get('news_impact', 'No news impact analysis available')}

🏛️ **Economic Factors**
{sentiment.get('economic_factors', 'No economic factors analysis available')}

📈 **Current Market Mood**
{sentiment.get('market_mood', 'No market mood analysis available')}

💭 **Sentiment Reasoning**
{sentiment.get('sentiment_reasoning', 'No sentiment reasoning available')}"""
        
        # Add additional notes if available
        additional_notes = chatgpt_confirmation.get('additional_notes', '')
        if additional_notes:
            ai_message += f"""

📝 **ADDITIONAL INSIGHTS**
{additional_notes}"""
        
        # Add enhanced trading recommendation if available
        if 'trading_recommendation' in chatgpt_confirmation:
            trading_rec = chatgpt_confirmation['trading_recommendation']
            ai_message += f"""

💼 **ENHANCED TRADING STRATEGY**
🎯 **Entry Strategy**: {trading_rec.get('entry_strategy', 'Follow standard signal guidelines')}
🚪 **Exit Strategy**: {trading_rec.get('exit_strategy', 'Use predefined stop loss and take profit levels')}
📏 **Position Sizing**: {trading_rec.get('position_sizing', 'Use appropriate risk management')}
⚠️ **Risk Management**: {trading_rec.get('risk_management', 'Standard risk management applies')}"""
        
        # Add trading recommendation based on signal
        ai_message += f"""

🎯 **TRADING RECOMMENDATION**"""
        
        if signal_info['signal'] == SIGNAL_BUY:
            ai_message += f"""
🟢 **BUY RECOMMENDATION**
• Entry Point: Around {signal_info['current_price']:,} IDR
• Stop Loss: {signal_info['stop_loss_price']:,} IDR (-5%)
• Take Profit: {signal_info['take_profit_price']:,} IDR (+10%)
• Risk/Reward Ratio: 1:2 (favorable)"""
        
        elif signal_info['signal'] == SIGNAL_SELL:
            ai_message += f"""
🔴 **SELL RECOMMENDATION**
• Current holders should consider taking profits
• Avoid new long positions at current levels
• Monitor for potential re-entry at lower levels
• Consider partial position reduction"""
        
        elif signal_info['signal'] == SIGNAL_STRONG_SELL:
            ai_message += f"""
🚨 **STRONG SELL RECOMMENDATION**
• Exit all positions immediately
• High probability of further decline
• Consider short positions if available
• Avoid any new long positions"""
        
        elif signal_info['signal'] == SIGNAL_HOLD:
            ai_message += f"""
🟡 **HOLD RECOMMENDATION**
• Maintain current positions if any
• No clear directional signal at this time
• Monitor for better entry/exit opportunities
• Consider dollar-cost averaging if long-term bullish"""
        
        ai_message += f"""

⚠️ **Risk Management Reminder**
Always use proper position sizing and never risk more than you can afford to lose. This analysis is for educational purposes only.
        """
        
        return ai_message.strip()
    
    def encode_chart_image(self, chart_buffer: BytesIO) -> str:
        """Convert chart image to base64 for ChatGPT Vision analysis"""
        try:
            chart_buffer.seek(0)
            image_data = chart_buffer.read()
            base64_image = base64.b64encode(image_data).decode('utf-8')
            chart_buffer.seek(0)  # Reset buffer position
            return base64_image
        except Exception as e:
            logger.error(f"Error encoding chart image: {e}")
            return ""
    
    async def get_chatgpt_confirmation(self, signal_info: Dict, chart_buffer: Optional[BytesIO] = None) -> Dict:
        """Get ChatGPT confirmation with advanced analysis and optional chart vision"""
        if not self.openai_client or not ENABLE_CHATGPT_CONFIRMATION:
            return {
                'confirmed': True,
                'confidence': 1.0,
                'analysis': 'ChatGPT confirmation disabled',
                'recommendation': 'Proceed with original signal'
            }
        
        try:
            # Prepare market data for analysis
            market_data = {
                'symbol': signal_info['symbol'],
                'signal': signal_info['signal'],
                'signal_reason': signal_info['signal_reason'],
                'current_price': signal_info['current_price'],
                'price_change': signal_info['price_change'],
                'volume_ratio': signal_info.get('volume_ratio', 1.0),
                'rsi': signal_info['rsi'],
                'sma_short': signal_info['sma_short'],
                'sma_long': signal_info['sma_long'],
                'strength': signal_info['strength'],
                'stop_loss_price': signal_info['stop_loss_price'],
                'take_profit_price': signal_info['take_profit_price'],
                'recent_high': signal_info.get('recent_high', signal_info['current_price']),
                'recent_low': signal_info.get('recent_low', signal_info['current_price'])
            }
            
            # Determine asset type and format accordingly
            symbol = signal_info['symbol']
            is_crypto = symbol.endswith('-USD') or symbol in ['BTC', 'ETH', 'ADA', 'DOT', 'MATIC', 'SOL', 'AVAX', 'LINK', 'UNI', 'AAVE', 'COMP', 'MKR', 'SNX', 'YFI', 'CRV', 'BAL', 'SUSHI', 'LTC', 'BCH', 'XRP', 'BNB', 'DOGE', 'SHIB', 'ATOM']
            
            # Dynamic asset analysis based on type
            if is_crypto:
                asset_type = "cryptocurrency"
                currency_symbol = "USD"
                market_context = "cryptocurrency market"
                price_format = f"${market_data['current_price']:,.2f}"
                sl_format = f"${market_data['stop_loss_price']:,.2f}"
                tp_format = f"${market_data['take_profit_price']:,.2f}"
                sma_short_format = f"${market_data['sma_short']:,.2f}"
                sma_long_format = f"${market_data['sma_long']:,.2f}"
                recent_high_format = f"${market_data['recent_high']:,.2f}"
                recent_low_format = f"${market_data['recent_low']:,.2f}"
                market_specialization = f"cryptocurrency market analysis with expertise in digital assets, DeFi, and blockchain technology"
                market_hours = "24/7 global cryptocurrency markets"
                sector_analysis = """
CRYPTOCURRENCY CONTEXT:
- BTC, ETH: Leading cryptocurrencies (Bitcoin, Ethereum)
- DeFi Tokens: UNI, AAVE, COMP, MKR, SNX, YFI, CRV, BAL, SUSHI
- Layer 1 Blockchains: DOT, ADA, SOL, AVAX, ATOM
- Smart Contract Platforms: ETH, BNB, MATIC, LINK
- Alternative Coins: LTC, BCH, XRP, DOGE, SHIB"""
                market_factors = f"""
🔗 CRYPTOCURRENCY MARKET CONTEXT:
11. Consider global cryptocurrency market conditions and sentiment
12. Evaluate DeFi sector trends and institutional adoption
13. Assess regulatory developments and policy impacts globally
14. Consider Bitcoin dominance and altcoin season patterns

🌍 SENTIMENT & MARKET ANALYSIS:
15. Analyze current market sentiment for cryptocurrencies
16. Evaluate institutional investment flows and adoption
17. Consider recent news and events affecting crypto markets
18. Assess macroeconomic factors impacting digital assets
19. Provide overall {market_context} mood assessment"""
            else:
                asset_type = "Indonesian stock"
                currency_symbol = "IDR"
                market_context = "Indonesian stock market"
                price_format = f"{market_data['current_price']:,} IDR"
                sl_format = f"{market_data['stop_loss_price']:,} IDR"
                tp_format = f"{market_data['take_profit_price']:,} IDR"
                sma_short_format = f"{market_data['sma_short']:,} IDR"
                sma_long_format = f"{market_data['sma_long']:,} IDR"
                recent_high_format = f"{market_data['recent_high']:,} IDR"
                recent_low_format = f"{market_data['recent_low']:,} IDR"
                market_specialization = f"Indonesian stock market analysis with advanced technical analysis and sentiment analysis capabilities"
                market_hours = "Indonesian market trading hours"
                sector_analysis = """
COMPANY-SPECIFIC CONTEXT:
- BBCA.JK, BBRI.JK, BMRI.JK: Indonesian banking sector leaders
- TLKM.JK: State-owned telecommunications giant
- ASII.JK: Automotive and heavy equipment conglomerate
- UNVR.JK: Consumer goods multinational
- ICBP.JK, INDF.JK: Food and beverage industry
- GGRM.JK: Tobacco industry leader
- KLBF.JK: Pharmaceutical sector"""
                market_factors = f"""
🇮🇩 INDONESIAN MARKET CONTEXT:
11. Consider Indonesian market characteristics and trading hours
12. Evaluate sector-specific factors (banking, telecom, consumer goods, etc.)
13. Assess impact of Indonesian economic and political factors
14. Consider Jakarta Stock Exchange (IDX) market conditions

🌍 SENTIMENT & MARKET ANALYSIS:
15. Analyze current market sentiment for Indonesian stocks
16. Evaluate global market impact on Indonesian equities
17. Consider recent news and events affecting the sector/stock
18. Assess economic indicators and policy impacts
19. Provide overall {market_context} mood assessment"""
            
            # Determine if we should use vision analysis
            use_vision = (ENABLE_CHATGPT_VISION and 
                         chart_buffer is not None and 
                         ENABLE_CHART_PATTERN_ANALYSIS)
            
            # Select appropriate model
            model_to_use = CHATGPT_VISION_MODEL if use_vision else CHATGPT_MODEL
            
            # Create comprehensive prompt for both statistical and visual analysis
            base_prompt = f"""
You are an expert financial analyst specializing in {market_specialization}.

STATISTICAL ANALYSIS DATA:
Symbol: {market_data['symbol']}
Signal: {market_data['signal']}
Signal Reason: {market_data['signal_reason']}
Current Price: {price_format}
Price Change: {market_data['price_change']:+.2f}%
Volume Ratio: {market_data['volume_ratio']:.2f}x (vs 20-day average)
RSI (14-day): {market_data['rsi']:.1f}
SMA Short (10-day): {sma_short_format}
SMA Long (20-day): {sma_long_format}
Signal Strength: {market_data['strength']}
Stop Loss Level: {sl_format} (-15%)
Take Profit Level: {tp_format} (+25%)
Recent High (10-day): {recent_high_format}
Recent Low (10-day): {recent_low_format}

COMPREHENSIVE ANALYSIS REQUIREMENTS:

📊 STATISTICAL ANALYSIS:
1. Evaluate all technical indicators (SMA crossover, RSI levels, volume patterns)
2. Assess signal quality and reliability based on numerical data
3. Calculate risk-reward ratio and position sizing recommendations
4. Validate signal strength against historical patterns

📈 VISUAL CHART ANALYSIS (if chart provided):
5. Analyze price action patterns and trends visually
6. Identify support and resistance levels from chart
7. Examine volume bars for confirmation signals
8. Look for chart patterns (triangles, flags, head & shoulders, etc.)
9. Validate technical indicators visually (SMA crossovers, RSI divergences)
10. Assess overall chart momentum and trend direction

{market_factors}

{sector_analysis}

ANALYSIS OUTPUT REQUIREMENTS:
- Provide confidence score (0.0-1.0) based on both statistical and visual evidence
- Give clear recommendation: CONFIRM, REJECT, MODIFY, or PROCEED_WITH_CAUTION
- Identify 3-5 key factors supporting your decision
- Include both technical and fundamental reasoning
- Assess risk level: LOW, MEDIUM, HIGH
- Provide actionable trading insights for {asset_type}"""

            # Add vision-specific instructions if chart is available
            if use_vision:
                vision_prompt = f"""

📸 CHART VISUAL ANALYSIS INSTRUCTIONS:
The attached chart shows:
- Top panel: Price action with SMA lines (orange=10-day, blue=20-day) and trading signals
- Middle panel: RSI indicator with overbought (70) and oversold (30) levels
- Bottom panel: Volume bars with high-volume alerts in red

Please analyze the chart visually and provide insights on:
1. Price trend direction and momentum
2. SMA crossover patterns and their validity
3. RSI levels and any divergences with price
4. Volume confirmation of price movements
5. Support and resistance levels visible on the chart
6. Any chart patterns or formations
7. Overall visual confirmation of the statistical signal

Combine your visual analysis with the statistical data to provide a comprehensive assessment."""
                
                base_prompt += vision_prompt
            
            # Add JSON response format
            json_format = f"""

Please respond in JSON format:
{{
    "confirmed": boolean,
    "confidence": float (0.0-1.0),
    "analysis": "comprehensive analysis combining statistical and visual insights",
    "recommendation": "CONFIRM/REJECT/MODIFY/PROCEED_WITH_CAUTION",
    "risk_assessment": "LOW/MEDIUM/HIGH",
    "key_factors": ["factor1", "factor2", "factor3", "factor4", "factor5"],
    "additional_notes": "trading insights and recommendations",
    "statistical_analysis": {{
        "technical_score": float (0.0-1.0),
        "volume_confirmation": "STRONG/MODERATE/WEAK",
        "rsi_assessment": "OVERBOUGHT/OVERSOLD/NEUTRAL",
        "sma_trend": "BULLISH/BEARISH/NEUTRAL",
        "signal_reliability": "HIGH/MEDIUM/LOW"
    }},
    "visual_analysis": {{
        "chart_pattern": "description of any patterns seen",
        "trend_direction": "UPTREND/DOWNTREND/SIDEWAYS",
        "support_resistance": "key levels identified",
        "visual_confirmation": "CONFIRMS/CONTRADICTS/NEUTRAL",
        "chart_strength": "STRONG/MODERATE/WEAK"
    }},
    "sentiment_analysis": {{
        "overall_sentiment": "VERY_POSITIVE/POSITIVE/NEUTRAL/NEGATIVE/VERY_NEGATIVE",
        "sentiment_score": float (0.0-1.0),
        "market_mood": "current {market_context} conditions description",
        "sector_sentiment": "sector-specific analysis",
        "news_impact": "recent news and events impact",
        "economic_factors": "{market_context} economic factors",
        "global_influence": "global market influence",
        "sentiment_reasoning": "detailed sentiment explanation"
    }},
    "trading_recommendation": {{
        "entry_strategy": "specific entry recommendations",
        "exit_strategy": "stop loss and take profit guidance",
        "position_sizing": "recommended position size",
        "risk_management": "specific risk management advice"
    }}
}}"""
            
            final_prompt = base_prompt + json_format
            
            # Prepare messages for API call
            messages = [
                {
                    "role": "system",
                    "content": f"You are an expert financial analyst specializing in {market_specialization}. Provide objective, data-driven analysis combining statistical data with visual chart analysis when available."
                }
            ]
            
            # Add user message with or without image
            if use_vision and chart_buffer:
                # Encode chart image for vision analysis
                base64_image = self.encode_chart_image(chart_buffer)
                if base64_image:
                    logger.info(f"Using ChatGPT Vision analysis for {signal_info['symbol']} with chart image")
                    messages.append({
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": final_prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}",
                                    "detail": CHART_IMAGE_QUALITY
                                }
                            }
                        ]
                    })
                else:
                    # Fallback to text-only if image encoding fails
                    logger.warning(f"Image encoding failed for {signal_info['symbol']}, using text-only analysis")
                    use_vision = False
                    model_to_use = CHATGPT_MODEL
                    messages.append({
                        "role": "user",
                        "content": final_prompt
                    })
            else:
                # Text-only analysis
                logger.info(f"Using text-only ChatGPT analysis for {signal_info['symbol']}")
                messages.append({
                    "role": "user",
                    "content": final_prompt
                })
            
            # Make API call to ChatGPT
            for attempt in range(CHATGPT_MAX_RETRIES):
                try:
                    analysis_type = "Vision + Statistical" if use_vision else "Statistical Only"
                    logger.info(f"Requesting ChatGPT {analysis_type} confirmation for {signal_info['symbol']} (attempt {attempt + 1})")
                    
                    response = await self.openai_client.chat.completions.create(
                        model=model_to_use,
                        messages=messages,
                        temperature=0.3,  # Lower temperature for more consistent analysis
                        max_tokens=2000  # Increased for comprehensive analysis
                    )
                    
                    # Parse ChatGPT response
                    chatgpt_response = response.choices[0].message.content.strip()
                    
                    # Try to parse JSON response
                    try:
                        # Extract JSON from response if it's wrapped in markdown
                        if "```json" in chatgpt_response:
                            json_start = chatgpt_response.find("```json") + 7
                            json_end = chatgpt_response.find("```", json_start)
                            chatgpt_response = chatgpt_response[json_start:json_end].strip()
                        elif "```" in chatgpt_response:
                            json_start = chatgpt_response.find("```") + 3
                            json_end = chatgpt_response.rfind("```")
                            chatgpt_response = chatgpt_response[json_start:json_end].strip()
                        
                        analysis_result = json.loads(chatgpt_response)
                        
                        # Validate required fields
                        required_fields = ['confirmed', 'confidence', 'analysis', 'recommendation']
                        if all(field in analysis_result for field in required_fields):
                            # Enhanced logging with analysis type
                            analysis_type = "Vision + Statistical" if use_vision else "Statistical Only"
                            visual_conf = ""
                            if use_vision and 'visual_analysis' in analysis_result:
                                visual_conf = f" | Visual: {analysis_result['visual_analysis'].get('visual_confirmation', 'N/A')}"
                            
                            logger.info(f"ChatGPT {analysis_type} analysis complete for {signal_info['symbol']}: "
                                      f"{analysis_result['recommendation']} (confidence: {analysis_result['confidence']:.2f}){visual_conf}")
                            
                            # Add analysis metadata
                            analysis_result['analysis_type'] = analysis_type
                            analysis_result['vision_enabled'] = use_vision
                            
                            return analysis_result
                        else:
                            logger.warning(f"ChatGPT response missing required fields: {chatgpt_response}")
                            
                    except json.JSONDecodeError as e:
                        logger.warning(f"Failed to parse ChatGPT JSON response: {e}")
                        logger.warning(f"Raw response: {chatgpt_response}")
                        
                        # Fallback: create basic analysis from text response
                        return {
                            'confirmed': True,
                            'confidence': 0.5,
                            'analysis': chatgpt_response,
                            'recommendation': 'CONFIRM',
                            'risk_assessment': 'MEDIUM',
                            'key_factors': ['Technical analysis'],
                            'additional_notes': 'JSON parsing failed, using text response',
                            'analysis_type': 'Fallback Text',
                            'vision_enabled': False
                        }
                    
                except Exception as api_error:
                    logger.warning(f"ChatGPT API error (attempt {attempt + 1}): {api_error}")
                    if attempt < CHATGPT_MAX_RETRIES - 1:
                        await asyncio.sleep(2 ** attempt)  # Exponential backoff
                        continue
                    else:
                        raise api_error
            
        except Exception as e:
            logger.error(f"ChatGPT confirmation failed for {signal_info['symbol']}: {e}")
            return {
                'confirmed': True,
                'confidence': 0.5,
                'analysis': f'ChatGPT analysis failed: {str(e)}',
                'recommendation': 'PROCEED_WITH_CAUTION',
                'risk_assessment': 'UNKNOWN',
                'key_factors': ['Technical analysis only'],
                'additional_notes': 'ChatGPT confirmation unavailable',
                'analysis_type': 'Error Fallback',
                'vision_enabled': False
            }
    
    async def send_telegram_message(self, message: str, chart: Optional[BytesIO] = None):
        """Send message to Telegram"""
        try:
            if chart:
                await self.telegram_bot.send_photo(
                    chat_id=self.chat_id,
                    photo=chart,
                    caption=message,
                    parse_mode='Markdown'
                )
            else:
                await self.telegram_bot.send_message(
                    chat_id=self.chat_id,
                    text=message,
                    parse_mode='Markdown'
                )
            
            logger.info("Message sent to Telegram successfully")
            
        except TelegramError as e:
            logger.error(f"Error sending Telegram message: {e}")
        except Exception as e:
            logger.error(f"Unexpected error sending message: {e}")
    
    def is_watchlist_stock(self, symbol: str) -> bool:
        """Check if a stock is in the watchlist"""
        return ENABLE_WATCHLIST and symbol in WATCHLIST_STOCKS
    
    def update_watchlist_data(self, symbol: str, signal_info: Dict):
        """Update watchlist data for tracking"""
        if not self.is_watchlist_stock(symbol):
            return
        
        current_time = datetime.now()
        
        # Initialize watchlist data for symbol if not exists
        if symbol not in self.watchlist_data:
            self.watchlist_data[symbol] = {
                'last_price': signal_info['current_price'],
                'last_update': current_time,
                'price_alerts': [],
                'volume_alerts': [],
                'signal_history': []
            }
        
        watchlist_entry = self.watchlist_data[symbol]
        last_price = watchlist_entry['last_price']
        current_price = signal_info['current_price']
        
        # Check for significant price movements
        price_change_pct = abs((current_price - last_price) / last_price * 100)
        if price_change_pct >= WATCHLIST_PRICE_ALERT_PERCENTAGE:
            alert = {
                'type': 'PRICE_MOVE',
                'symbol': symbol,
                'old_price': last_price,
                'new_price': current_price,
                'change_pct': (current_price - last_price) / last_price * 100,
                'timestamp': current_time
            }
            watchlist_entry['price_alerts'].append(alert)
            self.watchlist_alerts.append(alert)
            logger.info(f"Watchlist price alert for {symbol}: {alert['change_pct']:+.2f}%")
        
        # Check for high volume alerts
        if ENABLE_WATCHLIST_VOLUME_ALERTS and signal_info.get('volume_ratio', 1) > HIGH_VOLUME_SELL_MULTIPLIER:
            alert = {
                'type': 'HIGH_VOLUME',
                'symbol': symbol,
                'volume_ratio': signal_info['volume_ratio'],
                'volume': signal_info['volume'],
                'timestamp': current_time
            }
            watchlist_entry['volume_alerts'].append(alert)
            self.watchlist_alerts.append(alert)
            logger.info(f"Watchlist volume alert for {symbol}: {signal_info['volume_ratio']:.2f}x normal")
        
        # Update watchlist data
        watchlist_entry['last_price'] = current_price
        watchlist_entry['last_update'] = current_time
        watchlist_entry['signal_history'].append({
            'signal': signal_info['signal'],
            'price': current_price,
            'timestamp': current_time
        })
        
        # Keep only last 10 alerts and signals
        watchlist_entry['price_alerts'] = watchlist_entry['price_alerts'][-10:]
        watchlist_entry['volume_alerts'] = watchlist_entry['volume_alerts'][-10:]
        watchlist_entry['signal_history'] = watchlist_entry['signal_history'][-10:]
    
    async def send_watchlist_alerts(self):
        """Send accumulated watchlist alerts"""
        if not ENABLE_WATCHLIST or not self.watchlist_alerts:
            return
        
        # Group alerts by type
        price_alerts = [a for a in self.watchlist_alerts if a['type'] == 'PRICE_MOVE']
        volume_alerts = [a for a in self.watchlist_alerts if a['type'] == 'HIGH_VOLUME']
        
        if not price_alerts and not volume_alerts:
            return
        
        alert_message = "🔔 **WATCHLIST ALERTS** 🔔\n\n"
        
        # Price movement alerts
        if price_alerts:
            alert_message += "📈 **PRICE MOVEMENTS:**\n"
            for alert in price_alerts[-5:]:  # Show last 5 alerts
                direction = "📈" if alert['change_pct'] > 0 else "📉"
                alert_message += f"{direction} {alert['symbol']}: {alert['change_pct']:+.2f}% → {alert['new_price']:,} IDR\n"
            alert_message += "\n"
        
        # Volume alerts
        if volume_alerts:
            alert_message += "📊 **HIGH VOLUME ALERTS:**\n"
            for alert in volume_alerts[-5:]:  # Show last 5 alerts
                alert_message += f"🔴 {alert['symbol']}: {alert['volume_ratio']:.1f}x normal volume\n"
            alert_message += "\n"
        
        alert_message += "⚠️ Monitor these watchlist stocks closely!"
        
        await self.send_telegram_message(alert_message)
        
        # Clear sent alerts
        self.watchlist_alerts.clear()
        logger.info(f"Sent watchlist alerts: {len(price_alerts)} price, {len(volume_alerts)} volume")
    
    async def generate_watchlist_summary(self) -> str:
        """Generate daily watchlist summary"""
        if not ENABLE_WATCHLIST or not ENABLE_WATCHLIST_DAILY_SUMMARY:
            return ""
        
        summary = "📋 **DAILY WATCHLIST SUMMARY** 📋\n\n"
        
        for symbol in WATCHLIST_STOCKS:
            if symbol in self.watchlist_data:
                data = self.watchlist_data[symbol]
                last_signal = data['signal_history'][-1] if data['signal_history'] else None
                
                # Signal emoji
                signal_emoji = {
                    SIGNAL_BUY: "🟢",
                    SIGNAL_SELL: "🔴", 
                    SIGNAL_STRONG_SELL: "🚨",
                    SIGNAL_HOLD: "🟡"
                }.get(last_signal['signal'] if last_signal else SIGNAL_HOLD, "⚪")
                
                summary += f"{signal_emoji} **{symbol}**\n"
                summary += f"💰 Price: {data['last_price']:,} IDR\n"
                
                if last_signal:
                    summary += f"📊 Last Signal: {last_signal['signal']}\n"
                
                # Recent alerts count
                recent_price_alerts = len([a for a in data['price_alerts'] if (datetime.now() - a['timestamp']).days == 0])
                recent_volume_alerts = len([a for a in data['volume_alerts'] if (datetime.now() - a['timestamp']).days == 0])
                
                if recent_price_alerts > 0:
                    summary += f"📈 Price Alerts Today: {recent_price_alerts}\n"
                if recent_volume_alerts > 0:
                    summary += f"📊 Volume Alerts Today: {recent_volume_alerts}\n"
                
                summary += "\n"
            else:
                summary += f"⚪ **{symbol}**: No data available\n\n"
        
        return summary
    
    async def analyze_stock(self, symbol: str) -> Optional[Dict]:
        """Analyze a single stock and return enhanced signal info"""
        logger.info(f"Analyzing {symbol}...")
        
        # Fetch data
        data = self.fetch_stock_data(symbol)
        if data is None or len(data) < max(SMA_LONG_PERIOD, RSI_PERIOD):
            logger.warning(f"Insufficient data for {symbol}")
            return None
        
        # Generate enhanced signals
        data_with_signals = self.generate_enhanced_signals(data)
        
        # Validate latest signal
        signal_info = self.validate_signal(data_with_signals, symbol)
        
        # Send ALL signals including HOLD to Telegram
        if signal_info['signal'] in [SIGNAL_BUY, SIGNAL_SELL, SIGNAL_STRONG_SELL, SIGNAL_HOLD] and signal_info['valid']:
            
            # Create enhanced chart first (needed for both Telegram and ChatGPT)
            chart = self.create_enhanced_chart(data_with_signals, symbol, signal_info)
            
            # Get ChatGPT confirmation with chart for vision analysis
            confirmation = await self.get_chatgpt_confirmation(signal_info, chart)
            
            # Check if ChatGPT confirms the signal
            should_send_signal = True
            confidence_threshold = CHATGPT_CONFIDENCE_THRESHOLD
            
            # Special handling for HOLD signals
            if signal_info['signal'] == SIGNAL_HOLD:
                if not ENABLE_HOLD_SIGNALS:
                    should_send_signal = False
                    logger.info(f"HOLD signals disabled for {symbol}")
                elif SEND_HOLD_SIGNALS_REGARDLESS_OF_CONFIDENCE:
                    confidence_threshold = 0.0  # Always send HOLD signals
                    logger.info(f"HOLD signal for {symbol}: Bypassing confidence check")
                else:
                    confidence_threshold = HOLD_SIGNAL_CONFIDENCE_THRESHOLD
                    logger.info(f"HOLD signal for {symbol}: Using lower threshold {confidence_threshold}")
            
            # Lower threshold for watchlist stocks
            elif self.is_watchlist_stock(symbol):
                confidence_threshold = WATCHLIST_ALERT_THRESHOLD
                # Boost confidence for watchlist stocks
                if 'confidence' in confirmation:
                    confirmation['confidence'] = min(1.0, confirmation['confidence'] * WATCHLIST_PRIORITY_MULTIPLIER)
                logger.info(f"Watchlist stock {symbol}: Using lower threshold {confidence_threshold} and boosted confidence")
            
            if ENABLE_CHATGPT_CONFIRMATION and self.openai_client:
                # Only send if ChatGPT confirms and confidence is above threshold
                if confirmation.get('recommendation') == 'REJECT':
                    should_send_signal = False
                    logger.info(f"ChatGPT rejected signal for {symbol}: {confirmation.get('analysis', 'No reason provided')}")
                elif confirmation.get('confidence', 0) < confidence_threshold:
                    should_send_signal = False
                    logger.info(f"ChatGPT confidence too low for {symbol}: {confirmation.get('confidence', 0):.2f} < {confidence_threshold}")
            
            if should_send_signal:
                # Format message with ChatGPT confirmation
                message = self.format_enhanced_signal_message(signal_info, confirmation)
                
                # Send to Telegram
                await self.send_telegram_message(message, chart)
                
                # Send separate detailed AI analysis message
                if ENABLE_CHATGPT_CONFIRMATION and self.openai_client and confirmation:
                    ai_message = self.format_detailed_ai_analysis(signal_info, confirmation)
                    await self.send_telegram_message(ai_message)
                
                # Store in history with ChatGPT confirmation
                signal_info['chatgpt_confirmation'] = confirmation
                self.signals_history.append(signal_info)
                
                logger.info(f"Signal sent for {symbol}: {signal_info['signal']} - {signal_info['signal_reason']} (ChatGPT: {confirmation.get('recommendation', 'N/A')})")
            else:
                logger.info(f"Signal filtered out for {symbol} by ChatGPT confirmation")
                # Still return signal_info but mark it as filtered
                signal_info['chatgpt_filtered'] = True
                signal_info['chatgpt_confirmation'] = confirmation
            
            # Update watchlist data
            self.update_watchlist_data(symbol, signal_info)
            
        return signal_info
    
    async def run_daily_analysis(self):
        """Run daily analysis for all Indonesian stocks"""
        logger.info("Starting daily EOD analysis with enhanced sell signals...")
        
        start_time = datetime.now()
        signals_sent = 0
        buy_signals = 0
        sell_signals = 0
        strong_sell_signals = 0
        hold_signals = 0
        chatgpt_filtered = 0
        chatgpt_confirmed = 0
        
        # Send start message
        chatgpt_status = "🤖 ChatGPT Confirmation: ENABLED" if (ENABLE_CHATGPT_CONFIRMATION and self.openai_client) else "🤖 ChatGPT Confirmation: DISABLED"
        vision_status = " + 👁️ Vision Analysis" if (ENABLE_CHATGPT_VISION and ENABLE_CHART_PATTERN_ANALYSIS) else ""
        watchlist_status = f"📋 Watchlist: {len(WATCHLIST_STOCKS)} stocks" if ENABLE_WATCHLIST else "📋 Watchlist: DISABLED"
        
        start_message = f"""
🤖 **Indonesian Stock Bot - Enhanced Daily Analysis**
📅 {start_time.strftime('%Y-%m-%d %H:%M:%S')}

🔍 Analyzing {len(INDONESIAN_STOCKS)} Indonesian stocks...
📊 Strategy: Enhanced SMA + RSI + Volume Analysis
🎯 Includes: Buy, Sell & Strong Sell signals
{chatgpt_status}{vision_status}
{watchlist_status}
        """
        
        await self.send_telegram_message(start_message)
        
        # Analyze each stock
        for i, symbol in enumerate(INDONESIAN_STOCKS):
            try:
                logger.info(f"Analyzing {symbol} ({i+1}/{len(INDONESIAN_STOCKS)})")
                signal_info = await self.analyze_stock(symbol)
                
                if signal_info and signal_info['signal'] in [SIGNAL_BUY, SIGNAL_SELL, SIGNAL_STRONG_SELL, SIGNAL_HOLD]:
                    # Check if signal was sent or filtered by ChatGPT
                    if signal_info.get('chatgpt_filtered', False):
                        chatgpt_filtered += 1
                    else:
                        signals_sent += 1
                        chatgpt_confirmed += 1
                        if signal_info['signal'] == SIGNAL_BUY:
                            buy_signals += 1
                        elif signal_info['signal'] == SIGNAL_SELL:
                            sell_signals += 1
                        elif signal_info['signal'] == SIGNAL_STRONG_SELL:
                            strong_sell_signals += 1
                        elif signal_info['signal'] == SIGNAL_HOLD:
                            hold_signals += 1
                
                # Longer delay to avoid rate limiting (3-5 seconds)
                delay = 3 + (i * 0.5)  # Increasing delay for each stock
                logger.info(f"Waiting {delay:.1f}s before next analysis...")
                await asyncio.sleep(delay)
                
            except Exception as e:
                logger.error(f"Error analyzing {symbol}: {e}")
                # Still wait even on error to avoid rapid requests
                await asyncio.sleep(2)
        
        # Send summary message
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # ChatGPT summary section
        chatgpt_summary = ""
        if ENABLE_CHATGPT_CONFIRMATION and self.openai_client:
            total_signals_generated = signals_sent + chatgpt_filtered
            chatgpt_summary = f"""
🤖 **ChatGPT Analysis:**
✅ Signals Confirmed: {chatgpt_confirmed}
❌ Signals Filtered: {chatgpt_filtered}
📊 Total Generated: {total_signals_generated}
🎯 Approval Rate: {(chatgpt_confirmed / max(total_signals_generated, 1)) * 100:.1f}%
"""
        
        summary_message = f"""
✅ **Daily Analysis Complete**

📊 Stocks Analyzed: {len(INDONESIAN_STOCKS)}
🚨 Signals Sent: {signals_sent}
🟢 Buy Signals: {buy_signals}
🔴 Sell Signals: {sell_signals}
🚨 Strong Sell Signals: {strong_sell_signals}
🟡 Hold Signals: {hold_signals}{chatgpt_summary}
⏱️ Duration: {duration:.1f} seconds

Next analysis: Tomorrow at market close
        """
        
        await self.send_telegram_message(summary_message)
        logger.info(f"Daily analysis complete. {signals_sent} signals sent (Buy: {buy_signals}, Sell: {sell_signals}, Strong Sell: {strong_sell_signals}). ChatGPT filtered: {chatgpt_filtered}")
        
        # Send watchlist alerts if any
        await self.send_watchlist_alerts()
        
        # Send watchlist summary
        if ENABLE_WATCHLIST and ENABLE_WATCHLIST_DAILY_SUMMARY:
            watchlist_summary = await self.generate_watchlist_summary()
            if watchlist_summary:
                await self.send_telegram_message(watchlist_summary)
    
    def run_bot(self):
        """Run the bot with scheduled daily analysis"""
        logger.info("Starting Enhanced Indonesian Stock Trading Bot...")
        
        # Schedule daily analysis at 5 PM Jakarta time (after market close)
        schedule.every().day.at("17:00").do(lambda: asyncio.run(self.run_daily_analysis()))
        
        # Also allow manual trigger for testing
        logger.info("Bot scheduled to run daily at 17:00 Jakarta time")
        logger.info("Press Ctrl+C to stop the bot")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")


async def main():
    """Main function for testing"""
    try:
        bot = IndonesianStockBot()
        
        # Run immediate analysis for testing
        await bot.run_daily_analysis()
        
    except Exception as e:
        logger.error(f"Error in main: {e}")


if __name__ == "__main__":
    # For testing, run immediate analysis
    # For production, use bot.run_bot() for scheduled execution
    asyncio.run(main()) 