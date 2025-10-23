# src/ai_models/prediction_tracker.py
import json
from datetime import datetime, timedelta
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

class PredictionTracker:
    def __init__(self):
        self.predictions_file = 'data/predictions/history.json'
        self.performance_metrics = {}
    
    def log_prediction(self, prediction_data):
        """Store prediction for future validation"""
        prediction = {
            'id': datetime.now().isoformat(),
            'symbol': prediction_data['symbol'],
            'action': prediction_data['action'],
            'price_at_prediction': prediction_data['current_price'],
            'target_price': prediction_data['target_price'],
            'timeframe': prediction_data['timeframe'],
            'confidence': prediction_data['confidence'],
            'validation_date': (datetime.now() + timedelta(days=prediction_data['timeframe'])).isoformat(),
            'validated': False,
            'outcome': None
        }
        
        with open(self.predictions_file, 'a') as f:
            json.dump(prediction, f)
            f.write('\n')
    
    def validate_predictions(self):
        """Check past predictions against actual outcomes"""
        validated = []
        
        with open(self.predictions_file, 'r') as f:
            predictions = [json.loads(line) for line in f]
        
        for pred in predictions:
            if not pred['validated'] and datetime.fromisoformat(pred['validation_date']) <= datetime.now():
                actual_price = self._get_current_price(pred['symbol'])
                
                # Determine if prediction was correct
                if pred['action'] == 'BUY':
                    success = actual_price > pred['price_at_prediction'] * 1.02
                elif pred['action'] == 'SELL':
                    success = actual_price < pred['price_at_prediction'] * 0.98
                else:  # HOLD
                    success = abs(actual_price - pred['price_at_prediction']) / pred['price_at_prediction'] < 0.05
                
                pred['validated'] = True
                pred['outcome'] = 'SUCCESS' if success else 'FAILURE'
                pred['actual_price'] = actual_price
                pred['return_pct'] = (actual_price - pred['price_at_prediction']) / pred['price_at_prediction'] * 100
                
                validated.append(pred)
        
        self._update_model_weights(validated)
        return validated
    
    def _update_model_weights(self, validated_predictions):
        """Adjust LLM weights based on performance"""
        model_performance = {}
        
        for pred in validated_predictions:
            model = pred.get('primary_model')
            if model:
                if model not in model_performance:
                    model_performance[model] = {'correct': 0, 'total': 0}
                
                model_performance[model]['total'] += 1
                if pred['outcome'] == 'SUCCESS':
                    model_performance[model]['correct'] += 1
        
        # Update weights based on accuracy
        new_weights = {}
        for model, perf in model_performance.items():
            accuracy = perf['correct'] / perf['total'] if perf['total'] > 0 else 0.5
            new_weights[model] = accuracy
        
        # Normalize weights
        total = sum(new_weights.values())
        for model in new_weights:
            new_weights[model] /= total
        
        return new_weights
