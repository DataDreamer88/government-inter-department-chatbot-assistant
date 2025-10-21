# backend/chatbot/query_processor.py
import re
from typing import Dict, List
import json

class QueryProcessor:
    """Process and understand user queries"""
    
    # Common state names in India
    INDIAN_STATES = [
        'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
        'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka',
        'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
        'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu',
        'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal'
    ]
    
    # Common crop names
    COMMON_CROPS = [
        'Rice', 'Wheat', 'Maize', 'Jowar', 'Bajra', 'Ragi', 'Barley',
        'Cotton', 'Jute', 'Sugarcane', 'Groundnut', 'Soybean', 'Sunflower',
        'Coconut', 'Arecanut', 'Tea', 'Coffee', 'Rubber'
    ]
    
    @staticmethod
    def extract_states(query: str) -> List[str]:
        """Extract state names from query"""
        query_lower = query.lower()
        found_states = []
        
        for state in QueryProcessor.INDIAN_STATES:
            if state.lower() in query_lower:
                found_states.append(state)
        
        return found_states
    
    @staticmethod
    def extract_crops(query: str) -> List[str]:
        """Extract crop names from query"""
        query_lower = query.lower()
        found_crops = []
        
        for crop in QueryProcessor.COMMON_CROPS:
            if crop.lower() in query_lower:
                found_crops.append(crop)
        
        return found_crops
    
    @staticmethod
    def extract_years(query: str) -> List[int]:
        """Extract years from query"""
        # Match 4-digit years
        years = re.findall(r'\b(19|20)\d{2}\b', query)
        return [int(year) for year in years]
    
    @staticmethod
    def extract_numbers(query: str) -> List[int]:
        """Extract numbers from query (for N years, M crops, etc.)"""
        numbers = re.findall(r'\b\d+\b', query)
        return [int(num) for num in numbers if len(num) <= 2]
    
    @staticmethod
    def determine_query_type(query: str) -> str:
        """Determine the type of query"""
        query_lower = query.lower()
        
        # Check for keywords
        if any(word in query_lower for word in ['compare', 'comparison', 'versus', 'vs']):
            return 'comparison'
        elif any(word in query_lower for word in ['trend', 'over time', 'decade', 'years']):
            return 'trend_analysis'
        elif any(word in query_lower for word in ['correlate', 'correlation', 'relationship', 'impact']):
            return 'correlation'
        elif any(word in query_lower for word in ['policy', 'recommend', 'argument', 'support']):
            return 'policy_analysis'
        elif any(word in query_lower for word in ['highest', 'lowest', 'maximum', 'minimum', 'top', 'best']):
            return 'ranking'
        elif any(word in query_lower for word in ['rainfall', 'rain', 'precipitation']):
            if any(word in query_lower for word in ['crop', 'production', 'agriculture']):
                return 'climate_agriculture_correlation'
            else:
                return 'climate_query'
        elif any(word in query_lower for word in ['crop', 'production', 'yield', 'agriculture']):
            return 'agriculture_query'
        else:
            return 'general_query'
    
    @staticmethod
    def parse_query(query: str) -> Dict:
        """
        Parse query and extract all relevant information
        
        Args:
            query: User query string
            
        Returns:
            Dictionary with parsed information
        """
        return {
            'original_query': query,
            'query_type': QueryProcessor.determine_query_type(query),
            'states': QueryProcessor.extract_states(query),
            'crops': QueryProcessor.extract_crops(query),
            'years': QueryProcessor.extract_years(query),
            'numbers': QueryProcessor.extract_numbers(query)
        }