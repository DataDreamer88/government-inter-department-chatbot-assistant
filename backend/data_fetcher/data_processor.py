# backend/data_fetcher/data_processor.py
import pandas as pd
from typing import List, Dict

class DataProcessor:
    """Process and clean data from data.gov.in"""

    @staticmethod
    def clean_crop_data(data: List[Dict]) -> pd.DataFrame:
        """Clean and standardize crop production data"""
        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data)

        # Exact column names from API
        column_mapping = {
            'state_name': 'state',
            'district_name': 'district',
            'crop_year': 'year',
            'season': 'season',
            'crop': 'crop',
            'area_': 'area_hectares',
            'production_': 'production_tonnes'
        }

        df = df.rename(columns=column_mapping)

        # Convert numeric columns
        numeric_cols = ['area_hectares', 'production_tonnes', 'year']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Calculate yield
        if 'area_hectares' in df.columns and 'production_tonnes' in df.columns:
            df['yield_tonnes_per_hectare'] = df['production_tonnes'] / df['area_hectares']

        # Clean text columns
        text_cols = ['state', 'district', 'crop', 'season']
        for col in text_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip().str.title()

        return df.dropna(subset=['state', 'crop'])

    @staticmethod
    def clean_rainfall_data(data: List[Dict]) -> pd.DataFrame:
        """Clean and standardize rainfall data"""
        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data)

        column_mapping = {
            'SUBDIVISION': 'subdivision',
            'YEAR': 'year',
            'JAN': 'jan', 'FEB': 'feb', 'MAR': 'mar', 'APR': 'apr',
            'MAY': 'may', 'JUN': 'jun', 'JUL': 'jul', 'AUG': 'aug',
            'SEP': 'sep', 'OCT': 'oct', 'NOV': 'nov', 'DEC': 'dec',
            'ANNUAL': 'annual',
            'JF': 'jf', 'MAM': 'mam', 'JJAS': 'jjas', 'OND': 'ond'
        }
        df = df.rename(columns=column_mapping)

        month_cols = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec', 'annual']
        for col in month_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        if 'year' in df.columns:
            df['year'] = pd.to_numeric(df['year'], errors='coerce')
        return df.dropna(subset=['subdivision', 'year'])

    # Keep your other aggregation and formatting methods as they are.

    
    @staticmethod
    def aggregate_crop_by_state(df: pd.DataFrame, years: int = 5) -> pd.DataFrame:
        """Aggregate crop production by state for recent years"""
        recent_years = df['year'].max() - years + 1
        df_recent = df[df['year'] >= recent_years]
        
        agg_df = df_recent.groupby(['state', 'crop']).agg({
            'production_tonnes': 'sum',
            'area_hectares': 'sum',
            'year': 'count'
        }).reset_index()
        
        agg_df.columns = ['state', 'crop', 'total_production', 'total_area', 'num_records']
        agg_df['avg_yield'] = agg_df['total_production'] / agg_df['total_area']
        
        return agg_df.sort_values('total_production', ascending=False)
    
    @staticmethod
    def calculate_rainfall_statistics(df: pd.DataFrame, years: int = 10) -> pd.DataFrame:
        """Calculate rainfall statistics for recent years"""
        recent_years = df['year'].max() - years + 1
        df_recent = df[df['year'] >= recent_years]
        
        stats_df = df_recent.groupby('subdivision').agg({
            'annual': ['mean', 'std', 'min', 'max']
        }).reset_index()
        
        stats_df.columns = ['subdivision', 'avg_rainfall', 'std_rainfall', 'min_rainfall', 'max_rainfall']
        
        return stats_df.sort_values('avg_rainfall', ascending=False)
    
    @staticmethod
    def format_for_embedding(df: pd.DataFrame, data_type: str) -> List[Dict]:
        """
        Format data for embedding generation
        
        Args:
            df: Cleaned dataframe
            data_type: 'crop' or 'rainfall'
            
        Returns:
            List of dictionaries with text and metadata
        """
        documents = []
        
        if data_type == 'crop':
            for _, row in df.iterrows():
                text = f"In {row.get('state', 'Unknown')}, {row.get('district', 'Unknown')} district, "\
                       f"{row.get('crop', 'Unknown')} crop production was {row.get('production_tonnes', 0):.2f} tonnes "\
                       f"from {row.get('area_hectares', 0):.2f} hectares in year {row.get('year', 'Unknown')} "\
                       f"during {row.get('season', 'Unknown')} season. "\
                       f"Yield was {row.get('yield_tonnes_per_hectare', 0):.2f} tonnes per hectare."
                
                documents.append({
                    'text': text,
                    'metadata': {
                        'type': 'crop_production',
                        'state': row.get('state'),
                        'district': row.get('district'),
                        'crop': row.get('crop'),
                        'year': row.get('year'),
                        'season': row.get('season'),
                        'source': 'data.gov.in - Ministry of Agriculture'
                    }
                })
        
        elif data_type == 'rainfall':
            for _, row in df.iterrows():
                text = f"In {row.get('subdivision', 'Unknown')}, the annual rainfall was "\
                       f"{row.get('annual', 0):.2f} mm in year {row.get('year', 'Unknown')}. "\
                       f"Monthly rainfall: January {row.get('jan', 0):.2f} mm, "\
                       f"February {row.get('feb', 0):.2f} mm, March {row.get('mar', 0):.2f} mm, "\
                       f"April {row.get('apr', 0):.2f} mm, May {row.get('may', 0):.2f} mm, "\
                       f"June {row.get('jun', 0):.2f} mm, July {row.get('jul', 0):.2f} mm, "\
                       f"August {row.get('aug', 0):.2f} mm, September {row.get('sep', 0):.2f} mm, "\
                       f"October {row.get('oct', 0):.2f} mm, November {row.get('nov', 0):.2f} mm, "\
                       f"December {row.get('dec', 0):.2f} mm."
                
                documents.append({
                    'text': text,
                    'metadata': {
                        'type': 'rainfall',
                        'subdivision': row.get('subdivision'),
                        'year': row.get('year'),
                        'source': 'data.gov.in - India Meteorological Department'
                    }
                })
        
        return documents