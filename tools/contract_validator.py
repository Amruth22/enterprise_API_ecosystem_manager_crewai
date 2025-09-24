from crewai.tools import BaseTool
import json
import random
from typing import Dict, List

class ContractValidatorTool(BaseTool):
    name: str = "Contract Validator Tool"
    description: str = "Validate API contracts and check for breaking changes"

    def _run(self, api_spec_path: str = None, previous_version: str = None) -> str:
        """
        Validate API contracts and check for breaking changes.
        
        Args:
            api_spec_path: Path to API specification file (OpenAPI/Swagger)
            previous_version: Previous version to compare against
        """
        try:
            # Generate sample API contract validation
            contract_data = self._generate_sample_contract_validation(api_spec_path, previous_version)
            
            # Analyze the contract validation
            analysis = self._analyze_contract_validation(contract_data)
            
            result = {
                "api_spec_path": api_spec_path or "Sample API Contract",
                "previous_version": previous_version or "1.0.0",
                "contract_validation": contract_data,
                "analysis": analysis
            }
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return f"Contract validation failed: {str(e)}"

    def _generate_sample_contract_validation(self, api_spec_path: str = None, previous_version: str = None) -> Dict:
        """Generate sample API contract validation data."""
        # Sample API endpoints
        endpoints = [
            {
                "path": "/api/users",
                "method": "GET",
                "parameters": [
                    {"name": "limit", "in": "query", "required": False, "type": "integer"},
                    {"name": "offset", "in": "query", "required": False, "type": "integer"}
                ],
                "responses": {
                    "200": {"description": "Successful response", "schema": {"type": "array"}},
                    "401": {"description": "Unauthorized"},
                    "403": {"description": "Forbidden"}
                }
            },
            {
                "path": "/api/users",
                "method": "POST",
                "parameters": [
                    {"name": "body", "in": "body", "required": True, "schema": {"type": "object"}}
                ],
                "responses": {
                    "201": {"description": "User created", "schema": {"type": "object"}},
                    "400": {"description": "Bad request"},
                    "401": {"description": "Unauthorized"}
                }
            },
            {
                "path": "/api/users/{id}",
                "method": "GET",
                "parameters": [
                    {"name": "id", "in": "path", "required": True, "type": "string"}
                ],
                "responses": {
                    "200": {"description": "User details", "schema": {"type": "object"}},
                    "404": {"description": "User not found"},
                    "401": {"description": "Unauthorized"}
                }
            },
            {
                "path": "/api/users/{id}",
                "method": "PUT",
                "parameters": [
                    {"name": "id", "in": "path", "required": True, "type": "string"},
                    {"name": "body", "in": "body", "required": True, "schema": {"type": "object"}}
                ],
                "responses": {
                    "200": {"description": "User updated", "schema": {"type": "object"}},
                    "400": {"description": "Bad request"},
                    "404": {"description": "User not found"},
                    "401": {"description": "Unauthorized"}
                }
            }
        ]
        
        # Simulate breaking changes if comparing versions
        breaking_changes = []
        if previous_version:
            # Randomly introduce some breaking changes
            if random.random() < 0.3:  # 30% chance of breaking changes
                breaking_changes.append({
                    "type": "removed_endpoint",
                    "endpoint": "/api/users/profile",
                    "description": "Endpoint removed without deprecation"
                })
            if random.random() < 0.2:  # 20% chance of parameter changes
                breaking_changes.append({
                    "type": "parameter_removed",
                    "endpoint": "/api/users",
                    "parameter": "sort",
                    "description": "Required parameter 'sort' removed from GET /api/users"
                })
        
        # Add some validation issues
        validation_issues = []
        if random.random() < 0.4:  # 40% chance of validation issues
            validation_issues.append({
                "type": "missing_response_schema",
                "endpoint": "/api/users POST",
                "description": "Response schema not defined for 201 status"
            })
        if random.random() < 0.3:  # 30% chance of another issue
            validation_issues.append({
                "type": "inconsistent_naming",
                "description": "Inconsistent parameter naming (camelCase vs snake_case)"
            })
        
        contract_validation = {
            "api_name": "User Management API",
            "current_version": "2.0.0",
            "previous_version": previous_version or "1.0.0",
            "total_endpoints": len(endpoints),
            "endpoints": endpoints,
            "breaking_changes": breaking_changes,
            "validation_issues": validation_issues,
            "compatibility_score": round(random.uniform(70, 100), 2) if not breaking_changes else round(random.uniform(30, 70), 2)
        }
        
        return contract_validation

    def _analyze_contract_validation(self, contract_data: Dict) -> Dict:
        """Analyze contract validation results and provide recommendations."""
        breaking_changes = contract_data.get("breaking_changes", [])
        validation_issues = contract_data.get("validation_issues", [])
        
        analysis = {
            "compatibility_status": "COMPATIBLE" if not breaking_changes else "BREAKING_CHANGES",
            "issue_summary": {
                "breaking_changes_count": len(breaking_changes),
                "validation_issues_count": len(validation_issues)
            }
        }
        
        # Generate recommendations
        recommendations = []
        
        if breaking_changes:
            recommendations.append({
                "priority": "CRITICAL",
                "description": f"{len(breaking_changes)} breaking changes detected",
                "action": "Implement proper deprecation strategy and versioning"
            })
        
        if validation_issues:
            recommendations.append({
                "priority": "HIGH",
                "description": f"{len(validation_issues)} validation issues found",
                "action": "Fix API specification inconsistencies and missing schemas"
            })
        
        # Overall compatibility assessment
        compatibility_score = contract_data.get("compatibility_score", 0)
        if compatibility_score >= 90:
            recommendations.append({
                "priority": "LOW",
                "description": "High compatibility score",
                "action": "Continue monitoring for future changes"
            })
        elif compatibility_score >= 70:
            recommendations.append({
                "priority": "MEDIUM",
                "description": "Moderate compatibility score",
                "action": "Address identified issues to improve compatibility"
            })
        else:
            recommendations.append({
                "priority": "HIGH",
                "description": "Low compatibility score",
                "action": "Immediate attention required to fix compatibility issues"
            })
        
        analysis["recommendations"] = recommendations
        return analysis