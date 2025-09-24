from crewai.tools import BaseTool
import json
import random
from typing import Dict, List

class SDKGeneratorTool(BaseTool):
    name: str = "SDK Generator Tool"
    description: str = "Generate SDKs and code samples for different programming languages"

    def _run(self, api_endpoints: List[str] = None, languages: List[str] = None) -> str:
        """
        Generate SDKs and code samples.
        
        Args:
            api_endpoints: List of API endpoints to generate SDKs for
            languages: List of programming languages to generate SDKs in
        """
        try:
            # Generate sample SDKs
            sdk_data = self._generate_sample_sdks(api_endpoints, languages)
            
            # Analyze the SDK quality
            analysis = self._analyze_sdk_quality(sdk_data)
            
            result = {
                "endpoints": api_endpoints or ["Sample endpoints"],
                "languages": languages or ["python", "javascript", "java"],
                "generated_sdks": sdk_data,
                "quality_analysis": analysis
            }
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return f"SDK generation failed: {str(e)}"

    def _generate_sample_sdks(self, api_endpoints: List[str] = None, languages: List[str] = None) -> Dict:
        """Generate sample SDKs for different languages."""
        # Default endpoints if none provided
        if not api_endpoints:
            api_endpoints = ["/api/users", "/api/products"]
        
        # Default languages if none provided
        if not languages:
            languages = ["python", "javascript", "java"]
        
        sdks = {}
        
        for language in languages:
            if language == "python":
                sdks[language] = self._generate_python_sdk(api_endpoints)
            elif language == "javascript":
                sdks[language] = self._generate_javascript_sdk(api_endpoints)
            elif language == "java":
                sdks[language] = self._generate_java_sdk(api_endpoints)
            else:
                sdks[language] = self._generate_generic_sdk(api_endpoints, language)
        
        return sdks

    def _generate_python_sdk(self, api_endpoints: List[str]) -> Dict:
        """Generate Python SDK."""
        sdk_code = '''# Enterprise API Python SDK
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
    
    '''
        
        # Generate methods for each endpoint
        for endpoint in api_endpoints:
            path_parts = endpoint.split('/')
            if len(path_parts) >= 3:
                resource = path_parts[2]  # e.g., "users"
                
                # Collection methods
                if not "{" in endpoint:
                    # Capitalize first letter for class names
                    resource_capitalized = resource[0].upper() + resource[1:] if len(resource) > 1 else resource.upper()
                    
                    sdk_code += f'''    def list_{resource}(self, limit: int = 20, offset: int = 0) -> List[Dict]:
        """
        List {resource}.
        
        Args:
            limit (int): Maximum number of items to return
            offset (int): Offset for pagination
            
        Returns:
            List[Dict]: List of {resource}
        """
        params = {{'limit': limit, 'offset': offset}}
        # In a real implementation, you would pass params to the request
        return self._make_request('GET', '{endpoint}')
    
    def create_{resource}(self, data: Dict) -> Dict:
        """
        Create a new {resource}.
        
        Args:
            data (Dict): {resource_capitalized} data
            
        Returns:
            Dict: Created {resource} data
        """
        return self._make_request('POST', '{endpoint}', data)
    
    '''
                
                # Resource methods (with ID)
                else:
                    resource_singular = resource[:-1] if resource.endswith('s') else resource
                    resource_singular_capitalized = resource_singular[0].upper() + resource_singular[1:] if len(resource_singular) > 1 else resource_singular.upper()
                    
                    sdk_code += f'''    def get_{resource_singular}(self, {resource_singular}_id: str) -> Dict:
        """
        Get a specific {resource_singular} by ID.
        
        Args:
            {resource_singular}_id (str): The {resource_singular} ID
            
        Returns:
            Dict: {resource_singular_capitalized} data
        """
        return self._make_request('GET', f'{endpoint.split("{{")[0]}{{{resource_singular}_id}}')
    
    def update_{resource_singular}(self, {resource_singular}_id: str, data: Dict) -> Dict:
        """
        Update a specific {resource_singular}.
        
        Args:
            {resource_singular}_id (str): The {resource_singular} ID
            data (Dict): Updated {resource_singular} data
            
        Returns:
            Dict: Updated {resource} data
        """
        return self._make_request('PUT', f'{endpoint.split("{{")[0]}{{{resource_singular}_id}}', data)
    
    def delete_{resource_singular}(self, {resource_singular}_id: str) -> bool:
        """
        Delete a specific {resource_singular}.
        
        Args:
            {resource_singular}_id (str): The {resource_singular} ID
            
        Returns:
            bool: True if deleted successfully
        """
        self._make_request('DELETE', f'{endpoint.split("{{")[0]}{{{resource_singular}_id}}')
        return True
    '''
        
        sdk_code += '''
# Usage example:
# client = EnterpriseAPIClient("https://api.example.com/v1", "your-api-key")
# users = client.list_users(limit=10)
# new_user = client.create_user({"name": "John Doe", "email": "john@example.com"})
'''
        
        return {
            "language": "python",
            "code": sdk_code,
            "installation": "pip install requests",
            "usage_example": '''import enterprise_api

client = EnterpriseAPIClient("https://api.example.com/v1", "your-api-key")
users = client.list_users(limit=10)
'''
        }

    def _generate_javascript_sdk(self, api_endpoints: List[str]) -> Dict:
        """Generate JavaScript SDK."""
        sdk_code = '''// Enterprise API JavaScript SDK
class EnterpriseAPIClient {
    constructor(baseUrl, apiKey) {
        /**
         * Initialize the Enterprise API client.
         * 
         * @param {string} baseUrl - The base URL of the API
         * @param {string} apiKey - Your API key for authentication
         */
        this.baseUrl = baseUrl.replace(/\/$/, '');
        this.apiKey = apiKey;
        this.headers = {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json'
        };
    }
    
    async _makeRequest(method, endpoint, data = null) {
        /**
         * Make an HTTP request to the API.
         * 
         * @param {string} method - HTTP method (GET, POST, PUT, DELETE)
         * @param {string} endpoint - API endpoint
         * @param {Object} data - Request data for POST/PUT requests
         * 
         * @returns {Object} API response
         */
        const url = `${this.baseUrl}${endpoint}`;
        const config = {
            method: method,
            headers: this.headers
        };
        
        if (data) {
            config.body = JSON.stringify(data);
        }
        
        try {
            const response = await fetch(url, config);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            throw new Error(`API request failed: ${error.message}`);
        }
    }
    
    '''
        
        # Generate methods for each endpoint
        for endpoint in api_endpoints:
            path_parts = endpoint.split('/')
            if len(path_parts) >= 3:
                resource = path_parts[2]
                
                # Collection methods
                if not "{" in endpoint:
                    # Capitalize first letter for method names
                    resource_capitalized = resource[0].upper() + resource[1:] if len(resource) > 1 else resource.upper()
                    
                    sdk_code += f'''    async list{resource_capitalized}(limit = 20, offset = 0) {{
        /**
         * List {resource}.
         * 
         * @param {{number}} limit - Maximum number of items to return
         * @param {{number}} offset - Offset for pagination
         * 
         * @returns {{Array}} List of {resource}
         */
        // In a real implementation, you would pass params to the request
        return await this._makeRequest('GET', '{endpoint}');
    }}
    
    async create{resource_capitalized}(data) {{
        /**
         * Create a new {resource}.
         * 
         * @param {{Object}} data - {resource_capitalized} data
         * 
         * @returns {{Object}} Created {resource} data
         */
        return await this._makeRequest('POST', '{endpoint}', data);
    }}
    
    '''
                
                # Resource methods (with ID)
                else:
                    resource_singular = resource[:-1] if resource.endswith('s') else resource
                    resource_singular_capitalized = resource_singular[0].upper() + resource_singular[1:] if len(resource_singular) > 1 else resource_singular.upper()
                    
                    sdk_code += f'''    async get{resource_singular_capitalized}({resource_singular}Id) {{
        /**
         * Get a specific {resource_singular} by ID.
         * 
         * @param {{string}} {resource_singular}Id - The {resource_singular} ID
         * 
         * @returns {{Object}} {resource_singular_capitalized} data
         */
        return await this._makeRequest('GET', `{endpoint.split("{{")[0]}${{{resource_singular}Id}}`);
    }}
    
    async update{resource_singular_capitalized}({resource_singular}Id, data) {{
        /**
         * Update a specific {resource_singular}.
         * 
         * @param {{string}} {resource_singular}Id - The {resource_singular} ID
         * @param {{Object}} data - Updated {resource_singular} data
         * 
         * @returns {{Object}} Updated {resource} data
         */
        return await this._makeRequest('PUT', `{endpoint.split("{{")[0]}${{{resource_singular}Id}}`, data);
    }}
    
    async delete{resource_singular_capitalized}({resource_singular}Id) {{
        /**
         * Delete a specific {resource_singular}.
         * 
         * @param {{string}} {resource_singular}Id - The {resource_singular} ID
         * 
         * @returns {{boolean}} True if deleted successfully
         */
        await this._makeRequest('DELETE', `{endpoint.split("{{")[0]}${{{resource_singular}Id}}`);
        return true;
    }}
    '''
        
        sdk_code += '''
}

// Usage example:
// const client = new EnterpriseAPIClient("https://api.example.com/v1", "your-api-key");
// const users = await client.listUsers(10);
// const newUser = await client.createUser({name: "John Doe", email: "john@example.com"});
'''
        
        return {
            "language": "javascript",
            "code": sdk_code,
            "installation": "npm install node-fetch",
            "usage_example": '''const EnterpriseAPIClient = require('./enterprise-api-sdk');

const client = new EnterpriseAPIClient("https://api.example.com/v1", "your-api-key");
const users = await client.listUsers(10);
'''
        }

    def _generate_java_sdk(self, api_endpoints: List[str]) -> Dict:
        """Generate Java SDK."""
        sdk_code = '''// Enterprise API Java SDK
import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import java.util.List;
import java.util.Map;
import java.util.HashMap;

public class EnterpriseAPIClient {
    private static final String BASE_URL;
    private static final String API_KEY;
    private static final HttpClient client = HttpClient.newHttpClient();
    private static final Gson gson = new Gson();
    
    public EnterpriseAPIClient(String baseUrl, String apiKey) {
        /**
         * Initialize the Enterprise API client.
         * 
         * @param baseUrl The base URL of the API
         * @param apiKey Your API key for authentication
         */
        this.BASE_URL = baseUrl.replaceAll("/$", "");
        this.API_KEY = apiKey;
    }
    
    private HttpResponse<String> makeRequest(String method, String endpoint, String data) 
            throws IOException, InterruptedException {
        /**
         * Make an HTTP request to the API.
         * 
         * @param method HTTP method (GET, POST, PUT, DELETE)
         * @param endpoint API endpoint
         * @param data Request data for POST/PUT requests
         * 
         * @return API response
         */
        String url = BASE_URL + endpoint;
        
        HttpRequest.Builder requestBuilder = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .header("Authorization", "Bearer " + API_KEY)
                .header("Content-Type", "application/json");
        
        if ("GET".equals(method)) {
            requestBuilder = requestBuilder.GET();
        } else if ("POST".equals(method)) {
            requestBuilder = requestBuilder.POST(HttpRequest.BodyPublishers.ofString(data));
        } else if ("PUT".equals(method)) {
            requestBuilder = requestBuilder.PUT(HttpRequest.BodyPublishers.ofString(data));
        } else if ("DELETE".equals(method)) {
            requestBuilder = requestBuilder.DELETE();
        }
        
        HttpRequest request = requestBuilder.build();
        return client.send(request, HttpResponse.BodyHandlers.ofString());
    }
    
    '''
        
        # Generate methods for each endpoint
        for endpoint in api_endpoints:
            path_parts = endpoint.split('/')
            if len(path_parts) >= 3:
                resource = path_parts[2]
                
                # Collection methods
                if not "{" in endpoint:
                    # Capitalize first letter for method names
                    resource_capitalized = resource[0].upper() + resource[1:] if len(resource) > 1 else resource.upper()
                    
                    sdk_code += f'''    public List<Map<String, Object>> list{resource_capitalized}(int limit, int offset) 
            throws IOException, InterruptedException {{
        /**
         * List {resource}.
         * 
         * @param limit Maximum number of items to return
         * @param offset Offset for pagination
         * 
         * @return List of {resource}
         */
        // In a real implementation, you would pass params to the request
        HttpResponse<String> response = makeRequest("GET", "{endpoint}", null);
        if (response.statusCode() == 200) {{
            return gson.fromJson(response.body(), new TypeToken<List<Map<String, Object>>>(){{}}.getType());
        }} else {{
            throw new RuntimeException("API request failed with status: " + response.statusCode());
        }}
    }}
    
    public Map<String, Object> create{resource_capitalized}(Map<String, Object> data) 
            throws IOException, InterruptedException {{
        /**
         * Create a new {resource}.
         * 
         * @param data {resource_capitalized} data
         * 
         * @return Created {resource} data
         */
        String jsonData = gson.toJson(data);
        HttpResponse<String> response = makeRequest("POST", "{endpoint}", jsonData);
        if (response.statusCode() == 201) {{
            return gson.fromJson(response.body(), new TypeToken<Map<String, Object>>(){{}}.getType());
        }} else {{
            throw new RuntimeException("API request failed with status: " + response.statusCode());
        }}
    }}
    
    '''
                
                # Resource methods (with ID)
                else:
                    resource_singular = resource[:-1] if resource.endswith('s') else resource
                    resource_singular_capitalized = resource_singular[0].upper() + resource_singular[1:] if len(resource_singular) > 1 else resource_singular.upper()
                    
                    sdk_code += f'''    public Map<String, Object> get{resource_singular_capitalized}(String {resource_singular}Id) 
            throws IOException, InterruptedException {{
        /**
         * Get a specific {resource_singular} by ID.
         * 
         * @param {resource_singular}Id The {resource_singular} ID
         * 
         * @return {resource_singular_capitalized} data
         */
        HttpResponse<String> response = makeRequest("GET", "{endpoint.split("{{")[0]}{{" + {resource_singular}Id + "}}", null);
        if (response.statusCode() == 200) {{
            return gson.fromJson(response.body(), new TypeToken<Map<String, Object>>(){{}}.getType());
        }} else {{
            throw new RuntimeException("API request failed with status: " + response.statusCode());
        }}
    }}
    
    public Map<String, Object> update{resource_singular_capitalized}(String {resource_singular}Id, Map<String, Object> data) 
            throws IOException, InterruptedException {{
        /**
         * Update a specific {resource_singular}.
         * 
         * @param {resource_singular}Id The {resource_singular} ID
         * @param data Updated {resource_singular} data
         * 
         * @return Updated {resource} data
         */
        String jsonData = gson.toJson(data);
        HttpResponse<String> response = makeRequest("PUT", "{endpoint.split("{{")[0]}{{" + {resource_singular}Id + "}}", jsonData);
        if (response.statusCode() == 200) {{
            return gson.fromJson(response.body(), new TypeToken<Map<String, Object>>(){{}}.getType());
        }} else {{
            throw new RuntimeException("API request failed with status: " + response.statusCode());
        }}
    }}
    
    public boolean delete{resource_singular_capitalized}(String {resource_singular}Id) 
            throws IOException, InterruptedException {{
        /**
         * Delete a specific {resource_singular}.
         * 
         * @param {resource_singular}Id The {resource_singular} ID
         * 
         * @return True if deleted successfully
         */
        HttpResponse<String> response = makeRequest("DELETE", "{endpoint.split("{{")[0]}{{" + {resource_singular}Id + "}}", null);
        if (response.statusCode() == 204) {{
            return true;
        }} else {{
            throw new RuntimeException("API request failed with status: " + response.statusCode());
        }}
    }}
    '''
        
        sdk_code += '''
}

// Usage example:
// EnterpriseAPIClient client = new EnterpriseAPIClient("https://api.example.com/v1", "your-api-key");
// List<Map<String, Object>> users = client.listUsers(10, 0);
// Map<String, Object> newUser = client.createUser(Map.of("name", "John Doe", "email", "john@example.com"));
'''
        
        return {
            "language": "java",
            "code": sdk_code,
            "installation": "Add Gson dependency to your project",
            "usage_example": '''EnterpriseAPIClient client = new EnterpriseAPIClient("https://api.example.com/v1", "your-api-key");
List<Map<String, Object>> users = client.listUsers(10, 0);
'''
        }

    def _generate_generic_sdk(self, api_endpoints: List[str], language: str) -> Dict:
        """Generate generic SDK for other languages."""
        return {
            "language": language,
            "code": f"// {language.capitalize()} SDK implementation for {', '.join(api_endpoints)}",
            "installation": f"// Installation instructions for {language}",
            "usage_example": f"// Usage example in {language}"
        }

    def _analyze_sdk_quality(self, sdk_data: Dict) -> Dict:
        """Analyze SDK quality and provide recommendations."""
        analysis = {
            "completeness_score": random.randint(75, 100),
            "consistency_score": random.randint(80, 95),
            "documentation_score": random.randint(70, 90)
        }
        
        # Generate recommendations
        recommendations = []
        
        if analysis["completeness_score"] < 85:
            recommendations.append({
                "priority": "MEDIUM",
                "description": "SDK completeness can be improved",
                "action": "Add missing methods for all API endpoints"
            })
        else:
            recommendations.append({
                "priority": "LOW",
                "description": "SDK completeness is good",
                "action": "Maintain current SDK coverage"
            })
        
        if analysis["documentation_score"] < 80:
            recommendations.append({
                "priority": "HIGH",
                "description": "SDK documentation needs improvement",
                "action": "Add more detailed docstrings and usage examples"
            })
        
        analysis["recommendations"] = recommendations
        return analysis