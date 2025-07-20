import os
import requests

class MapBox:
    def __init__(self):
        self.token = os.getenv('MAP_BOX_PUB_TOKEN')

    def get_location(self, address: str) -> dict:        
        if not self.token:
            return {
                'error': 'MapBox token not configured',
                'features': []
            }
        
        try:
            url = f'https://api.mapbox.com/search/searchbox/v1/forward?access_token={self.token}&q={address}&limit=1'
            response = requests.get(url)
                
            # Check if the request was successful
            if response.status_code != 200:
                return {
                    'error': f'API request failed with status code: {response.status_code}',
                    'features': []
                }

            
            # Try to parse JSON
            try:
                return response.json()
            except requests.exceptions.JSONDecodeError as e:
                return {
                    'error': f'Invalid JSON response: {str(e)}',
                    'features': []
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'error': f'Request failed: {str(e)}',
                'features': []
            }
    
    def get_coordinates(self, address: str) -> tuple:
        location = self.get_location(address)
        if 'error' in location:
            return (None, None)
        
        if not location.get('features') or len(location['features']) == 0:
            return (None, None)
        
        try:
            coordinates = location['features'][0]['geometry']['coordinates']
            return tuple(coordinates)
        except (KeyError, IndexError) as e:
            return (None, None)
    