# src/analyzers/technical_analysis.py
import yfinance as yf
import pandas as pd
import numpy as np
from ta import add_all_ta_features
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands

class TechnicalAnalyzer:
    def __init__(self):
        self.patterns = {
            'vcp': self.detect_vcp_pattern,
            'pinch': self.detect_pinch_pattern,
            'breakout': self.detect_breakout
        }
    
    def detect_vcp_pattern(self, df, symbol):
        """Volatility Contraction Pattern detection"""
        # Calculate contractions
        df['high_low_pct'] = (df['High'] - df['Low']) / df['Close'] * 100
        df['contraction'] = df['high_low_pct'].rolling(window=10).mean()
        
        # Detect VCP: Series of lower highs with contracting volatility
        contractions = []
        for i in range(3, len(df)-20):
            window = df.iloc[i:i+20]
            if window['contraction'].iloc[-1] < window['contraction'].iloc[0] * 0.7:
                if window['Volume'].iloc[-5:].mean() < window['Volume'].iloc[:5].mean() * 0.8:
                    contractions.append({
                        'date': window.index[-1],
                        'strength': 1 - (window['contraction'].iloc[-1] / window['contraction'].iloc[0]),
                        'price': window['Close'].iloc[-1]
                    })
        
        return {
            'detected': len(contractions) > 0,
            'signals': contractions,
            'recommendation': 'BUY' if contractions and contractions[-1]['strength'] > 0.3 else 'HOLD'
        }
    
    def detect_pinch_pattern(self, df):
        """Detect Bollinger Band Pinch (low volatility precedes big moves)"""
        bb = BollingerBands(df['Close'])
        df['bb_width'] = bb.bollinger_hband() - bb.bollinger_lband()
        df['bb_pinch'] = df['bb_width'] < df['bb_width'].rolling(50).mean() * 0.5
        
        pinch_zones = df[df['bb_pinch']].tail(5)
        
        return {
            'active_pinch': len(pinch_zones) > 0,
            'dates': pinch_zones.index.tolist(),
            'volatility_rank': df['bb_width'].iloc[-1] / df['bb_width'].mean()
        }
    
    def calculate_rsi_signals(self, df):
        """RSI with divergence detection"""
        rsi = RSIIndicator(df['Close'])
        df['rsi'] = rsi.rsi()
        
        # Detect divergences
        price_lows = df['Low'].rolling(5).min()
        rsi_lows = df['rsi'].rolling(5).min()
        
        bullish_divergence = (
            (df['Low'].iloc[-1] < df['Low'].iloc[-20]) & 
            (df['rsi'].iloc[-1] > df['rsi'].iloc[-20])
        )
        
        return {
            'current_rsi': df['rsi'].iloc[-1],
            'oversold': df['rsi'].iloc[-1] < 30,
            'overbought': df['rsi'].iloc[-1] > 70,
            'bullish_divergence': bullish_divergence,
            'signal': self._get_rsi_signal(df['rsi'].iloc[-1], bullish_divergence)
        }# src/analyzers/technical_analysis.py
import yfinance as yf
import pandas as pd
import numpy as np
from ta import add_all_ta_features
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands

class TechnicalAnalyzer:
    def __init__(self):
        self.patterns = {
            'vcp': self.detect_vcp_pattern,
            'pinch': self.detect_pinch_pattern,
            'breakout': self.detect_breakout
        }
    
    def detect_vcp_pattern(self, df, symbol):
        """Volatility Contraction Pattern detection"""
        # Calculate contractions
        df['high_low_pct'] = (df['High'] - df['Low']) / df['Close'] * 100
        df['contraction'] = df['high_low_pct'].rolling(window=10).mean()
        
        # Detect VCP: Series of lower highs with contracting volatility
        contractions = []
        for i in range(3, len(df)-20):
            window = df.iloc[i:i+20]
            if window['contraction'].iloc[-1] < window['contraction'].iloc[0] * 0.7:
                if window['Volume'].iloc[-5:].mean() < window['Volume'].iloc[:5].mean() * 0.8:
                    contractions.append({
                        'date': window.index[-1],
                        'strength': 1 - (window['contraction'].iloc[-1] / window['contraction'].iloc[0]),
                        'price': window['Close'].iloc[-1]
                    })
        
        return {
            'detected': len(contractions) > 0,
            'signals': contractions,
            'recommendation': 'BUY' if contractions and contractions[-1]['strength'] > 0.3 else 'HOLD'
        }
    
    def detect_pinch_pattern(self, df):
        """Detect Bollinger Band Pinch (low volatility precedes big moves)"""
        bb = BollingerBands(df['Close'])
        df['bb_width'] = bb.bollinger_hband() - bb.bollinger_lband()
        df['bb_pinch'] = df['bb_width'] < df['bb_width'].rolling(50).mean() * 0.5
        
        pinch_zones = df[df['bb_pinch']].tail(5)
        
        return {
            'active_pinch': len(pinch_zones) > 0,
            'dates': pinch_zones.index.tolist(),
            'volatility_rank': df['bb_width'].iloc[-1] / df['bb_width'].mean()
        }
    
    def calculate_rsi_signals(self, df):
        """RSI with divergence detection"""
        rsi = RSIIndicator(df['Close'])
        df['rsi'] = rsi.rsi()
        
        # Detect divergences
        price_lows = df['Low'].rolling(5).min()
        rsi_lows = df['rsi'].rolling(5).min()
        
        bullish_divergence = (
            (df['Low'].iloc[-1] < df['Low'].iloc[-20]) & 
            (df['rsi'].iloc[-1] > df['rsi'].iloc[-20])
        )
        
        return {
            'current_rsi': df['rsi'].iloc[-1],
            'oversold': df['rsi'].iloc[-1] < 30,
            'overbought': df['rsi'].iloc[-1] > 70,
            'bullish_divergence': bullish_divergence,
            'signal': self._get_rsi_signal(df['rsi'].iloc[-1], bullish_divergence)
        }
