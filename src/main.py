# src/main.py
#!/usr/bin/env python3
"""
Financial AI Advisor - Main Entry Point
"""

import os
import sys
import json
import asyncio
import argparse
from datetime import datetime

# Add src to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ============================================================================
# TEST FUNCTIONS (For initial setup verification)
# ============================================================================

def test_system():
    """Test basic functionality"""
    print("🚀 Financial AI Advisor - System Test")
    print("=" * 50)
    
    # Test market data
    print("\n📊 Testing Market Data...")
    try:
        from utils.market_data_helper import MarketDataFetcher
        fetcher = MarketDataFetcher()
        
        # Load portfolio
        with open('data/portfolio.json', 'r') as f:
            portfolio = json.load(f)
        
        # Test with portfolio stocks
        for stock in portfolio['stocks'][:2]:  # Test first 2 stocks
            symbol = stock['symbol']
            print(f"Fetching {symbol}...")
            data = fetcher.get_stock_price(symbol)
            if data:
                print(f"  ✅ {symbol}: ${data['price']:.2f} (source: {data['source']})")
            else:
                print(f"  ❌ {symbol}: Failed to fetch")
    except ImportError as e:
        print(f"  ⚠️ Market data module not ready: {e}")
    except Exception as e:
        print(f"  ❌ Market data test failed: {e}")
    
    # Test LLM
    print("\n🤖 Testing AI Models...")
    try:
        from ai_models.llm_orchestrator import LLMOrchestrator
        llm = LLMOrchestrator()
        
        test_prompt = "Give me a one-line bullish or bearish sentiment for AAPL stock."
        
        # Test Groq
        response = llm.query_groq(test_prompt)
        if response:
            print(f"  ✅ Groq: {response[:100]}...")
        else:
            print(f"  ⚠️ Groq: Not available")
    except ImportError as e:
        print(f"  ⚠️ LLM module not ready: {e}")
    except Exception as e:
        print(f"  ❌ LLM test failed: {e}")
    
    # Test Email
    print("\n📧 Testing Email Collection...")
    try:
        from collectors.email_collector import EmailCollector
        collector = EmailCollector()
        print(f"  ✅ Email collector initialized")
    except ImportError as e:
        print(f"  ⚠️ Email module not ready: {e}")
    except Exception as e:
        print(f"  ❌ Email test failed: {e}")
    
    print("\n✅ System test complete!")
    return True

# ============================================================================
# MAIN FINANCIAL AI ADVISOR CLASS (Full Implementation)
# ============================================================================

class FinancialAIAdvisor:
    def __init__(self):
        """Initialize the Financial AI Advisor"""
        self.initialized = False
        try:
            self.load_config()
            self.initialize_components()
            self.initialized = True
        except Exception as e:
            print(f"⚠️ Partial initialization: {e}")
            # Continue with limited functionality for testing
    
    def load_config(self):
        """Load configuration"""
        # For now, use environment variables
        self.config = {
            'email': os.environ.get('SMTP_USER'),
            'portfolio_file': 'data/portfolio.json',
            'questions_file': 'data/questions_queue.json'
        }
        
        # Load portfolio
        if os.path.exists(self.config['portfolio_file']):
            with open(self.config['portfolio_file'], 'r') as f:
                self.portfolio = json.load(f)
        else:
            self.portfolio = {'stocks': [], 'crypto': [], 'commodities': []}
    
    def initialize_components(self):
        """Initialize all components with error handling"""
        self.components = {}
        
        # Try to initialize each component
        try:
            from collectors.email_collector import EmailCollector
            self.email_collector = EmailCollector()
            self.components['email'] = True
        except:
            self.components['email'] = False
            
        try:
            from utils.market_data_helper import MarketDataFetcher
            self.market_fetcher = MarketDataFetcher()
            self.components['market'] = True
        except:
            self.components['market'] = False
            
        try:
            from ai_models.llm_orchestrator import LLMOrchestrator
            self.llm = LLMOrchestrator()
            self.components['llm'] = True
        except:
            self.components['llm'] = False
        
        # Print component status
        print("🔧 Component Status:")
        for comp, status in self.components.items():
            print(f"  {comp}: {'✅' if status else '❌'}")
    
    def load_pending_questions(self):
        """Load questions from queue"""
        if os.path.exists(self.config['questions_file']):
            with open(self.config['questions_file'], 'r') as f:
                content = f.read()
                if content:
                    questions = json.loads(content)
                    # Filter pending questions
                    return [q for q in questions if q.get('status') == 'pending']
        return []
    
    async def fetch_all_market_data(self):
        """Fetch market data for portfolio"""
        market_data = {}
        
        if not self.components.get('market'):
            print("⚠️ Market data component not available")
            return market_data
            
        for stock in self.portfolio.get('stocks', []):
            symbol = stock['symbol']
            data = self.market_fetcher.get_stock_price(symbol)
            if data:
                market_data[symbol] = data
        
        return market_data
    
    def run_technical_analysis(self, market_data):
        """Run technical analysis"""
        # Placeholder for now
        return {'status': 'pending_implementation'}
    
    def analyze_portfolio_correlations(self, market_data):
        """Analyze portfolio correlations"""
        # Placeholder for now
        return {'status': 'pending_implementation'}
    
    async def analyze_news_sentiment(self):
        """Analyze news sentiment"""
        # Placeholder for now
        return {'status': 'pending_implementation'}
    
    def format_portfolio_summary(self):
        return f"Stocks: {len(self.portfolio.get('stocks', []))}"
    
    def format_market_analysis(self):
        return "Market analysis pending implementation"
    
    def format_risk_alerts(self):
        return "Risk analysis pending implementation"
    
    def format_ai_recommendations(self, responses):
        return f"Processed {len(responses)} questions"
    
    def format_prediction_accuracy(self, validation_results):
        return "Prediction tracking pending implementation"
    
    def format_action_items(self, responses):
        return "Action items pending implementation"
    
    def get_historical_accuracy(self):
        return 0  # Placeholder
    
    async def process_daily_analysis(self):
        """Main daily analysis pipeline"""
        print("📊 Starting Daily Analysis...")
        
        # 1. Load pending questions
        questions = self.load_pending_questions()
        print(f"📧 Found {len(questions)} pending questions")
        
        # 2. Fetch market data
        market_data = await self.fetch_all_market_data()
        print(f"📈 Fetched data for {len(market_data)} symbols")
        
        # 3. Run technical analysis
        technical_signals = self.run_technical_analysis(market_data)
        
        # 4. Check correlations
        correlation_risks = self.analyze_portfolio_correlations(market_data)
        
        # 5. Get news and sentiment
        news_sentiment = await self.analyze_news_sentiment()
        
        # 6. Process each question with AI (simplified for now)
        responses = []
        if self.components.get('llm') and questions:
            for question in questions[:3]:  # Limit to 3 for testing
                try:
                    # Simple query for now
                    prompt = f"Financial question: {question['content']}"
                    response = self.llm.query_groq(prompt)
                    
                    responses.append({
                        'question': question,
                        'analysis': response or "Analysis pending",
                        'timestamp': datetime.now().isoformat()
                    })
                    
                    # Mark as processed
                    question['status'] = 'processed'
                except Exception as e:
                    print(f"Error processing question: {e}")
        
        # 7. Generate report
        report = self.generate_report(responses, {})
        print("\n📄 Report Generated:")
        print(report[:500] + "..." if len(report) > 500 else report)
        
        return {'processed': len(responses), 'status': 'success'}
    
    def generate_report(self, responses, validation_results):
        """Create comprehensive email report"""
        report = f"""
        📊 DAILY FINANCIAL AI ANALYSIS REPORT
        =====================================
        Date: {datetime.now().strftime('%Y-%m-%d')}
        
        🎯 PORTFOLIO SUMMARY
        -------------------
        {self.format_portfolio_summary()}
        
        📈 MARKET ANALYSIS
        -----------------
        {self.format_market_analysis()}
        
        ⚠️ RISK ALERTS
        --------------
        {self.format_risk_alerts()}
        
        🤖 AI RECOMMENDATIONS
        --------------------
        {self.format_ai_recommendations(responses)}
        
        📊 PREDICTION ACCURACY
        ---------------------
        {self.format_prediction_accuracy(validation_results)}
        
        🎯 ACTION ITEMS
        --------------
        {self.format_action_items(responses)}
        
        ---
        Components Status: {sum(1 for v in self.components.values() if v)}/{len(self.components)} active
        """
        return report
    
    def run_backtest(self):
        """Run backtesting"""
        print("🔄 Backtesting not yet implemented")
        
    def monitor_portfolio(self):
        """Monitor portfolio"""
        print("👁️ Portfolio monitoring not yet implemented")

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Financial AI Advisor')
    parser.add_argument('--mode', 
                       choices=['test', 'analysis', 'backtest', 'monitor'],
                       default='test',
                       help='Operation mode')
    
    args = parser.parse_args()
    
    if args.mode == 'test':
        # Run system test
        test_system()
    else:
        # Run full advisor
        advisor = FinancialAIAdvisor()
        
        if args.mode == 'analysis':
            asyncio.run(advisor.process_daily_analysis())
        elif args.mode == 'backtest':
            advisor.run_backtest()
        elif args.mode == 'monitor':
            advisor.monitor_portfolio()
