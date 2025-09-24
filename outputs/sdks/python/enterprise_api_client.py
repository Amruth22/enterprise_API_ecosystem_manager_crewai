# Enterprise API Python SDK
import requests
import json
from typing import Dict, List, Optional

class EnterpriseAPIClient:
    def __init__(self, base_url: str, api_key: str):
        """
        Initialize the Enterprise API client.

        Args:
            base_url (str): The base URL of the API
            api_key (str): Your API key for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

    def _make_request(self, method: str, endpoint: str, data: Dict = None) -> Dict:
        """
        Make an HTTP request to the API.

        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE)
            endpoint (str): API endpoint
            data (Dict, optional): Request data for POST/PUT requests

        Returns:
            Dict: API response
        """
        url = f"{self.base_url}{endpoint}"

        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=self.headers)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=self.headers, json=data)
            elif method.upper() == 'PUT':
                response = requests.put(url, headers=self.headers, json=data)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=self.headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json() if response.content else {}

        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")

        def list_deploy(self, limit: int = 20, offset: int = 0) -> List[Dict]:
        """
        List deploy.

        Args:
            limit (int): Maximum number of items to return
            offset (int): Offset for pagination

        Returns:
            List[Dict]: List of deploy
        """
        params = {'limit': limit, 'offset': offset}
        # In a real implementation, you would pass params to the request
        return self._make_request('GET', '/agent/deploy')

    def create_deploy(self, data: Dict) -> Dict:
        """
        Create a new deploy.

        Args:
            data (Dict): Deploy data

        Returns:
            Dict: Created deploy data
        """
        return self._make_request('POST', '/agent/deploy', data)

        def get_statu(self, statu_id: str) -> Dict:
        """
        Get a specific statu by ID.

        Args:
            statu_id (str): The statu ID

        Returns:
            Dict: Statu data
        """
        return self._make_request('GET', f'/agent/status/{agent_id}{statu_id}')

    def update_statu(self, statu_id: str, data: Dict) -> Dict:
        """
        Update a specific statu.

        Args:
            statu_id (str): The statu ID
            data (Dict): Updated statu data

        Returns:
            Dict: Updated status data
        """
        return self._make_request('PUT', f'/agent/status/{agent_id}{statu_id}', data)

    def delete_statu(self, statu_id: str) -> bool:
        """
        Delete a specific statu.

        Args:
            statu_id (str): The statu ID

        Returns:
            bool: True if deleted successfully
        """
        self._make_request('DELETE', f'/agent/status/{agent_id}{statu_id}')
        return True
        def list_message(self, limit: int = 20, offset: int = 0) -> List[Dict]:
        """
        List message.

        Args:
            limit (int): Maximum number of items to return
            offset (int): Offset for pagination

        Returns:
            List[Dict]: List of message
        """
        params = {'limit': limit, 'offset': offset}
        # In a real implementation, you would pass params to the request
        return self._make_request('GET', '/queue/message')

    def create_message(self, data: Dict) -> Dict:
        """
        Create a new message.

        Args:
            data (Dict): Message data

        Returns:
            Dict: Created message data
        """
        return self._make_request('POST', '/queue/message', data)


# Usage example:
# client = EnterpriseAPIClient("https://api.example.com/v1", "your-api-key")
# users = client.list_users(limit=10)
# new_user = client.create_user({"name": "John Doe", "email": "john@example.com"})