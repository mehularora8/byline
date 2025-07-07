import requests
import logging
from datetime import datetime, timedelta
from typing import Dict, Any

class ExaSearch:
    """Simple class to interact with Exa search API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.exa.ai/search"
        self.headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }
        logging.info(f"ExaSearch initialized with API key: {api_key[:8]}...")
    
    def search(self, query: str, num_results: int = 10, text: bool = True) -> Dict[str, Any]:
        """Search using Exa API"""
        logging.info(f"ExaSearch.search called with query: '{query}', num_results: {num_results}")
        
        payload = {
            "query": query,
            "numResults": num_results,
            "text": text
        }
        
        payload["startPublishedDate"] = (datetime.now() - timedelta(days=1)).isoformat()
        payload["endPublishedDate"] = datetime.now().isoformat()
        
        logging.info(f"Sending request to Exa API with payload: {payload}")
        
        response = requests.post(
            self.base_url,
            headers=self.headers,
            json=payload
        )
        
        if response.status_code == 200:
            result = response.json()
            logging.info(f"Exa search successful, got {len(result.get('results', []))} results")
            return result
        else:
            error_msg = f"Exa search failed: {response.status_code} - {response.text}"
            logging.error(error_msg)
            raise Exception(error_msg)

