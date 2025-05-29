import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
import pandas as pd
import numpy as np
from datetime import datetime
import io
from typing import Dict, Tuple
import seaborn as sns

class TechnicalChartGenerator:
    """Generate technical analysis charts similar to the example image"""
    
    def __init__(self):
        plt.style.use('dark_background')
        sns.set_palette("husl")
        
    def create_analysis_chart(self, df: pd.DataFrame, signals: Dict, symbol: str) -> io.BytesIO:
        """Create comprehensive technical analysis chart"""
        
        # Set up the figure with subplots
        fig = plt.figure(figsize=(16, 12), facecolor='black')
        fig.suptitle(f'{symbol} - Murphy Technical Analysis', fontsize=16, color='white', y=0.98)
        
        # Define grid layout
        gs = fig.add_gridspec(4, 2, height_ratios=[3, 1, 1, 0.5], width_ratios=[3, 1], 
                             hspace=0.3, wspace=0.2)
        
        # Main price chart
        ax_main = fig.add_subplot(gs[0, :])
        self.plot_price_chart(ax_main, df, signals, symbol)
        
        # RSI
        ax_rsi = fig.add_subplot(gs[1, :])
        self.plot_rsi(ax_rsi, df)
        
        # Volume
        ax_volume = fig.add_subplot(gs[2, :])
        self.plot_volume(ax_volume, df)
        
        # Signal summary
        ax_summary = fig.add_subplot(gs[3, :])
        self.plot_signal_summary(ax_summary, signals)
        
        plt.tight_layout()
        
        # Save to BytesIO buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', facecolor='black', edgecolor='none', 
                   bbox_inches='tight', dpi=150)
        buffer.seek(0)
        plt.close()
        
        return buffer
    
    def plot_price_chart(self, ax, df: pd.DataFrame, signals: Dict, symbol: str):
        """Plot main price chart with indicators"""
        
        # Price line
        ax.plot(df.index, df['close'], color='#00ff88', linewidth=2, label='Price')
        
        # Moving averages
        if 'sma_20' in df.columns:
            ax.plot(df.index, df['sma_20'], color='orange', linewidth=1, label='SMA 20', alpha=0.8)
        if 'sma_50' in df.columns:
            ax.plot(df.index, df['sma_50'], color='red', linewidth=1, label='SMA 50', alpha=0.8)
        
        # Bollinger Bands
        if 'bb_upper' in df.columns and 'bb_lower' in df.columns:
            ax.fill_between(df.index, df['bb_upper'], df['bb_lower'], 
                           alpha=0.1, color='blue', label='Bollinger Bands')
            ax.plot(df.index, df['bb_upper'], color='blue', linewidth=0.5, alpha=0.7)
            ax.plot(df.index, df['bb_lower'], color='blue', linewidth=0.5, alpha=0.7)
        
        # Support and Resistance
        if 'support' in df.columns and 'resistance' in df.columns:
            latest_support = df['support'].iloc[-1]
            latest_resistance = df['resistance'].iloc[-1]
            
            ax.axhline(y=latest_support, color='green', linestyle='--', alpha=0.6, label='Support')
            ax.axhline(y=latest_resistance, color='red', linestyle='--', alpha=0.6, label='Resistance')
        
        # Entry, Stop Loss, Take Profit levels
        if signals['signal'] in ['BUY', 'SELL']:
            if signals['entry_price'] > 0:
                ax.axhline(y=signals['entry_price'], color='yellow', linewidth=2, label='Entry')
            if signals['stop_loss'] > 0:
                ax.axhline(y=signals['stop_loss'], color='red', linewidth=1, linestyle=':', label='Stop Loss')
            if signals['take_profit'] > 0:
                ax.axhline(y=signals['take_profit'], color='green', linewidth=1, linestyle=':', label='Take Profit')
        
        # Signal marker
        if signals['signal'] in ['BUY', 'SELL']:
            latest_price = df['close'].iloc[-1]
            latest_time = df.index[-1]
            
            if signals['signal'] == 'BUY':
                ax.scatter(latest_time, latest_price, color='green', s=200, marker='^', 
                          zorder=5, label='BUY Signal')
            else:
                ax.scatter(latest_time, latest_price, color='red', s=200, marker='v', 
                          zorder=5, label='SELL Signal')
        
        # Formatting
        ax.set_ylabel('Price (USDT)', color='white')
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.2)
        ax.legend(loc='upper left', framealpha=0.1)
        ax.set_facecolor('black')
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=6))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    def plot_rsi(self, ax, df: pd.DataFrame):
        """Plot RSI indicator"""
        if 'rsi' in df.columns:
            ax.plot(df.index, df['rsi'], color='purple', linewidth=2)
            ax.axhline(y=70, color='red', linestyle='--', alpha=0.7, label='Overbought')
            ax.axhline(y=30, color='green', linestyle='--', alpha=0.7, label='Oversold')
            ax.axhline(y=50, color='gray', linestyle='-', alpha=0.5)
            
            # Fill overbought/oversold areas
            ax.fill_between(df.index, 70, 100, alpha=0.1, color='red')
            ax.fill_between(df.index, 0, 30, alpha=0.1, color='green')
            
        ax.set_ylabel('RSI', color='white')
        ax.set_ylim(0, 100)
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.2)
        ax.set_facecolor('black')
        ax.legend(loc='upper right', framealpha=0.1)
    
    def plot_volume(self, ax, df: pd.DataFrame):
        """Plot volume with moving average"""
        # Volume bars
        colors = ['green' if df['close'].iloc[i] >= df['open'].iloc[i] else 'red' 
                 for i in range(len(df))]
        ax.bar(df.index, df['volume'], color=colors, alpha=0.6, width=0.8)
        
        # Volume moving average
        if 'volume_sma' in df.columns:
            ax.plot(df.index, df['volume_sma'], color='yellow', linewidth=1, label='Vol MA')
        
        ax.set_ylabel('Volume', color='white')
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.2)
        ax.set_facecolor('black')
        ax.legend(loc='upper right', framealpha=0.1)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    
    def plot_signal_summary(self, ax, signals: Dict):
        """Plot signal summary information"""
        ax.axis('off')
        
        # Signal status
        signal_color = {
            'BUY': 'green',
            'SELL': 'red', 
            'HOLD': 'yellow',
            'NO_DATA': 'gray'
        }
        
        strength_color = {
            'STRONG': 'green',
            'MEDIUM': 'orange',
            'WEAK': 'red',
            'NONE': 'gray'
        }
        
        # Create text summary
        summary_text = f"""
🎯 Signal: {signals['signal']} | Strength: {signals['strength']} | Confidence: {signals['confidence']}%
💰 Price: ${signals['price']:.4f} | Entry: ${signals['entry_price']:.4f}
🛡️ Stop Loss: ${signals['stop_loss']:.4f} | 🎯 Take Profit: ${signals['take_profit']:.4f}
📊 Risk/Reward: 1:{signals['risk_reward']} | RSI: {signals['indicators'].get('rsi', 'N/A')}
📈 SMA20: ${signals['indicators'].get('sma_20', 'N/A')} | SMA50: ${signals['indicators'].get('sma_50', 'N/A')}
        """
        
        ax.text(0.02, 0.5, summary_text, transform=ax.transAxes, fontsize=11,
                color='white', verticalalignment='center', fontfamily='monospace',
                bbox=dict(boxstyle="round,pad=0.5", facecolor='black', alpha=0.8))
        
        # Add pattern detection
        patterns_text = "Patterns: "
        active_patterns = [f"{k}:{v}" for k, v in signals['patterns'].items() if v != 'NONE']
        if active_patterns:
            patterns_text += " | ".join(active_patterns)
        else:
            patterns_text += "None detected"
            
        ax.text(0.98, 0.5, patterns_text, transform=ax.transAxes, fontsize=10,
                color='cyan', verticalalignment='center', horizontalalignment='right',
                fontfamily='monospace')
    
    def create_simple_chart(self, symbol: str, price: float, signals: Dict) -> io.BytesIO:
        """Create a simple signal chart when full data is not available"""
        
        fig, ax = plt.subplots(figsize=(10, 6), facecolor='black')
        
        # Simple signal display
        signal_colors = {'BUY': 'green', 'SELL': 'red', 'HOLD': 'yellow', 'NO_DATA': 'gray'}
        
        ax.text(0.5, 0.7, f"{symbol}", ha='center', va='center', transform=ax.transAxes,
                fontsize=24, color='white', fontweight='bold')
        
        ax.text(0.5, 0.5, f"Signal: {signals['signal']}", ha='center', va='center', 
                transform=ax.transAxes, fontsize=20, 
                color=signal_colors.get(signals['signal'], 'white'))
        
        ax.text(0.5, 0.3, f"Price: ${price:.4f}", ha='center', va='center', 
                transform=ax.transAxes, fontsize=16, color='white')
        
        ax.text(0.5, 0.1, f"Confidence: {signals['confidence']}% | Strength: {signals['strength']}", 
                ha='center', va='center', transform=ax.transAxes, fontsize=14, color='cyan')
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        ax.set_facecolor('black')
        
        # Save to buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', facecolor='black', edgecolor='none', 
                   bbox_inches='tight', dpi=150)
        buffer.seek(0)
        plt.close()
        
        return buffer 