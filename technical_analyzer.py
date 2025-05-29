import pandas as pd
import numpy as np
import ta
from typing import Dict, List, Tuple, Optional
import ccxt
from datetime import datetime, timedelta

class MurphyTechnicalAnalyzer:
    """Technical Analysis based on John J. Murphy's principles"""
    
    def __init__(self):
        self.exchange = ccxt.binance()
        
    def get_ohlcv_data(self, symbol: str, timeframe: str = '4h', limit: int = 200) -> pd.DataFrame:
        """Fetch OHLCV data from exchange"""
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            return df
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return pd.DataFrame()
    
    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate technical indicators based on Murphy's methods"""
        if df.empty:
            return df
            
        # Moving Averages (Murphy's Trend Analysis)
        df['sma_20'] = ta.trend.sma_indicator(df['close'], window=20)
        df['sma_50'] = ta.trend.sma_indicator(df['close'], window=50)
        df['ema_12'] = ta.trend.ema_indicator(df['close'], window=12)
        df['ema_26'] = ta.trend.ema_indicator(df['close'], window=26)
        
        # MACD (Murphy's Momentum Analysis)
        df['macd'] = ta.trend.macd_diff(df['close'])
        df['macd_signal'] = ta.trend.macd_signal(df['close'])
        df['macd_histogram'] = ta.trend.macd(df['close'])
        
        # RSI (Wilder's RSI - mentioned in Murphy's book)
        df['rsi'] = ta.momentum.rsi(df['close'], window=14)
        
        # Bollinger Bands (Murphy's Volatility Analysis)
        bb = ta.volatility.BollingerBands(df['close'])
        df['bb_upper'] = bb.bollinger_hband()
        df['bb_middle'] = bb.bollinger_mavg()
        df['bb_lower'] = bb.bollinger_lband()
        df['bb_width'] = (df['bb_upper'] - df['bb_lower']) / df['bb_middle'] * 100
        
        # Volume Analysis (Murphy's Volume Principles) - Fixed
        df['volume_sma'] = df['volume'].rolling(window=20).mean()
        df['obv'] = ta.volume.on_balance_volume(df['close'], df['volume'])
        
        # Support and Resistance Levels
        df['support'] = df['low'].rolling(window=20).min()
        df['resistance'] = df['high'].rolling(window=20).max()
        
        # Fibonacci Retracements (Murphy's Retracement Analysis)
        df = self.calculate_fibonacci_levels(df)
        
        return df
    
    def calculate_fibonacci_levels(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate Fibonacci retracement levels"""
        if len(df) < 20:
            return df
            
        # Find recent swing high and low
        recent_high = df['high'].tail(20).max()
        recent_low = df['low'].tail(20).min()
        
        diff = recent_high - recent_low
        
        df['fib_23.6'] = recent_high - (diff * 0.236)
        df['fib_38.2'] = recent_high - (diff * 0.382)
        df['fib_50.0'] = recent_high - (diff * 0.500)
        df['fib_61.8'] = recent_high - (diff * 0.618)
        
        return df
    
    def detect_patterns(self, df: pd.DataFrame) -> Dict[str, str]:
        """Detect chart patterns based on Murphy's pattern analysis"""
        patterns = {
            'head_shoulders': 'NONE',
            'double_top': 'NONE',
            'double_bottom': 'NONE',
            'triangle': 'NONE',
            'flag': 'NONE'
        }
        
        if len(df) < 50:
            return patterns
        
        # Head and Shoulders Detection (simplified)
        recent_highs = df['high'].tail(20)
        if len(recent_highs) >= 3:
            peaks = recent_highs.nlargest(3)
            if len(peaks) == 3:
                if peaks.iloc[1] > peaks.iloc[0] and peaks.iloc[1] > peaks.iloc[2]:
                    patterns['head_shoulders'] = 'BEARISH'
        
        # Double Top/Bottom Detection
        recent_data = df.tail(30)
        highs = recent_data['high']
        lows = recent_data['low']
        
        # Double Top
        if len(highs) >= 2:
            max_high = highs.max()
            second_max = highs.nlargest(2).iloc[1]
            if abs(max_high - second_max) / max_high < 0.02:  # Within 2%
                patterns['double_top'] = 'BEARISH'
        
        # Double Bottom
        if len(lows) >= 2:
            min_low = lows.min()
            second_min = lows.nsmallest(2).iloc[1]
            if abs(min_low - second_min) / min_low < 0.02:  # Within 2%
                patterns['double_bottom'] = 'BULLISH'
        
        # Triangle Pattern Detection (simplified)
        if len(df) >= 20:
            recent_highs = df['high'].tail(20)
            recent_lows = df['low'].tail(20)
            
            high_trend = np.polyfit(range(len(recent_highs)), recent_highs, 1)[0]
            low_trend = np.polyfit(range(len(recent_lows)), recent_lows, 1)[0]
            
            if abs(high_trend) < 0.1 and low_trend > 0.1:
                patterns['triangle'] = 'ASCENDING'
            elif high_trend < -0.1 and abs(low_trend) < 0.1:
                patterns['triangle'] = 'DESCENDING'
            elif high_trend < -0.1 and low_trend > 0.1:
                patterns['triangle'] = 'SYMMETRICAL'
        
        return patterns
    
    def generate_signals(self, df: pd.DataFrame) -> Dict[str, any]:
        """Generate trading signals based on Murphy's analysis"""
        if df.empty or len(df) < 50:
            return self.empty_signal()
        
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        signals = {
            'timestamp': latest.name,
            'price': latest['close'],
            'signal': 'HOLD',
            'strength': 'WEAK',
            'confidence': 0,
            'entry_price': 0,
            'stop_loss': 0,
            'take_profit': 0,
            'risk_reward': 0,
            'indicators': {},
            'patterns': {},
            'analysis': []
        }
        
        # Trend Analysis (Murphy's Trend Principles)
        trend_signals = []
        
        # Moving Average Crossover
        if latest['ema_12'] > latest['ema_26'] and prev['ema_12'] <= prev['ema_26']:
            trend_signals.append('BULLISH_MA_CROSS')
        elif latest['ema_12'] < latest['ema_26'] and prev['ema_12'] >= prev['ema_26']:
            trend_signals.append('BEARISH_MA_CROSS')
        
        # Price vs SMA
        if latest['close'] > latest['sma_20'] > latest['sma_50']:
            trend_signals.append('BULLISH_TREND')
        elif latest['close'] < latest['sma_20'] < latest['sma_50']:
            trend_signals.append('BEARISH_TREND')
        
        # MACD Analysis
        macd_signals = []
        if latest['macd'] > latest['macd_signal'] and prev['macd'] <= prev['macd_signal']:
            macd_signals.append('BULLISH_MACD')
        elif latest['macd'] < latest['macd_signal'] and prev['macd'] >= prev['macd_signal']:
            macd_signals.append('BEARISH_MACD')
        
        # RSI Analysis (Murphy's Momentum Principles)
        rsi_signals = []
        if latest['rsi'] < 30:
            rsi_signals.append('OVERSOLD')
        elif latest['rsi'] > 70:
            rsi_signals.append('OVERBOUGHT')
        elif 40 <= latest['rsi'] <= 60:
            rsi_signals.append('NEUTRAL')
        
        # Bollinger Bands Analysis
        bb_signals = []
        if latest['close'] > latest['bb_upper']:
            bb_signals.append('BB_BREAKOUT_UP')
        elif latest['close'] < latest['bb_lower']:
            bb_signals.append('BB_BREAKOUT_DOWN')
        elif latest['bb_width'] < 10:
            bb_signals.append('BB_SQUEEZE')
        
        # Volume Analysis (Murphy's Volume Principles)
        volume_signals = []
        if latest['volume'] > latest['volume_sma'] * 1.5:
            volume_signals.append('HIGH_VOLUME')
        elif latest['volume'] < latest['volume_sma'] * 0.5:
            volume_signals.append('LOW_VOLUME')
        
        # Support/Resistance Analysis
        sr_signals = []
        price = latest['close']
        if abs(price - latest['support']) / price < 0.02:
            sr_signals.append('AT_SUPPORT')
        elif abs(price - latest['resistance']) / price < 0.02:
            sr_signals.append('AT_RESISTANCE')
        
        # Generate final signal
        bullish_count = len([s for s in trend_signals + macd_signals + rsi_signals + bb_signals if 'BULLISH' in s or 'OVERSOLD' in s])
        bearish_count = len([s for s in trend_signals + macd_signals + rsi_signals + bb_signals if 'BEARISH' in s or 'OVERBOUGHT' in s])
        
        # Determine signal strength and direction
        if bullish_count > bearish_count and bullish_count >= 2:
            signals['signal'] = 'BUY'
            signals['confidence'] = min(bullish_count * 20, 100)
        elif bearish_count > bullish_count and bearish_count >= 2:
            signals['signal'] = 'SELL'
            signals['confidence'] = min(bearish_count * 20, 100)
        else:
            signals['signal'] = 'HOLD'
            signals['confidence'] = 50
        
        # Determine signal strength
        if signals['confidence'] >= 80:
            signals['strength'] = 'STRONG'
        elif signals['confidence'] >= 60:
            signals['strength'] = 'MEDIUM'
        else:
            signals['strength'] = 'WEAK'
        
        # Calculate entry, stop loss, and take profit
        if signals['signal'] == 'BUY':
            signals['entry_price'] = latest['close']
            signals['stop_loss'] = max(latest['support'], latest['close'] * 0.95)
            signals['take_profit'] = min(latest['resistance'], latest['close'] * 1.1)
        elif signals['signal'] == 'SELL':
            signals['entry_price'] = latest['close']
            signals['stop_loss'] = min(latest['resistance'], latest['close'] * 1.05)
            signals['take_profit'] = max(latest['support'], latest['close'] * 0.9)
        
        # Calculate risk/reward ratio
        if signals['stop_loss'] != 0:
            risk = abs(signals['entry_price'] - signals['stop_loss'])
            reward = abs(signals['take_profit'] - signals['entry_price'])
            signals['risk_reward'] = round(reward / risk, 2) if risk > 0 else 0
        
        # Store detailed analysis
        signals['indicators'] = {
            'rsi': round(latest['rsi'], 2),
            'macd': round(latest['macd'], 4),
            'sma_20': round(latest['sma_20'], 2),
            'sma_50': round(latest['sma_50'], 2),
            'bb_width': round(latest['bb_width'], 2),
            'volume_ratio': round(latest['volume'] / latest['volume_sma'], 2)
        }
        
        signals['patterns'] = self.detect_patterns(df)
        
        signals['analysis'] = {
            'trend': trend_signals,
            'momentum': macd_signals + rsi_signals,
            'volatility': bb_signals,
            'volume': volume_signals,
            'support_resistance': sr_signals
        }
        
        return signals
    
    def empty_signal(self) -> Dict[str, any]:
        """Return empty signal structure"""
        return {
            'timestamp': datetime.now(),
            'price': 0,
            'signal': 'NO_DATA',
            'strength': 'NONE',
            'confidence': 0,
            'entry_price': 0,
            'stop_loss': 0,
            'take_profit': 0,
            'risk_reward': 0,
            'indicators': {},
            'patterns': {},
            'analysis': []
        }
    
    def analyze_symbol(self, symbol: str, timeframe: str = '4h') -> Dict[str, any]:
        """Complete technical analysis for a symbol"""
        try:
            # Get data
            df = self.get_ohlcv_data(symbol, timeframe)
            if df.empty:
                return self.empty_signal()
            
            # Calculate indicators
            df = self.calculate_indicators(df)
            
            # Generate signals
            signals = self.generate_signals(df)
            signals['symbol'] = symbol
            signals['timeframe'] = timeframe
            
            return signals
            
        except Exception as e:
            print(f"Error analyzing {symbol}: {e}")
            return self.empty_signal() 