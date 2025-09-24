// Register a new agent
const url = "http://localhost:8000/agents";
const data = {
  agent_id: "research_agent_001",
  agent_type: "research"
};

fetch(url, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(data)
})
.then(response => response.json())
.then(data => console.log(data));

// Assign a task to an agent
const taskUrl = "http://localhost:8000/tasks";
const taskData = {
  agent_id: "research_agent_001",
  task_description: "Analyze the sentiment of a given text.",
  task_data: {text: "This is a great product!"}
};

fetch(taskUrl, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(taskData)
})
.then(response => response.json())
.then(data => console.log(data));

// Retrieve results for an agent
const resultsUrl = "http://localhost:8000/results/research_agent_001";

fetch(resultsUrl)
  .then(response => response.json())
  .then(data => console.log(data));
```

## 5. SDKs

### Python SDK

```python
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
    

# Usage example:
# client = EnterpriseAPIClient("https://api.example.com/v1", "your-api-key")
# users = client.list_users(limit=10)
# new_user = client.create_user({"name": "John Doe", "email": "john@example.com"})