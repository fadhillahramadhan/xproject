"""
Configuration file for Indonesian Stock Trading Bot
"""

# Indonesian Stock Symbols (Jakarta Stock Exchange)
INDONESIAN_STOCKS = [
    'BBCA.JK',  # Bank Central Asia
    'BBRI.JK',  # Bank Rakyat Indonesia
    'BMRI.JK',  # Bank Mandiri
    'TLKM.JK',  # Telkom Indonesia
    'ASII.JK',  # Astra International
    'UNVR.JK',  # Unilever Indonesia
    'ICBP.JK',  # Indofood CBP
    'GGRM.JK',  # Gudang Garam
    'INDF.JK',  # Indofood Sukses Makmur
    'KLBF.JK',  # Kalbe Farma
]

# Technical Analysis Parameters
SMA_SHORT_PERIOD = 20  # Short-term Simple Moving Average (increased from 10)
SMA_LONG_PERIOD = 50   # Long-term Simple Moving Average (increased from 20)
DATA_PERIOD = "1y"     # Data period to fetch (6 months for better long-term analysis)

# Trading Signal Thresholds
MIN_VOLUME_THRESHOLD = 1000000  # Minimum volume for signal validity
MIN_PRICE_CHANGE = 0.03  # Minimum 3% price change for strong signal (increased from 2%)

# Sell Signal Parameters - LONG TERM FOCUSED
STOP_LOSS_PERCENTAGE = 0.15  # 15% stop loss (increased from 5% for long-term)
TAKE_PROFIT_PERCENTAGE = 0.25  # 25% take profit (increased from 10% for long-term)
RSI_OVERBOUGHT_THRESHOLD = 80  # RSI above 80 for sell signal (increased from 70)
RSI_OVERSOLD_THRESHOLD = 20   # RSI below 20 for buy signal (decreased from 30)
RSI_PERIOD = 21  # RSI calculation period (increased from 14 for smoother signals)

# Price Action Sell Signals - LONG TERM FOCUSED
BEARISH_DIVERGENCE_THRESHOLD = 0.05  # 5% divergence for bearish signal (increased from 3%)
HIGH_VOLUME_SELL_MULTIPLIER = 3.0  # Volume 3x average for strong sell signal (increased from 2x)

# Telegram Settings (will be loaded from .env file)
TELEGRAM_BOT_TOKEN = None
TELEGRAM_CHAT_ID = None

# OpenAI Settings (will be loaded from .env file)
OPENAI_API_KEY = None

# ChatGPT Confirmation Settings
ENABLE_CHATGPT_CONFIRMATION = True  # Set to False to disable ChatGPT confirmation
CHATGPT_MODEL = "gpt-4o-mini"  # More cost-effective model
CHATGPT_CONFIDENCE_THRESHOLD = 0.7  # Minimum confidence score (0.0-1.0)
CHATGPT_MAX_RETRIES = 2  # Maximum retries for API calls
ENABLE_SENTIMENT_ANALYSIS = True  # Enable sentiment analysis in ChatGPT confirmation
SENTIMENT_WEIGHT = 0.3  # How much sentiment affects final confidence (0.0-1.0)

# ChatGPT Vision Analysis Settings
ENABLE_CHATGPT_VISION = True  # Enable image analysis with ChatGPT Vision
CHATGPT_VISION_MODEL = "gpt-4o"  # Vision-capable model (required for image analysis)
ENABLE_CHART_PATTERN_ANALYSIS = True  # Analyze chart patterns and visual indicators
ENABLE_TECHNICAL_INDICATOR_VALIDATION = True  # Validate technical indicators visually
CHART_IMAGE_QUALITY = "high"  # Image quality for analysis: "low", "medium", "high"

# Market Hours (Jakarta time - UTC+7)
MARKET_OPEN_HOUR = 9
MARKET_CLOSE_HOUR = 16

# Signal Types
SIGNAL_BUY = "BUY"
SIGNAL_SELL = "SELL"
SIGNAL_STRONG_SELL = "STRONG_SELL"
SIGNAL_HOLD = "HOLD"

# Watchlist Configuration
ENABLE_WATCHLIST = True  # Enable watchlist functionality
WATCHLIST_STOCKS = [
    # High Priority Stocks (always monitored)
    'BBCA.JK',  # Bank Central Asia
    'BBRI.JK',  # Bank Rakyat Indonesia
    'BMRI.JK',  # Bank Mandiri
    'TLKM.JK',  # Telkom Indonesia
    'AADI.JK',  # ADI
]

# Watchlist Alert Settings
WATCHLIST_ALERT_THRESHOLD = 0.5  # Lower confidence threshold for watchlist stocks
WATCHLIST_PRIORITY_MULTIPLIER = 1.2  # Boost confidence for watchlist stocks
ENABLE_WATCHLIST_DAILY_SUMMARY = True  # Send daily watchlist summary
WATCHLIST_PRICE_ALERT_PERCENTAGE = 5.0  # Alert on 5%+ price moves
ENABLE_WATCHLIST_VOLUME_ALERTS = True  # Alert on high volume for watchlist stocks

# HOLD Signal Configuration
ENABLE_HOLD_SIGNALS = True  # Send HOLD signals to Telegram
HOLD_SIGNAL_CONFIDENCE_THRESHOLD = 0.3  # Lower threshold for HOLD signals (30%)
SEND_HOLD_SIGNALS_REGARDLESS_OF_CONFIDENCE = True  # Send HOLD signals even if ChatGPT confidence is low 