# 🚀 Murphy's Crypto Trading Bot

A sophisticated Telegram bot for cryptocurrency technical analysis based on **John J. Murphy's "Technical Analysis of Financial Markets"** principles. Perfect for swing trading with comprehensive chart analysis and automated signals.

![Bot Preview](https://via.placeholder.com/800x400/1a1a1a/00ff88?text=Murphy's+Crypto+Trading+Bot)

## 🌟 Features

### 📊 Technical Analysis (Murphy's Methods)

-   **Trend Analysis**: Moving Averages (SMA/EMA), MACD
-   **Momentum Indicators**: RSI, Stochastic Oscillators
-   **Volatility Analysis**: Bollinger Bands, Band Width
-   **Volume Analysis**: OBV, Volume Confirmation
-   **Support/Resistance**: Key level identification
-   **Fibonacci Retracements**: 23.6%, 38.2%, 50%, 61.8%

### 🎯 Pattern Recognition

-   **Reversal Patterns**: Head & Shoulders, Double Tops/Bottoms, Triple Tops/Bottoms
-   **Continuation Patterns**: Triangles (Ascending, Descending, Symmetrical), Flags, Pennants
-   **Chart Pattern Detection**: Automated pattern identification

### 💼 Risk Management

-   **Entry/Exit Points**: Calculated based on technical levels
-   **Stop Loss Levels**: Risk-based stop placement
-   **Take Profit Targets**: Support/resistance based targets
-   **Risk/Reward Ratios**: Automatic R:R calculations

### 📈 Visual Charts

-   **Professional Charts**: Dark theme, multi-timeframe analysis
-   **Technical Overlays**: All indicators visualized
-   **Signal Markers**: Clear buy/sell entry points
-   **Pattern Highlights**: Visual pattern identification

## 🛠️ Installation

### Prerequisites

-   Python 3.8 or higher
-   Telegram Bot Token (from @BotFather)

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd TradingCryptoBot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configuration

1. Copy `config.env` and add your settings:

```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN_HERE

# Optional: Exchange API Keys for real-time data
BINANCE_API_KEY=your_binance_api_key
BINANCE_SECRET_KEY=your_binance_secret_key

# Bot Settings
DEFAULT_TIMEFRAME=4h
DEFAULT_SYMBOLS=BTC/USDT,ETH/USDT,BNB/USDT,ADA/USDT,SOL/USDT
ANALYSIS_INTERVAL=3600
RISK_THRESHOLD=75
```

### 4. Get Telegram Bot Token

1. Message @BotFather on Telegram
2. Create new bot: `/newbot`
3. Choose bot name and username
4. Copy the token and add to `config.env`

### 5. Run the Bot

```bash
python telegram_bot.py
```

## 🎮 Usage

### Basic Commands

-   `/start` - Welcome message and setup
-   `/help` - Show all available commands
-   `/analyze <symbol>` - Analyze specific crypto (e.g., `/analyze BTC/USDT`)
-   `/signals` - Get signals for watchlist
-   `/watchlist` - Manage your crypto watchlist

### Quick Analysis

Simply send a crypto symbol directly:

```
BTC/USDT
ETH/USDT
DOT/USDT
```

### Example Workflow

1. Start bot: `/start`
2. Get watchlist signals: `/signals`
3. Analyze specific coin: `/analyze BTC/USDT`
4. Manage watchlist: `/watchlist`

## 📊 Signal Interpretation

### Signal Types

-   🟢 **BUY**: Multiple bullish indicators aligned
-   🔴 **SELL**: Multiple bearish indicators aligned
-   🟡 **HOLD**: Mixed or neutral signals
-   ⚫ **NO_DATA**: Insufficient data for analysis

### Signal Strength

-   🔥 **STRONG** (80-100%): High confidence, multiple confirmations
-   ⚡ **MEDIUM** (60-79%): Moderate confidence, some confirmations
-   💧 **WEAK** (<60%): Low confidence, limited confirmations

### Risk Levels

-   **GREEN**: Low risk, good R:R ratio
-   **YELLOW**: Medium risk, acceptable R:R
-   **RED**: High risk, poor R:R ratio

## 🔬 Technical Analysis Details

### Murphy's Core Principles

1. **Market Action Discounts Everything**: Price reflects all available information
2. **Prices Move in Trends**: Trends persist until definitively broken
3. **History Repeats Itself**: Patterns repeat due to human psychology

### Indicators Implementation

-   **RSI (14)**: Wilder's original RSI implementation
-   **MACD (12,26,9)**: Standard MACD settings
-   **Bollinger Bands (20,2)**: 20-period SMA with 2 standard deviations
-   **Volume Analysis**: 20-period volume moving average
-   **Support/Resistance**: 20-period high/low analysis

### Pattern Detection Algorithms

-   **Head & Shoulders**: Peak analysis with volume confirmation
-   **Double Tops/Bottoms**: Price level comparison within 2% tolerance
-   **Triangles**: Trendline convergence analysis
-   **Fibonacci Levels**: Automatic swing high/low identification

## 🚀 Advanced Features

### Chart Generation

-   **Multi-Panel Layout**: Price, RSI, Volume, Signal Summary
-   **Professional Styling**: Dark theme, clear indicators
-   **Export Quality**: High-resolution PNG format
-   **Mobile Optimized**: Readable on all devices

### Automated Monitoring

-   **Watchlist Tracking**: Monitor multiple symbols
-   **Signal Alerts**: Real-time notifications
-   **Pattern Alerts**: Notify when patterns form
-   **Risk Warnings**: Alert on high-risk setups

## 🔧 Customization

### Adding New Indicators

1. Edit `technical_analyzer.py`
2. Add indicator calculation in `calculate_indicators()`
3. Include in signal generation logic
4. Update chart visualization

### Custom Patterns

1. Add pattern detection in `detect_patterns()`
2. Define pattern criteria
3. Include in signal scoring
4. Add to chart annotations

### Timeframe Modification

-   Supported: 1m, 5m, 15m, 30m, 1h, 4h, 1d, 1w
-   Default: 4h (optimal for swing trading)
-   Modify in `config.env` or per analysis

## 📈 Trading Integration

### Supported Exchanges

-   **Binance** (Primary data source)
-   **Binance US**
-   **Coinbase Pro** (via CCXT)
-   **Kraken** (via CCXT)

### Portfolio Tracking

-   Track multiple positions
-   Calculate portfolio performance
-   Risk assessment across holdings
-   Correlation analysis

## 🛡️ Risk Disclaimer

> **⚠️ Important**: This bot is for educational and informational purposes only.
>
> -   **Not Financial Advice**: All signals are based on technical analysis only
> -   **Risk Warning**: Cryptocurrency trading involves substantial risk
> -   **No Guarantees**: Past performance doesn't guarantee future results
> -   **Personal Responsibility**: Always do your own research (DYOR)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📚 References

-   **John J. Murphy**: "Technical Analysis of the Financial Markets"
-   **Technical Analysis Library**: TA-Lib Python implementation
-   **CCXT**: Cryptocurrency exchange trading library
-   **Python Telegram Bot**: Official Telegram bot framework

## 📞 Support

-   **Issues**: Open GitHub issue
-   **Questions**: Start a discussion
-   **Features**: Submit feature requests
-   **Community**: Join our Telegram group

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ for the crypto trading community**

_"The trend is your friend until it bends at the end"_ - John J. Murphy
