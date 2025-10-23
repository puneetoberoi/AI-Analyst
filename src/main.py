# src/main.py
import asyncio
from datetime import datetime
import json
import argparse

class FinancialAIAdvisor:
    def __init__(self):
        self.load_config()
        self.initialize_components()
    
    async def process_daily_analysis(self):
        """Main daily analysis pipeline"""
        
        # 1. Load pending questions
        questions = self.load_pending_questions()
        
        # 2. Fetch market data
        market_data = await self.fetch_all_market_data()
        
        # 3. Run technical analysis
        technical_signals = self.run_technical_analysis(market_data)
        
        # 4. Check correlations
        correlation_risks = self.analyze_portfolio_correlations(market_data)
        
        # 5. Get news and sentiment
        news_sentiment = await self.analyze_news_sentiment()
        
        # 6. Process each question with AI
        responses = []
        for question in questions:
            analysis = await self.consensus_engine.get_consensus_analysis(
                question=question,
                market_data={
                    'technical': technical_signals,
                    'correlations': correlation_risks,
                    'news': news_sentiment,
                    'portfolio': self.portfolio
                },
                portfolio=self.portfolio
            )
            
            # Log prediction for learning
            self.prediction_tracker.log_prediction(analysis)
            
            responses.append({
                'question': question,
                'analysis': analysis,
                'timestamp': datetime.now().isoformat()
            })
        
        # 7. Validate past predictions
        validation_results = self.prediction_tracker.validate_predictions()
        
        # 8. Generate and send report
        report = self.generate_report(responses, validation_results)
        self.send_email_report(report)
        
        # 9. Update cache and knowledge base
        self.update_knowledge_base(responses, validation_results)
        
        return {'processed': len(questions), 'status': 'success'}
    
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
        This analysis considered {len(self.data_sources)} data sources
        Consensus from {len(self.llm_models)} AI models
        Historical accuracy: {self.get_historical_accuracy()}%
        """
        return report

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['analysis', 'backtest', 'monitor'])
    args = parser.parse_args()
    
    advisor = FinancialAIAdvisor()
    
    if args.mode == 'analysis':
        asyncio.run(advisor.process_daily_analysis())
    elif args.mode == 'backtest':
        advisor.run_backtest()
    elif args.mode == 'monitor':
        advisor.monitor_portfolio()
