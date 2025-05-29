# Indonesian Stock Trading Bot 🇮🇩

A comprehensive End-of-Day (EOD) trading signal bot for Indonesian stocks using enhanced SMA crossover strategy with **comprehensive SELL signal detection**. The bot analyzes Jakarta Stock Exchange (JSX) stocks and sends trading signals via Telegram with beautiful charts and detailed sell recommendations.

## Features ✨

-   **📊 Enhanced Technical Analysis**: SMA crossover + RSI + Volume analysis
-   **🇮🇩 Indonesian Stocks**: Pre-configured with top Indonesian stocks (BBCA.JK, BBRI.JK, etc.)
-   **📱 Telegram Integration**: Sends signals with charts directly to your Telegram
-   **📈 Beautiful Charts**: Dark-themed charts with price, SMA, RSI, and signal markers
-   **🚨 Comprehensive Sell Signals**: Regular sell + Strong sell signals with multiple triggers
-   **🤖 ChatGPT Confirmation**: AI-powered signal validation and risk assessment
-   **🎯 Trading Levels**: Automatic stop-loss and take-profit calculations
-   **⏰ Scheduled Analysis**: Automatic daily analysis after market close
-   **🔍 Signal Validation**: Volume and price change validation for signal quality
-   **📝 Comprehensive Logging**: Detailed logs for monitoring and debugging

## Indonesian Stocks Covered 🏦

-   **BBCA.JK** - Bank Central Asia
-   **BBRI.JK** - Bank Rakyat Indonesia
-   **BMRI.JK** - Bank Mandiri
-   **TLKM.JK** - Telkom Indonesia
-   **ASII.JK** - Astra International
-   **UNVR.JK** - Unilever Indonesia
-   **ICBP.JK** - Indofood CBP
-   **GGRM.JK** - Gudang Garam
-   **INDF.JK** - Indofood Sukses Makmur
-   **KLBF.JK** - Kalbe Farma

## Enhanced Strategy Details 📊

### 🟢 BUY SIGNALS

1. **SMA Crossover + RSI Confirmation**: Short SMA crosses above Long SMA + RSI < 70
2. **RSI Oversold Recovery**: RSI recovers from oversold (< 30) while trend is bullish

### 🔴 SELL SIGNALS

1. **SMA Bearish Crossover**: Short SMA crosses below Long SMA
2. **RSI Overbought**: RSI > 70 (overbought territory)
3. **High Volume Sell-off**: Volume > 2x average + Price drop > 2%
4. **Bearish Divergence**: Price trending up but RSI trending down

### 🚨 STRONG SELL SIGNALS

1. **Multiple Bearish Indicators**: SMA crossover + RSI overbought simultaneously
2. **Extreme Overbought**: RSI > 80 + High volume
3. **Price Crash**: Price drop > 5% + High volume

### 🎯 Trading Levels

-   **Stop Loss**: Automatic 5% below entry price
-   **Take Profit**: Automatic 10% above entry price
-   **Recent High/Low**: 10-day rolling high and low levels

### 📊 Technical Indicators

-   **Short SMA**: 10-day Simple Moving Average
-   **Long SMA**: 20-day Simple Moving Average
-   **RSI**: 14-day Relative Strength Index
-   **Volume Analysis**: 20-day volume moving average comparison

## 🤖 Enhanced ChatGPT Analysis System

The bot now includes an advanced ChatGPT-powered confirmation system with **Vision Analysis** capabilities that analyzes both statistical data and chart images before sending signals to Telegram.

### 🔄 How It Works

1. **📊 Statistical Analysis**: Bot generates signals using SMA, RSI, and volume indicators
2. **📈 Chart Creation**: Enhanced chart with technical indicators and visual signals
3. **👁️ Vision Analysis**: ChatGPT analyzes the chart image for visual patterns
4. **🤖 AI Review**: Combined statistical and visual analysis by ChatGPT
5. **⚖️ Risk Assessment**: Comprehensive evaluation of market conditions
6. **🎯 Confidence Scoring**: Signals receive confidence scores (0-100%)
7. **🔍 Filtering**: Only high-confidence signals are sent to Telegram

### 🆕 Enhanced Analysis Features

#### 👁️ **Vision Analysis (NEW!)**

-   **Chart Pattern Recognition**: Identifies triangles, flags, head & shoulders, etc.
-   **Visual Trend Confirmation**: Validates statistical signals with visual evidence
-   **Support/Resistance Levels**: AI identifies key price levels from chart
-   **Volume Bar Analysis**: Visual confirmation of volume patterns
-   **Technical Indicator Validation**: Cross-checks SMA crossovers and RSI visually

#### 📊 **Statistical Analysis**

-   **Technical Score**: Numerical assessment of signal quality (0-100%)
-   **Volume Confirmation**: STRONG/MODERATE/WEAK volume validation
-   **RSI Assessment**: OVERBOUGHT/OVERSOLD/NEUTRAL classification
-   **SMA Trend**: BULLISH/BEARISH/NEUTRAL trend direction
-   **Signal Reliability**: HIGH/MEDIUM/LOW reliability rating

### 🔍 Comprehensive Analysis Components

#### 📊 **Core Technical Analysis**

-   **📈 Technical Indicator Validation**: Confirms SMA crossovers, RSI levels, volume patterns
-   **🇮🇩 Indonesian Market Context**: Considers local market conditions and characteristics
-   **⚖️ Risk-Reward Assessment**: Evaluates potential profit vs. risk
-   **🎯 Confidence Scoring**: Provides numerical confidence (0.0-1.0)
-   **📝 Detailed Analysis**: Written explanation combining statistical and visual insights

#### 👁️ **Visual Chart Analysis**

-   **📈 Chart Pattern Detection**: Identifies classic patterns (triangles, flags, channels)
-   **📊 Trend Direction Analysis**: Visual confirmation of uptrend/downtrend/sideways
-   **🎯 Support/Resistance Identification**: Key price levels from chart analysis
-   **📊 Volume Pattern Validation**: Visual confirmation of volume spikes and patterns
-   **✅ Signal Confirmation**: Visual validation of statistical signals

#### 🧠 **Advanced Intelligence Features**

-   **🔑 Key Factors**: Highlights 3-5 most important decision factors
-   **⚠️ Risk Classification**: LOW/MEDIUM/HIGH risk assessment
-   **💼 Trading Strategy**: Specific entry/exit recommendations and position sizing
-   **📊 Sentiment Analysis**: Comprehensive market sentiment evaluation
-   **🏢 Sector Analysis**: Industry-specific sentiment and trends
-   **🌍 Global Impact**: International market influence assessment
-   **📰 News Impact**: Recent events and news sentiment analysis
-   **🏛️ Economic Factors**: Indonesian economic conditions evaluation

### 🎯 Enhanced Signal Filtering Logic

#### 🤖 **AI Recommendation Types**

-   **✅ CONFIRM**: Signal sent to Telegram with full AI endorsement
-   **❌ REJECT**: Signal blocked due to poor quality or high risk
-   **⚠️ MODIFY**: Signal sent with additional warnings and context
-   **🚨 PROCEED_WITH_CAUTION**: Signal sent with enhanced risk warnings

#### 📊 **Multi-Layer Confidence System**

-   **🎯 Statistical Confidence**: Based on technical indicators (0-100%)
-   **👁️ Visual Confidence**: Based on chart pattern analysis (0-100%)
-   **🧠 Combined Confidence**: Weighted combination of both analyses
-   **🔍 Confidence Threshold**: Only signals above 70% combined confidence are sent (configurable)

#### 👁️ **Vision Analysis Integration**

-   **📈 Visual Confirmation**: Chart patterns must support statistical signals
-   **🎯 Pattern Strength**: Strong visual patterns boost confidence scores
-   **⚠️ Visual Contradictions**: Charts contradicting statistics trigger warnings
-   **📊 Trend Validation**: Visual trend direction must align with signal direction

### 🚀 Enhanced Benefits

#### 🛡️ **Superior Signal Quality**

-   **🔍 Dual Validation**: Both statistical and visual confirmation required
-   **📈 Higher Success Rate**: Multi-layer analysis improves signal accuracy
-   **🚫 False Signal Reduction**: AI eliminates contradictory or weak signals
-   **⚡ Real-time Analysis**: Instant combined statistical and visual review

#### 🧠 **Professional-Grade Analysis**

-   **👁️ Chart Reading**: AI "sees" patterns like professional traders
-   **📊 Comprehensive Reports**: Detailed statistical and visual breakdowns
-   **🎯 Actionable Insights**: Specific entry/exit strategies and risk management
-   **📈 Market Context**: Indonesian market-specific analysis and sentiment

#### 📊 **Advanced Monitoring**

-   **🔍 Analysis Type Tracking**: Monitor vision vs. text-only analysis performance
-   **📈 Confidence Metrics**: Track statistical vs. visual confidence scores
-   **🎯 Pattern Recognition**: Monitor which chart patterns perform best
-   **⚡ Performance Analytics**: Comprehensive success rate tracking

### 📊 Advanced Sentiment Analysis

The ChatGPT confirmation system now includes comprehensive sentiment analysis that evaluates:

#### Market Sentiment Factors

-   **🚀 Overall Market Sentiment**: VERY_POSITIVE, POSITIVE, NEUTRAL, NEGATIVE, VERY_NEGATIVE
-   **📈 Sentiment Score**: Numerical sentiment rating (0-100%)
-   **🏢 Sector-Specific Analysis**: Banking, telecom, consumer goods, automotive sentiment
-   **📰 News Impact Assessment**: Recent events affecting stock performance
-   **🏛️ Economic Indicators**: Indonesian economic factors and policy impacts
-   **🌍 Global Market Influence**: International market effects on Indonesian stocks

#### Sentiment Integration

-   **🎯 Weighted Confidence**: Sentiment affects final signal confidence
-   **⚖️ Risk Adjustment**: Negative sentiment increases risk assessment
-   **📊 Contextual Analysis**: Combines technical and sentiment data
-   **🔍 Real-time Evaluation**: Current market mood and conditions

#### Sentiment Scoring

-   **🟢 Positive (70-100%)**: Strong bullish sentiment, favorable conditions
-   **🟡 Neutral (40-69%)**: Mixed signals, moderate market conditions
-   **🔴 Negative (0-39%)**: Bearish sentiment, unfavorable conditions

### ⚙️ Vision Analysis Configuration

#### 🔧 **Configuration Settings**

```python
# ChatGPT Vision Analysis Settings
ENABLE_CHATGPT_VISION = True  # Enable image analysis with ChatGPT Vision
CHATGPT_VISION_MODEL = "gpt-4o"  # Vision-capable model (required for image analysis)
ENABLE_CHART_PATTERN_ANALYSIS = True  # Analyze chart patterns and visual indicators
ENABLE_TECHNICAL_INDICATOR_VALIDATION = True  # Validate technical indicators visually
CHART_IMAGE_QUALITY = "high"  # Image quality for analysis: "low", "medium", "high"
```

#### 🧪 **Testing Enhanced Analysis**

```bash
# Test enhanced ChatGPT analysis with vision
python test_enhanced_chatgpt.py BBCA.JK

# Test with different stocks
python test_enhanced_chatgpt.py TLKM.JK
python test_enhanced_chatgpt.py BMRI.JK

# Test with US stocks (for comparison)
python test_enhanced_chatgpt.py AAPL
```

#### 📊 **Sample Enhanced Analysis Output**

```
🤖 ENHANCED CHATGPT ANALYSIS RESULTS
==================================================
👁️📊 Analysis Type: Vision + Statistical
🎯 Recommendation: CONFIRM
💪 Confidence: 85.0%
⚠️ Risk Assessment: MEDIUM

📊 STATISTICAL ANALYSIS BREAKDOWN
   🎯 Technical Score: 78.0%
   📈 Volume Confirmation: STRONG
   📊 RSI Assessment: NEUTRAL
   📈 SMA Trend: BULLISH
   🎯 Signal Reliability: HIGH

👁️ VISUAL CHART ANALYSIS
   📈 Chart Pattern: Ascending triangle formation
   📊 Trend Direction: UPTREND
   🎯 Support/Resistance: Strong support at 9,200, resistance at 9,800
   ✅ Visual Confirmation: CONFIRMS
   💪 Chart Strength: STRONG

💼 ENHANCED TRADING STRATEGY
   🎯 Entry: Buy on breakout above 9,800 with volume confirmation
   🚪 Exit: Stop loss at 9,200, take profit at 10,500
   📏 Position Size: 2-3% of portfolio maximum
   ⚠️ Risk Mgmt: Use trailing stop after 5% profit
```

## 📋 Advanced Watchlist System

The bot now includes a powerful watchlist feature for monitoring your favorite stocks with enhanced alerts and priority handling.

### 🎯 Watchlist Features

-   **⭐ Priority Monitoring**: Watchlist stocks get enhanced attention
-   **🔔 Real-time Alerts**: Price movements and volume spikes
-   **📊 Lower Thresholds**: 50% confidence vs 70% for regular stocks
-   **📈 Priority Boost**: 1.2x confidence multiplier for watchlist stocks
-   **📋 Daily Summary**: Comprehensive watchlist performance report
-   **🚨 Instant Notifications**: Immediate alerts for significant changes

### 📊 Watchlist Alerts

#### Price Movement Alerts

-   **📈 5%+ Price Changes**: Automatic alerts for significant moves
-   **📉 Direction Indicators**: Clear up/down movement visualization
-   **💰 Price Tracking**: Historical price monitoring and comparison

#### Volume Alerts

-   **📊 High Volume Detection**: 2x+ normal volume triggers alerts
-   **🔴 Volume Spikes**: Unusual trading activity notifications
-   **📈 Volume Ratio**: Real-time volume vs average comparison

### 🎯 Watchlist Priority System

#### Enhanced Signal Processing

-   **Lower Confidence Threshold**: 50% vs 70% for regular stocks
-   **Confidence Boost**: 1.2x multiplier for watchlist stocks
-   **Priority Filtering**: Watchlist signals get preferential treatment
-   **Enhanced Analysis**: More detailed ChatGPT analysis for watchlist stocks

#### Default Watchlist Stocks

```python
WATCHLIST_STOCKS = [
    'BBCA.JK',  # Bank Central Asia
    'BBRI.JK',  # Bank Rakyat Indonesia
    'BMRI.JK',  # Bank Mandiri
    'TLKM.JK',  # Telkom Indonesia
]
```

### 🛠️ Watchlist Management

#### Using the Watchlist Manager

```bash
# Show watchlist info
python watchlist_manager.py info

# Analyze all watchlist stocks
python watchlist_manager.py analyze

# Monitor watchlist for 30 minutes
python watchlist_manager.py monitor 30
```

#### Sample Watchlist Output

```
📋 COMPREHENSIVE WATCHLIST ANALYSIS
============================================================
📅 Analysis Time: 2024-01-15 14:30:00
📋 Analyzing 4 watchlist stocks...

🔍 Analyzing BBCA.JK (1/4)...
   🟢 Signal: BUY
   💰 Price: 10,250 IDR (+2.45%)
   📊 RSI: 45.2
   📈 Volume: 1.2x normal
   🤖 ChatGPT: CONFIRM (🟢 85.0%)

📋 WATCHLIST SUMMARY
------------------------------
🟢 Buy Signals: 1
🔴 Sell Signals: 0
🚨 Strong Sell Signals: 0
🟡 Hold/No Signal: 3

📈 TOP MOVERS:
   📈 BBCA.JK: +2.45%
```

## Installation & Setup 🚀

### 1. Clone and Install Dependencies

```bash
# Clone the repository
git clone <your-repo-url>
cd TradingBot

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Create Telegram Bot

1. **Create a Bot**:

    - Message [@BotFather](https://t.me/BotFather) on Telegram
    - Send `/newbot` and follow instructions
    - Save your **Bot Token**

2. **Get Your Chat ID**:
    - Message [@userinfobot](https://t.me/userinfobot) on Telegram
    - Save your **Chat ID**

### 3. Get OpenAI API Key (for ChatGPT Confirmation)

1. **Create OpenAI Account**:

    - Go to [OpenAI Platform](https://platform.openai.com/)
    - Sign up or log in to your account

2. **Generate API Key**:

    - Navigate to [API Keys](https://platform.openai.com/api-keys)
    - Click "Create new secret key"
    - Copy and save your **API Key** securely

3. **Add Credits** (if needed):
    - Go to [Billing](https://platform.openai.com/account/billing)
    - Add payment method and credits for API usage
    - ChatGPT confirmation uses minimal credits (~$0.01-0.05 per signal)

### 4. Configure Environment

1. **Create `.env` file** (copy from `env_example.txt`):

```bash
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# ChatGPT Confirmation Settings
ENABLE_CHATGPT_CONFIRMATION = True    # Enable/disable ChatGPT confirmation
CHATGPT_MODEL = "gpt-4o-mini"         # ChatGPT model (cost-effective)
CHATGPT_CONFIDENCE_THRESHOLD = 0.7    # Minimum confidence (0.0-1.0)
CHATGPT_MAX_RETRIES = 2               # API retry attempts
ENABLE_SENTIMENT_ANALYSIS = True      # Enable sentiment analysis
SENTIMENT_WEIGHT = 0.3                # Sentiment influence on confidence (0.0-1.0)
```

2. **Update the values** with your actual credentials.

## Usage 📱

### Test Single Stock (Enhanced)

```bash
# Test with default stock (BBCA.JK) - shows detailed analysis
python test_single_stock.py

# Test with specific stock
python test_single_stock.py BBRI.JK
```

### Run Daily Analysis (One-time)

```bash
python trading_bot.py
```

### Run Scheduled Bot (Production)

```bash
python run_bot.py
```

### Watchlist Management

```bash
# Show current watchlist configuration
python watchlist_manager.py info

# Analyze all watchlist stocks
python watchlist_manager.py analyze

# Monitor watchlist for 30 minutes (real-time)
python watchlist_manager.py monitor 30

# Monitor watchlist for 2 hours
python watchlist_manager.py monitor 120
```

## Enhanced Configuration ⚙️

### Modify Trading Parameters

Edit `config.py` to customize:

```python
# Technical Analysis Parameters
SMA_SHORT_PERIOD = 10  # Short-term SMA
SMA_LONG_PERIOD = 20   # Long-term SMA
RSI_PERIOD = 14        # RSI calculation period

# Sell Signal Parameters
STOP_LOSS_PERCENTAGE = 0.05      # 5% stop loss
TAKE_PROFIT_PERCENTAGE = 0.10    # 10% take profit
RSI_OVERBOUGHT_THRESHOLD = 70    # RSI sell threshold
RSI_OVERSOLD_THRESHOLD = 30      # RSI buy threshold
HIGH_VOLUME_SELL_MULTIPLIER = 2.0 # Volume threshold for sell signals

# ChatGPT Confirmation Settings
ENABLE_CHATGPT_CONFIRMATION = True    # Enable/disable ChatGPT confirmation
CHATGPT_MODEL = "gpt-4o-mini"         # ChatGPT model (cost-effective)
CHATGPT_CONFIDENCE_THRESHOLD = 0.7    # Minimum confidence (0.0-1.0)
CHATGPT_MAX_RETRIES = 2               # API retry attempts
ENABLE_SENTIMENT_ANALYSIS = True      # Enable sentiment analysis
SENTIMENT_WEIGHT = 0.3                # Sentiment influence on confidence (0.0-1.0)

# Signal Validation
MIN_VOLUME_THRESHOLD = 1000000   # Minimum volume
MIN_PRICE_CHANGE = 0.02          # Minimum 2% price change

# Watchlist Configuration
ENABLE_WATCHLIST = True                    # Enable watchlist functionality
WATCHLIST_ALERT_THRESHOLD = 0.5           # Lower threshold for watchlist (50%)
WATCHLIST_PRIORITY_MULTIPLIER = 1.2       # Confidence boost for watchlist
WATCHLIST_PRICE_ALERT_PERCENTAGE = 5.0    # Price movement alert threshold
ENABLE_WATCHLIST_VOLUME_ALERTS = True     # Enable volume alerts
ENABLE_WATCHLIST_DAILY_SUMMARY = True     # Daily watchlist summary
```

## Enhanced Sample Output 📊

### Telegram Message Format (Buy Signal)

```
🇮🇩 Indonesian Stock Signal 🇮🇩

📊 BBCA.JK
📅 Date: 2024-01-15

🟢 Signal: BUY 💪
🎯 Reason: SMA Crossover + RSI OK

💰 Current Price: 10,250 IDR
📈 Price Change: +2.45%
📊 Volume: 15,234,567 (🟡 NORMAL)

📉 SMA 10: 10,180 IDR
📉 SMA 20: 10,050 IDR
📊 RSI: 45.2 (🟡 NEUTRAL)

🎯 Trading Levels:
🛑 Stop Loss: 9,738 IDR (-5%)
🎯 Take Profit: 11,275 IDR (+10%)
📈 Recent High: 10,400 IDR
📉 Recent Low: 9,850 IDR

✅ Valid Signal: Yes
💪 Strength: STRONG

🤖 **ChatGPT Analysis:**
✅ Recommendation: CONFIRM
🟢 Confidence: 85.0%
🟡 Risk Assessment: MEDIUM
📊 Sentiment: 📈 POSITIVE (🟢 78.0%)
🏢 Sector: Indonesian banking sector showing resilience with strong fundamentals and government support...
💭 Analysis: Strong technical setup with SMA crossover confirmed. RSI in healthy range suggests room for upward movement. Volume supports the breakout...

⚠️ **Disclaimer**: This is for educational purposes only. Always do your own research before making investment decisions.
```

### Telegram Message Format (Strong Sell Signal)

```
🇮🇩 Indonesian Stock Signal 🇮🇩

📊 TLKM.JK
📅 Date: 2024-01-15

🚨 Signal: STRONG_SELL 🚨🚨
🎯 Reason: Multiple Bearish Signals

💰 Current Price: 3,850 IDR
📈 Price Change: -3.20%
📊 Volume: 45,678,900 (🔴 HIGH VOLUME)

📉 SMA 10: 3,920 IDR
📉 SMA 20: 4,050 IDR
📊 RSI: 75.8 (🔴 OVERBOUGHT)

🎯 Trading Levels:
🛑 Stop Loss: 3,658 IDR (-5%)
🎯 Take Profit: 4,235 IDR (+10%)
📈 Recent High: 4,100 IDR
📉 Recent Low: 3,750 IDR

✅ Valid Signal: Yes
💪 Strength: VERY_STRONG

🤖 **ChatGPT Analysis:**
❌ Recommendation: REJECT
🔴 Confidence: 45.0%
🔴 Risk Assessment: HIGH
📊 Sentiment: 📉 NEGATIVE (🔴 35.0%)
🏢 Sector: Telecom sector facing regulatory pressures and increased competition from digital services...
💭 Analysis: Multiple bearish indicators present but market conditions suggest potential oversold bounce. High volume could indicate capitulation...

⚠️ **Disclaimer**: This is for educational purposes only. Always do your own research before making investment decisions.
```

### Enhanced Chart Features

-   **3-Panel Layout**: Price/SMA, RSI, Volume
-   **RSI Indicators**: Overbought/Oversold lines
-   **Volume Alerts**: Red bars for high volume
-   **Stop-Loss/Take-Profit Lines**: Visual trading levels
-   **Signal Markers**: Buy (green ▲), Sell (red ▼), Strong Sell (dark red ▼)

## Signal Types & Actions 🎯

### 🟢 BUY Signals

**When to Act:**

-   Enter long positions
-   Set stop-loss at -5%
-   Target take-profit at +10%

### 🔴 SELL Signals

**When to Act:**

-   Exit long positions
-   Take profits if holding
-   Avoid new long entries

### 🚨 STRONG SELL Signals

**When to Act:**

-   **Immediate exit** from positions
-   Consider short positions (if available)
-   High probability of further decline

## Enhanced Testing Output 🧪

The `test_single_stock.py` now provides comprehensive analysis:

```
🇮🇩 INDONESIAN STOCK TRADING BOT - ENHANCED TESTING
============================================================

📊 ENHANCED ANALYSIS RESULTS FOR BBCA.JK
--------------------------------------------------
📅 Date: 2024-01-15
💰 Current Price: 10,250 IDR
📈 Price Change: +2.45%
📊 Volume: 15,234,567
📊 Volume Ratio: 1.2x

🎯 SIGNAL INFORMATION
------------------------------
🟢 Signal: BUY
🎯 Reason: SMA Crossover + RSI OK
✅ Valid: True
💪 Strength: STRONG

📊 TECHNICAL INDICATORS
------------------------------
📉 SMA 10: 10,180 IDR
📉 SMA 20: 10,050 IDR
📊 RSI: 45.2
📊 RSI Status: 🟡 NEUTRAL

🎯 TRADING LEVELS
------------------------------
🛑 Stop Loss: 9,738 IDR (-5%)
🎯 Take Profit: 11,275 IDR (+10%)
📈 Recent High: 10,400 IDR
📉 Recent Low: 9,850 IDR

💡 ACTION RECOMMENDATIONS
------------------------------
🟢 CONSIDER BUYING
   • Entry: Around 10,250 IDR
   • Stop Loss: 9,738 IDR
   • Take Profit: 11,275 IDR

🤖 CHATGPT CONFIRMATION
------------------------------
✅ Recommendation: CONFIRM
🟢 Confidence: 85.0%
🟡 Risk Assessment: MEDIUM
💭 Analysis: Strong technical setup with SMA crossover confirmed. RSI in healthy range suggests room for upward movement...
🔑 Key Factors:
   • SMA crossover with volume confirmation
   • RSI not overbought
   • Indonesian banking sector strength
📝 Notes: Good risk-reward ratio with clear stop-loss level

📊 SENTIMENT ANALYSIS
------------------------------
📈 Overall: POSITIVE (🟢 78.0%)
🏢 Sector: Indonesian banking sector showing strong fundamentals
🌍 Global Impact: Emerging markets gaining favor with investors
📰 News Impact: Recent positive earnings reports boost confidence
🏛️ Economic Factors: Bank Indonesia maintaining supportive monetary policy
📈 Market Mood: Cautiously optimistic with selective buying interest
```

## Scheduling 📅

### Daily Automatic Analysis

The bot runs daily at **5:00 PM Jakarta time** with enhanced analysis:

```python
# Enhanced daily summary includes:
📊 Stocks Analyzed: 10
🚨 Total Signals: 3
🟢 Buy Signals: 1
🔴 Sell Signals: 1
🚨 Strong Sell Signals: 1
```

## File Structure 📁

```
TradingBot/
├── trading_bot.py          # Enhanced main bot script
├── config.py              # Enhanced configuration with sell parameters
├── test_single_stock.py   # Enhanced testing utility
├── watchlist_manager.py   # Watchlist management and monitoring
├── run_bot.py             # Production runner
├── requirements.txt       # Python dependencies
├── env_example.txt        # Environment template
├── README.md             # This file
└── trading_bot.log       # Log file (created when running)
```

## Risk Management 🛡️

### Automatic Risk Controls

-   **5% Stop Loss**: Automatic calculation for all signals
-   **10% Take Profit**: Profit-taking recommendations
-   **Volume Validation**: Minimum 1M volume for valid signals
-   **RSI Confirmation**: Prevents buying in overbought conditions

### Signal Strength Classification

-   **VERY_STRONG**: Strong sell signals (immediate action required)
-   **STRONG**: High-confidence signals with multiple confirmations
-   **MODERATE**: Valid signals with basic confirmations
-   **WEAK**: Signals that don't meet validation criteria

## Troubleshooting 🔧

### Common Issues

1. **"No data found for symbol"**

    - Check if the stock symbol is correct (must end with .JK for Indonesian stocks)
    - Verify internet connection

2. **"Error sending Telegram message"**

    - Verify `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in `.env`
    - Check if bot is added to the chat

3. **"Insufficient data for analysis"**
    - Some stocks may have limited historical data
    - Try with more liquid stocks like BBCA.JK or BBRI.JK

### Enhanced Debug Mode

Enable debug logging by modifying `trading_bot.py`:

```python
logging.basicConfig(level=logging.DEBUG)  # Change from INFO to DEBUG
```

## Disclaimer ⚠️

This bot is for **educational purposes only**. Enhanced sell signals provide additional information but are not financial advice. Always:

-   **Do your own research** before making investment decisions
-   **Use stop-losses** to manage risk
-   **Consider market conditions** and your risk tolerance
-   **Test thoroughly** before using with real money
-   **Understand that past performance** doesn't guarantee future results
-   **Strong sell signals** indicate high risk - act accordingly

## Contributing 🤝

Feel free to contribute by:

-   Adding more technical indicators (MACD, Bollinger Bands, etc.)
-   Improving the sell signal logic
-   Adding more Indonesian stocks
-   Enhancing risk management features
-   Adding backtesting capabilities
-   Implementing portfolio management

## License 📄

This project is open source. Use at your own risk and responsibility.

---

**Happy Trading! 📈🇮🇩**
**Remember: The best trade is sometimes no trade! 🛡️**

### 📋 Watchlist Configuration

```python
# Watchlist Configuration
ENABLE_WATCHLIST = True                    # Enable watchlist functionality
WATCHLIST_ALERT_THRESHOLD = 0.5           # Lower threshold for watchlist (50%)
WATCHLIST_PRIORITY_MULTIPLIER = 1.2       # Confidence boost for watchlist
WATCHLIST_PRICE_ALERT_PERCENTAGE = 5.0    # Price movement alert threshold
ENABLE_WATCHLIST_VOLUME_ALERTS = True     # Enable volume alerts
ENABLE_WATCHLIST_DAILY_SUMMARY = True     # Daily watchlist summary
```
