# src/ai_models/consensus_engine.py
from groq import Groq
import google.generativeai as genai
import cohere
from typing import List, Dict
import json

class ConsensusEngine:
    def __init__(self, groq_key, gemini_key, cohere_key):
        self.groq = Groq(api_key=groq_key)
        self.gemini = genai.configure(api_key=gemini_key)
        self.cohere = cohere.Client(cohere_key)
        self.weights = {'groq': 0.4, 'gemini': 0.35, 'cohere': 0.25}
    
    async def get_consensus_analysis(self, question, market_data, portfolio):
        """Get analysis from multiple LLMs and create consensus"""
        
        prompt = self._build_analysis_prompt(question, market_data, portfolio)
        
        # Parallel LLM calls with fallback
        responses = {}
        
        try:
            responses['groq'] = await self._groq_analysis(prompt)
        except Exception as e:
            print(f"Groq failed: {e}")
            responses['groq'] = None
        
        try:
            responses['gemini'] = await self._gemini_analysis(prompt)
        except Exception as e:
            print(f"Gemini failed: {e}")
            responses['gemini'] = None
        
        try:
            responses['cohere'] = await self._cohere_analysis(prompt)
        except Exception as e:
            print(f"Cohere failed: {e}")
            responses['cohere'] = None
        
        # Create weighted consensus
        consensus = self._build_consensus(responses)
        
        return {
            'individual_responses': responses,
            'consensus': consensus,
            'confidence': self._calculate_confidence(responses)
        }
    
    def _build_consensus(self, responses):
        """Aggregate recommendations with confidence scoring"""
        recommendations = {
            'buy': 0, 'sell': 0, 'hold': 0,
            'reasons': [],
            'risk_factors': [],
            'opportunities': []
        }
        
        for model, response in responses.items():
            if response:
                weight = self.weights.get(model, 0.33)
                action = response.get('action', 'hold').lower()
                recommendations[action] += weight
                recommendations['reasons'].extend(response.get('reasons', []))
                recommendations['risk_factors'].extend(response.get('risks', []))
        
        # Determine final recommendation
        final_action = max(recommendations, key=lambda x: recommendations[x] if x in ['buy', 'sell', 'hold'] else 0)
        
        return {
            'action': final_action.upper(),
            'confidence': recommendations[final_action],
            'reasoning': list(set(recommendations['reasons']))[:5],
            'risks': list(set(recommendations['risk_factors']))[:3]
        }
