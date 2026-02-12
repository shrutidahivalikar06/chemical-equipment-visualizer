# api_client.py
import requests
import json
import pandas as pd
from typing import Optional, Dict, Any


class EquipmentAPIClient:
    """Client for Django backend API"""
    
    def __init__(self, base_url: str = "http://127.0.0.1:8000/api"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def upload_csv(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Upload CSV file to backend"""
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (file_path.split('/')[-1], f, 'text/csv')}
                response = self.session.post(
                    f"{self.base_url}/upload/",
                    files=files
                )
                response.raise_for_status()
                return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Upload error: {e}")
            return None
    
    def get_summary(self) -> Optional[Dict[str, Any]]:
        """Get equipment summary statistics"""
        try:
            response = self.session.get(f"{self.base_url}/summary/")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Summary error: {e}")
            return None
    
    def get_history(self) -> Optional[Dict[str, Any]]:
        """Get upload history"""
        try:
            response = self.session.get(f"{self.base_url}/history/")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"History error: {e}")
            return None
    
    def generate_pdf(self, save_path: str) -> bool:
        """Generate and download PDF report"""
        try:
            response = self.session.get(
                f"{self.base_url}/generate-pdf/",
                stream=True
            )
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        except requests.exceptions.RequestException as e:
            print(f"PDF generation error: {e}")
            return False
    
    def download_summary_json(self, save_path: str) -> bool:
        """Download summary as JSON"""
        try:
            summary = self.get_summary()
            if summary:
                with open(save_path, 'w') as f:
                    json.dump(summary, f, indent=2)
                return True
            return False
        except Exception as e:
            print(f"JSON download error: {e}")
            return False


# Utility functions for desktop app
def load_sample_data() -> pd.DataFrame:
    """Load sample equipment data for testing"""
    sample_data = {
        'equipment_name': [
            'Compressor-A-101', 'Separator-E-102', 'Distillation-Column-D-103',
            'Valve-G-104', 'Compressor-G-105', 'Heat-Exchanger-A-106',
            'Mixer-D-107', 'Distillation-Column-D-108', 'Reactor-D-109',
            'Pump-A-110'
        ],
        'equipment_type': [
            'Compressor', 'Separator', 'Distillation Column',
            'Valve', 'Compressor', 'Heat Exchanger',
            'Mixer', 'Distillation Column', 'Reactor',
            'Pump'
        ],
        'flowrate': [81.1, 119.4, 183.8, 113.4, 88.6, 211.9, 115.0, 170.5, 142.3, 102.0],
        'pressure': [9.4, 2.4, 1.7, 3.9, 9.1, 5.8, 3.4, 1.7, 4.2, 2.8],
        'temperature': [114.3, 43.0, 69.0, 63.3, 113.9, 99.3, 63.0, 85.1, 91.0, 48.5],
        'status': ['Active'] * 10,
        'location': ['Unit A'] * 5 + ['Unit B'] * 5,
        'purchase_year': [2019, 2020, 2018, 2021, 2019, 2020, 2021, 2018, 2019, 2020],
        'condition': ['Good'] * 7 + ['Excellent'] * 3
    }
    return pd.DataFrame(sample_data)