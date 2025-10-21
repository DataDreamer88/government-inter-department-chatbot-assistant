# backend/chatbot/llm_handler.py
from groq import Groq
from openai import OpenAI
from typing import List, Dict
from config import Config

class LLMHandler:
    """Handle LLM interactions using Groq or OpenAI"""
    
    def __init__(self, provider: str = None, model: str = None):
        """
        Initialize LLM handler
        
        Args:
            provider: 'groq' or 'openai'
            model: Model name
        """
        self.provider = provider or Config.LLM_PROVIDER
        self.model = model or Config.LLM_MODEL
        
        if self.provider == 'groq':
            self.client = Groq(api_key=Config.GROQ_API_KEY)
        elif self.provider == 'openai':
            self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
            self.model = 'gpt-3.5-turbo'
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
        
        print(f"LLM Handler initialized: {self.provider} - {self.model}")
    
    def generate_response(self, prompt: str, context: str = "", 
                         temperature: float = 0.3, max_tokens: int = 1024) -> str:
        """
        Generate response from LLM
        
        Args:
            prompt: User query
            context: Retrieved context from RAG
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            
        Returns:
            Generated response text
        """
        system_prompt = """You are Samarth, an intelligent agricultural data assistant. 
Your role is to help policymakers, researchers, and farmers understand India's agricultural 
economy and climate patterns using official government data from data.gov.in.

Guidelines:
1. Answer questions accurately using ONLY the provided context
2. Always cite your sources explicitly
3. If information is not in the context, clearly state that
4. Provide numerical data with appropriate units
5. When making comparisons, be specific and quantitative
6. Format responses clearly with bullet points when appropriate
7. For trends, mention the time period covered in the data

Remember: You are working with real government data. Accuracy and traceability are paramount."""

        user_message = f"""Context from data.gov.in:
{context}

Question: {prompt}

Please provide a detailed, data-backed answer with specific citations to the sources."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        try:
            if self.provider == 'groq':
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
            else:  # openai
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
            
            return response.choices[0].message.content
        
        except Exception as e:
            print(f"Error generating response: {e}")
            return f"I apologize, but I encountered an error: {str(e)}"
    
    def extract_query_intent(self, query: str) -> Dict:
        """
        Extract intent and entities from user query
        
        Args:
            query: User query
            
        Returns:
            Dictionary with intent and entities
        """
        prompt = f"""Analyze the following agricultural query and extract:
1. Primary intent (e.g., compare, analyze, find, list)
2. Entities mentioned (states, districts, crops, years, climate data)
3. Query type (crop_production, rainfall, correlation, policy_analysis)

Query: {query}

Respond in this exact format:
INTENT: [intent]
ENTITIES: [comma-separated list]
TYPE: [type]"""

        messages = [
            {"role": "system", "content": "You are a query analyzer for agricultural data."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            if self.provider == 'groq':
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.1,
                    max_tokens=200
                )
            else:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.1,
                    max_tokens=200
                )
            
            result = response.choices[0].message.content
            
            # Parse response
            intent_data = {
                'intent': '',
                'entities': [],
                'type': ''
            }
            
            for line in result.split('\n'):
                if line.startswith('INTENT:'):
                    intent_data['intent'] = line.split(':', 1)[1].strip()
                elif line.startswith('ENTITIES:'):
                    entities = line.split(':', 1)[1].strip()
                    intent_data['entities'] = [e.strip() for e in entities.split(',')]
                elif line.startswith('TYPE:'):
                    intent_data['type'] = line.split(':', 1)[1].strip()
            
            return intent_data
        
        except Exception as e:
            print(f"Error extracting intent: {e}")
            return {'intent': 'unknown', 'entities': [], 'type': 'general'}