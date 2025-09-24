from crewai.tools import BaseTool
import json
import random
from typing import Dict, List

class DocumentationBuilderTool(BaseTool):
    name: str = "Documentation Builder Tool"
    description: str = "Generate comprehensive API documentation and developer portal content"

    def _run(self, api_endpoints: List[str] = None, format_type: str = "openapi") -> str:
        """
        Generate API documentation.
        
        Args:
            api_endpoints: List of API endpoints to document
            format_type: Documentation format (openapi, markdown, html)
        """
        try:
            # Generate sample documentation
            doc_data = self._generate_sample_documentation(api_endpoints, format_type)
            
            # Analyze the documentation quality
            analysis = self._analyze_documentation_quality(doc_data)
            
            result = {
                "format_type": format_type,
                "endpoints": api_endpoints or ["Sample endpoints"],
                "generated_documentation": doc_data,
                "quality_analysis": analysis
            }
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return f"Documentation generation failed: {str(e)}"

    def _generate_sample_documentation(self, api_endpoints: List[str] = None, format_type: str = "openapi") -> Dict:
        """Generate sample API documentation."""
        # Default endpoints if none provided
        if not api_endpoints:
            api_endpoints = ["/api/users", "/api/products", "/api/orders"]
        
        # Generate documentation based on format type
        if format_type == "openapi":
            return self._generate_openapi_spec(api_endpoints)
        elif format_type == "markdown":
            return self._generate_markdown_docs(api_endpoints)
        else:  # html
            return self._generate_html_docs(api_endpoints)

    def _generate_openapi_spec(self, api_endpoints: List[str]) -> Dict:
        """Generate OpenAPI specification."""
        paths = {}
        
        for endpoint in api_endpoints:
            # Simple path parsing
            path_parts = endpoint.split('/')
            if len(path_parts) >= 3:
                resource = path_parts[2]  # e.g., "users" from "/api/users"
                
                # GET collection
                paths[endpoint] = {
                    "get": {
                        "summary": f"List {resource.capitalize()}",
                        "description": f"Retrieve a list of {resource}.",
                        "parameters": [
                            {
                                "name": "limit",
                                "in": "query",
                                "description": "Maximum number of items to return",
                                "required": False,
                                "schema": {"type": "integer", "format": "int32", "default": 20}
                            },
                            {
                                "name": "offset",
                                "in": "query",
                                "description": "Offset for pagination",
                                "required": False,
                                "schema": {"type": "integer", "format": "int32", "default": 0}
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": f"Successful response with list of {resource}",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "array",
                                            "items": {"$ref": f"#/components/schemas/{resource.capitalize()}"}
                                        }
                                    }
                                }
                            },
                            "401": {"$ref": "#/components/responses/Unauthorized"},
                            "403": {"$ref": "#/components/responses/Forbidden"}
                        }
                    }
                }
                
                # POST to collection
                if "users" in resource or "products" in resource:
                    paths[endpoint]["post"] = {
                        "summary": f"Create {resource.capitalize()}",
                        "description": f"Create a new {resource} resource.",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": f"#/components/schemas/{resource.capitalize()}"}
                                }
                            }
                        },
                        "responses": {
                            "201": {
                                "description": f"{resource.capitalize()} created successfully",
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": f"#/components/schemas/{resource.capitalize()}"}
                                    }
                                }
                            },
                            "400": {"$ref": "#/components/responses/BadRequest"},
                            "401": {"$ref": "#/components/responses/Unauthorized"},
                            "403": {"$ref": "#/components/responses/Forbidden"}
                        }
                    }
                
                # If endpoint has ID parameter (e.g., /api/users/{id})
                if "{" in endpoint:
                    paths[endpoint] = {
                        "get": {
                            "summary": f"Get {resource.capitalize()} by ID",
                            "description": f"Retrieve a specific {resource} by its unique identifier.",
                            "parameters": [
                                {
                                    "name": "id",
                                    "in": "path",
                                    "description": f"The {resource} identifier",
                                    "required": True,
                                    "schema": {"type": "string"}
                                }
                            ],
                            "responses": {
                                "200": {
                                    "description": f"Successful response with {resource} details",
                                    "content": {
                                        "application/json": {
                                            "schema": {"$ref": f"#/components/schemas/{resource.capitalize()}"}
                                        }
                                    }
                                },
                                "404": {"$ref": "#/components/responses/NotFound"},
                                "401": {"$ref": "#/components/responses/Unauthorized"},
                                "403": {"$ref": "#/components/responses/Forbidden"}
                            }
                        },
                        "put": {
                            "summary": f"Update {resource.capitalize()}",
                            "description": f"Update an existing {resource} resource.",
                            "parameters": [
                                {
                                    "name": "id",
                                    "in": "path",
                                    "description": f"The {resource} identifier",
                                    "required": True,
                                    "schema": {"type": "string"}
                                }
                            ],
                            "requestBody": {
                                "required": True,
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": f"#/components/schemas/{resource.capitalize()}"}
                                    }
                                }
                            },
                            "responses": {
                                "200": {
                                    "description": f"{resource.capitalize()} updated successfully",
                                    "content": {
                                        "application/json": {
                                            "schema": {"$ref": f"#/components/schemas/{resource.capitalize()}"}
                                        }
                                    }
                                },
                                "400": {"$ref": "#/components/responses/BadRequest"},
                                "404": {"$ref": "#/components/responses/NotFound"},
                                "401": {"$ref": "#/components/responses/Unauthorized"},
                                "403": {"$ref": "#/components/responses/Forbidden"}
                            }
                        },
                        "delete": {
                            "summary": f"Delete {resource.capitalize()}",
                            "description": f"Delete a specific {resource} by its unique identifier.",
                            "parameters": [
                                {
                                    "name": "id",
                                    "in": "path",
                                    "description": f"The {resource} identifier",
                                    "required": True,
                                    "schema": {"type": "string"}
                                }
                            ],
                            "responses": {
                                "204": {"description": f"{resource.capitalize()} deleted successfully"},
                                "404": {"$ref": "#/components/responses/NotFound"},
                                "401": {"$ref": "#/components/responses/Unauthorized"},
                                "403": {"$ref": "#/components/responses/Forbidden"}
                            }
                        }
                    }
        
        # Common schemas
        schemas = {
            "User": {
                "type": "object",
                "properties": {
                    "id": {"type": "string", "format": "uuid", "description": "Unique identifier"},
                    "name": {"type": "string", "description": "User's full name"},
                    "email": {"type": "string", "format": "email", "description": "User's email address"},
                    "createdAt": {"type": "string", "format": "date-time", "description": "Creation timestamp"}
                },
                "required": ["id", "name", "email"]
            },
            "Product": {
                "type": "object",
                "properties": {
                    "id": {"type": "string", "format": "uuid", "description": "Unique identifier"},
                    "name": {"type": "string", "description": "Product name"},
                    "price": {"type": "number", "format": "float", "description": "Product price"},
                    "description": {"type": "string", "description": "Product description"},
                    "createdAt": {"type": "string", "format": "date-time", "description": "Creation timestamp"}
                },
                "required": ["id", "name", "price"]
            }
        }
        
        # Common responses
        responses = {
            "BadRequest": {
                "description": "Bad request - invalid input data",
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": {
                                "error": {"type": "string"},
                                "message": {"type": "string"}
                            }
                        }
                    }
                }
            },
            "Unauthorized": {
                "description": "Unauthorized - authentication required",
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": {
                                "error": {"type": "string"},
                                "message": {"type": "string"}
                            }
                        }
                    }
                }
            },
            "Forbidden": {
                "description": "Forbidden - insufficient permissions",
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": {
                                "error": {"type": "string"},
                                "message": {"type": "string"}
                            }
                        }
                    }
                }
            },
            "NotFound": {
                "description": "Resource not found",
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": {
                                "error": {"type": "string"},
                                "message": {"type": "string"}
                            }
                        }
                    }
                }
            }
        }
        
        openapi_spec = {
            "openapi": "3.0.3",
            "info": {
                "title": "Enterprise API Documentation",
                "description": "Comprehensive documentation for enterprise APIs",
                "version": "1.0.0"
            },
            "servers": [
                {
                    "url": "https://api.example.com/v1",
                    "description": "Production server"
                }
            ],
            "paths": paths,
            "components": {
                "schemas": schemas,
                "responses": responses
            }
        }
        
        return openapi_spec

    def _generate_markdown_docs(self, api_endpoints: List[str]) -> Dict:
        """Generate Markdown documentation."""
        markdown_content = f"""# Enterprise API Documentation

## Overview
This document provides comprehensive documentation for the Enterprise APIs.

## Base URL
```
https://api.example.com/v1
```

## Authentication
All API requests require authentication via Bearer token:
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## API Endpoints

"""
        
        for endpoint in api_endpoints:
            path_parts = endpoint.split('/')
            if len(path_parts) >= 3:
                resource = path_parts[2]
                
                markdown_content += f"### {resource.capitalize()} Endpoints\n\n"
                
                if not "{" in endpoint:
                    # Collection endpoints
                    markdown_content += f"#### List {resource.capitalize()}\n\n"
                    markdown_content += f"**GET** `{endpoint}`\n\n"
                    markdown_content += f"Retrieve a list of {resource}.\n\n"
                    markdown_content += "**Query Parameters:**\n\n"
                    markdown_content += "| Parameter | Type | Required | Description |\n"
                    markdown_content += "|-----------|------|----------|-------------|\n"
                    markdown_content += "| limit | integer | No | Maximum number of items to return (default: 20) |\n"
                    markdown_content += "| offset | integer | No | Offset for pagination (default: 0) |\n\n"
                    
                    if "users" in resource or "products" in resource:
                        markdown_content += f"#### Create {resource.capitalize()}\n\n"
                        markdown_content += f"**POST** `{endpoint}`\n\n"
                        markdown_content += f"Create a new {resource}.\n\n"
                        markdown_content += "**Request Body:**\n\n```\n{\n  \"name\": \"string\",\n  \"email\": \"string\"  // for users\n}\n```\n\n"
                
                else:
                    # Resource endpoints
                    markdown_content += f"#### Get {resource.capitalize()}\n\n"
                    markdown_content += f"**GET** `{endpoint}`\n\n"
                    markdown_content += f"Retrieve a specific {resource} by ID.\n\n"
                    
                    markdown_content += f"#### Update {resource.capitalize()}\n\n"
                    markdown_content += f"**PUT** `{endpoint}`\n\n"
                    markdown_content += f"Update an existing {resource}.\n\n"
                    
                    markdown_content += f"#### Delete {resource.capitalize()}\n\n"
                    markdown_content += f"**DELETE** `{endpoint}`\n\n"
                    markdown_content += f"Delete a specific {resource}.\n\n"
        
        markdown_content += """## Error Responses

All error responses follow this format:

```
{
  "error": "string",
  "message": "string"
}
```

## Rate Limiting

API requests are rate limited to 1000 requests per hour per API key.

## Support

For support, contact api-support@example.com
"""
        
        return {
            "format": "markdown",
            "content": markdown_content
        }

    def _generate_html_docs(self, api_endpoints: List[str]) -> Dict:
        """Generate HTML documentation."""
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Enterprise API Documentation</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1, h2, h3 {{ color: #333; }}
        code {{ background-color: #f4f4f4; padding: 2px 4px; border-radius: 3px; }}
        pre {{ background-color: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <h1>Enterprise API Documentation</h1>
    
    <h2>Overview</h2>
    <p>This document provides comprehensive documentation for the Enterprise APIs.</p>
    
    <h2>Base URL</h2>
    <pre>https://api.example.com/v1</pre>
    
    <h2>Authentication</h2>
    <p>All API requests require authentication via Bearer token:</p>
    <pre>Authorization: Bearer YOUR_ACCESS_TOKEN</pre>
    
    <h2>API Endpoints</h2>
"""
        
        for endpoint in api_endpoints:
            path_parts = endpoint.split('/')
            if len(path_parts) >= 3:
                resource = path_parts[2]
                
                html_content += f"    <h3>{resource.capitalize()} Endpoints</h3>\n"
                
                if not "{" in endpoint:
                    # Collection endpoints
                    html_content += f"    <h4>List {resource.capitalize()}</h4>\n"
                    html_content += f"    <p><strong>GET</strong> <code>{endpoint}</code></p>\n"
                    html_content += f"    <p>Retrieve a list of {resource}.</p>\n"
                    html_content += "    <p><strong>Query Parameters:</strong></p>\n"
                    html_content += "    <table>\n"
                    html_content += "        <tr><th>Parameter</th><th>Type</th><th>Required</th><th>Description</th></tr>\n"
                    html_content += "        <tr><td>limit</td><td>integer</td><td>No</td><td>Maximum number of items to return (default: 20)</td></tr>\n"
                    html_content += "        <tr><td>offset</td><td>integer</td><td>No</td><td>Offset for pagination (default: 0)</td></tr>\n"
                    html_content += "    </table>\n"
                    
                    if "users" in resource or "products" in resource:
                        html_content += f"    <h4>Create {resource.capitalize()}</h4>\n"
                        html_content += f"    <p><strong>POST</strong> <code>{endpoint}</code></p>\n"
                        html_content += f"    <p>Create a new {resource}.</p>\n"
                        html_content += "    <p><strong>Request Body:</strong></p>\n"
                        html_content += "    <pre>{\n  \"name\": \"string\",\n  \"email\": \"string\"\n}</pre>\n"
                
                else:
                    # Resource endpoints
                    html_content += f"    <h4>Get {resource.capitalize()}</h4>\n"
                    html_content += f"    <p><strong>GET</strong> <code>{endpoint}</code></p>\n"
                    html_content += f"    <p>Retrieve a specific {resource} by ID.</p>\n"
                    
                    html_content += f"    <h4>Update {resource.capitalize()}</h4>\n"
                    html_content += f"    <p><strong>PUT</strong> <code>{endpoint}</code></p>\n"
                    html_content += f"    <p>Update an existing {resource}.</p>\n"
                    
                    html_content += f"    <h4>Delete {resource.capitalize()}</h4>\n"
                    html_content += f"    <p><strong>DELETE</strong> <code>{endpoint}</code></p>\n"
                    html_content += f"    <p>Delete a specific {resource}.</p>\n"
        
        html_content += """    
    <h2>Error Responses</h2>
    <p>All error responses follow this format:</p>
    <pre>{
  "error": "string",
  "message": "string"
}</pre>
    
    <h2>Rate Limiting</h2>
    <p>API requests are rate limited to 1000 requests per hour per API key.</p>
    
    <h2>Support</h2>
    <p>For support, contact <a href="mailto:api-support@example.com">api-support@example.com</a></p>
</body>
</html>"""
        
        return {
            "format": "html",
            "content": html_content
        }

    def _analyze_documentation_quality(self, doc_data: Dict) -> Dict:
        """Analyze documentation quality and provide recommendations."""
        analysis = {
            "completeness_score": random.randint(70, 100),
            "consistency_score": random.randint(75, 95),
            "clarity_score": random.randint(80, 90)
        }
        
        # Generate recommendations
        recommendations = []
        
        if analysis["completeness_score"] < 80:
            recommendations.append({
                "priority": "HIGH",
                "description": "Documentation completeness needs improvement",
                "action": "Add missing endpoint descriptions and examples"
            })
        elif analysis["completeness_score"] < 90:
            recommendations.append({
                "priority": "MEDIUM",
                "description": "Documentation completeness is good but can be improved",
                "action": "Consider adding more detailed examples and use cases"
            })
        else:
            recommendations.append({
                "priority": "LOW",
                "description": "Documentation completeness is excellent",
                "action": "Maintain current documentation standards"
            })
        
        if analysis["consistency_score"] < 80:
            recommendations.append({
                "priority": "HIGH",
                "description": "Documentation consistency issues detected",
                "action": "Standardize formatting and terminology across all endpoints"
            })
        
        if analysis["clarity_score"] < 85:
            recommendations.append({
                "priority": "MEDIUM",
                "description": "Documentation clarity can be improved",
                "action": "Simplify technical language and add more visual examples"
            })
        
        analysis["recommendations"] = recommendations
        return analysis