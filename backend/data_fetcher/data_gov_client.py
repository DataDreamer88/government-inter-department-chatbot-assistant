# backend/data_fetcher/data_gov_client.py
import requests
from typing import Dict, List, Optional
from config import Config

class DataGovClient:
    """Client for interacting with data.gov.in API"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or Config.DATA_GOV_API_KEY
        self.base_url = Config.DATA_GOV_BASE_URL

        # Correct resource IDs as per your images
        self.RESOURCE_IDS = {
            'crop_production': '35be999b-0208-4354-b557-f6ca9a5355de',  # District-wise crop production statistics
            'rainfall': '8e0bd482-4aba-4d99-9cb9-ff124f6f1c2f',        # Sub Divisional Monthly Rainfall
        }

    def fetch_data(self, resource_id: str, filters: Dict = None, limit: int = 100, offset: int = 0) -> Dict:
        """
        Fetch data from data.gov.in API

        Args:
            resource_id: Resource ID from data.gov.in
            filters: Dictionary of filters to apply
            limit: Number of records to fetch
            offset: Offset for pagination
            
        Returns:
            Dictionary containing API response
        """
        url = f"{self.base_url}{resource_id}"

        params = {
            'api-key': self.api_key,
            'format': 'json',
            'offset': offset,
            'limit': limit
        }

        # Add filters if provided
        if filters:
            for key, value in filters.items():
                params[f'filters[{key}]'] = value

        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return {'records': [], 'error': str(e)}

    def fetch_crop_production(self, state: str = None, district: str = None, crop: str = None, year: str = None) -> List[Dict]:
        """Fetch crop production data with filters"""
        filters = {}
        if state:
            filters['State Name'] = state
        if district:
            filters['District Name'] = district
        if crop:
            filters['Crop'] = crop
        if year:
            filters['Crop Year'] = year
            
        result = self.fetch_data(self.RESOURCE_IDS['crop_production'], filters, limit=1000)
        print("Raw crop data result - first record:", result.get('records', [None])[0])
        return result.get('records', [])

    def fetch_rainfall_data(self, subdivision: str = None, year: str = None) -> List[Dict]:
        """Fetch rainfall data with filters"""
        filters = {}
        if subdivision:
            filters['SUBDIVISION'] = subdivision
        if year:
            filters['YEAR'] = year
            
        result = self.fetch_data(self.RESOURCE_IDS['rainfall'], filters, limit=1000)
        print("Raw rainfall data result - first record:", result.get('records', [None])[0])
        return result.get('records', [])

    def search_resources(self, query: str) -> List[Dict]:
        search_url = "https://api.data.gov.in/catalog/search"
        params = {
            'api-key': self.api_key,
            'format': 'json',
            'q': query
        }
        try:
            response = requests.get(search_url, params=params, timeout=30)
            response.raise_for_status()
            return response.json().get('results', [])
        except requests.exceptions.RequestException as e:
            print(f"Error searching resources: {e}")
            return []
