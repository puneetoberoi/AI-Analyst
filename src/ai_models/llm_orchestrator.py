# src/ai_models/llm_orchestrator.py
from groq import Groq
import google.generativeai as genai
import cohere
import os

class LLMOrchestrator:
    def __init__(self):
        # Fix Groq initialization - remove proxies argument
        try:
            self.groq_client = Groq(
                api_key=os.environ.get('GROQ_API_KEY', '')
            )
            print("✅ Groq initialized")
        except TypeError:
            # Fallback for older version
            try:
                from groq import Client as GroqClient
                self.groq_client = GroqClient(
                    api_key=os.environ.get('GROQ_API_KEY', '')
                )
                print("✅ Groq initialized (legacy)")
            except:
                self.groq_client = None
                print("⚠️ Groq not available")
        
        # Initialize Gemini
        genai.configure(api_key=os.environ.get('GEMINI_API_KEY', ''))
        self.gemini_model = genai.GenerativeModel('gemini-pro')
        
        # Initialize Cohere
        self.cohere_client = cohere.Client(
            api_key=os.environ.get('COHERE_API_KEY', '')
        )
    
    def query_groq(self, prompt, model="llama3-8b-8192"):
        """Query Groq with error handling"""
        if not self.groq_client:
            return None
            
        try:
            completion = self.groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a financial analyst."},
                    {"role": "user", "content": prompt}
                ],
                model=model,
                temperature=0.7,
                max_tokens=1000
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Groq error: {e}")
            return None
