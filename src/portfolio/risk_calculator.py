# src/portfolio/risk_calculator.py
import numpy as np
import pandas as pd
from scipy import stats

class PortfolioRiskAnalyzer:
    def __init__(self, portfolio_data):
        self.portfolio = portfolio_data
        self.correlation_threshold = 0.7
    
    def analyze_correlations(self, price_data):
        """Detect dangerous correlations in portfolio"""
        correlation_matrix = price_data.pct_change().corr()
        
        high_correlations = []
        for i in range(len(correlation_matrix.columns)):
            for j in range(i+1, len(correlation_matrix.columns)):
                corr_value = correlation_matrix.iloc[i, j]
                if abs(corr_value) > self.correlation_threshold:
                    high_correlations.append({
                        'pair': (correlation_matrix.columns[i], correlation_matrix.columns[j]),
                        'correlation': corr_value,
                        'risk_level': 'HIGH' if corr_value > 0.85 else 'MEDIUM'
                    })
        
        return {
            'high_correlations': high_correlations,
            'diversification_score': self._calculate_diversification_score(correlation_matrix),
            'recommendations': self._get_diversification_recommendations(high_correlations)
        }
    
    def calculate_var(self, returns, confidence_level=0.95):
        """Calculate Value at Risk"""
        return np.percentile(returns, (1 - confidence_level) * 100)
    
    def calculate_sharpe_ratio(self, returns, risk_free_rate=0.02):
        """Calculate Sharpe Ratio for risk-adjusted returns"""
        excess_returns = returns - risk_free_rate/252
        return np.sqrt(252) * excess_returns.mean() / excess_returns.std()
