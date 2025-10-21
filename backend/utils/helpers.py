# backend/utils/helpers.py
import json
from datetime import datetime
from typing import Any, Dict

def format_timestamp() -> str:
    """Get current timestamp in ISO format"""
    return datetime.now().isoformat()

def safe_json_dumps(data: Any) -> str:
    """Safely convert data to JSON string"""
    try:
        return json.dumps(data, indent=2, default=str)
    except Exception as e:
        return json.dumps({'error': str(e)})

def validate_api_key(api_key: str) -> bool:
    """Validate API key format"""
    return api_key and len(api_key) > 10

def extract_year_range(query: str) -> tuple:
    """Extract year range from query"""
    import re
    years = re.findall(r'\b(19|20)\d{2}\b', query)
    if len(years) >= 2:
        return (int(years[0]), int(years[-1]))
    elif len(years) == 1:
        return (int(years[0]), int(years[0]))
    return (None, None)