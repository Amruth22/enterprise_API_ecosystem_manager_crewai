from crewai.tools import BaseTool
import json
import random
from typing import Dict, List

class TestGeneratorTool(BaseTool):
    name: str = "Test Generator Tool"
    description: str = "Generate test cases for API endpoints and integration scenarios"

    def _run(self, api_endpoints: List[str] = None, test_type: str = "integration") -> str:
        """
        Generate test cases for API endpoints.
        
        Args:
            api_endpoints: List of API endpoints to generate tests for
            test_type: Type of tests to generate (unit, integration, contract)
        """
        try:
            # Generate sample test cases
            test_data = self._generate_sample_test_cases(api_endpoints, test_type)
            
            # Analyze the test coverage
            analysis = self._analyze_test_coverage(test_data)
            
            result = {
                "test_type": test_type,
                "endpoints": api_endpoints or ["Sample endpoints"],
                "generated_tests": test_data,
                "coverage_analysis": analysis
            }
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return f"Test generation failed: {str(e)}"

    def _generate_sample_test_cases(self, api_endpoints: List[str] = None, test_type: str = "integration") -> Dict:
        """Generate sample test cases."""
        # Default endpoints if none provided
        if not api_endpoints:
            api_endpoints = ["/api/users", "/api/users/{id}", "/api/products"]
        
        test_suites = {}
        
        for endpoint in api_endpoints:
            tests = []
            
            # Generate different types of tests based on test_type
            if test_type in ["integration", "contract"]:
                # Positive test cases
                tests.append({
                    "id": f"TC-001-{len(tests)+1}",
                    "name": f"Valid GET request to {endpoint}",
                    "type": "positive",
                    "description": "Verify successful response for valid request",
                    "steps": [
                        "Send GET request to endpoint",
                        "Validate response status code is 200",
                        "Validate response body structure"
                    ],
                    "expected_result": "200 OK with valid JSON response"
                })
                
                # Negative test cases
                tests.append({
                    "id": f"TC-002-{len(tests)+1}",
                    "name": f"Invalid authentication to {endpoint}",
                    "type": "negative",
                    "description": "Verify proper error handling for unauthorized requests",
                    "steps": [
                        "Send request without authentication token",
                        "Validate response status code is 401",
                        "Validate error message"
                    ],
                    "expected_result": "401 Unauthorized with proper error message"
                })
                
                # Edge case test cases
                tests.append({
                    "id": f"TC-003-{len(tests)+1}",
                    "name": f"Rate limiting for {endpoint}",
                    "type": "edge_case",
                    "description": "Verify rate limiting is enforced",
                    "steps": [
                        "Send multiple rapid requests",
                        "Validate that rate limiting kicks in",
                        "Validate 429 Too Many Requests response"
                    ],
                    "expected_result": "429 Too Many Requests after rate limit exceeded"
                })
            
            if test_type == "integration":
                # Integration-specific tests
                tests.append({
                    "id": f"TC-004-{len(tests)+1}",
                    "name": f"Database integration for {endpoint}",
                    "type": "integration",
                    "description": "Verify data persistence and retrieval",
                    "steps": [
                        "Create new resource via POST",
                        "Retrieve resource via GET",
                        "Validate data consistency"
                    ],
                    "expected_result": "Data persisted correctly and retrievable"
                })
                
                # Dependency tests
                tests.append({
                    "id": f"TC-005-{len(tests)+1}",
                    "name": f"External service dependency for {endpoint}",
                    "type": "integration",
                    "description": "Verify integration with external services",
                    "steps": [
                        "Trigger operation that requires external service",
                        "Validate external service is called",
                        "Validate proper handling of external service responses"
                    ],
                    "expected_result": "External service integration works correctly"
                })
            
            test_suites[endpoint] = {
                "total_tests": len(tests),
                "positive_tests": len([t for t in tests if t["type"] == "positive"]),
                "negative_tests": len([t for t in tests if t["type"] == "negative"]),
                "edge_case_tests": len([t for t in tests if t["type"] == "edge_case"]),
                "integration_tests": len([t for t in tests if t["type"] == "integration"]),
                "test_cases": tests
            }
        
        return {
            "test_suites": test_suites,
            "total_test_suites": len(test_suites),
            "total_test_cases": sum(suite["total_tests"] for suite in test_suites.values())
        }

    def _analyze_test_coverage(self, test_data: Dict) -> Dict:
        """Analyze test coverage and provide recommendations."""
        test_suites = test_data.get("test_suites", {})
        
        analysis = {
            "coverage_metrics": {
                "total_endpoints": len(test_suites),
                "total_test_cases": test_data.get("total_test_cases", 0),
                "average_tests_per_endpoint": test_data.get("total_test_cases", 0) / len(test_suites) if test_suites else 0
            }
        }
        
        # Coverage by test type
        coverage_by_type = {}
        for suite in test_suites.values():
            for test in suite.get("test_cases", []):
                test_type = test["type"]
                if test_type not in coverage_by_type:
                    coverage_by_type[test_type] = 0
                coverage_by_type[test_type] += 1
        
        analysis["coverage_by_type"] = coverage_by_type
        
        # Generate recommendations
        recommendations = []
        
        avg_tests = analysis["coverage_metrics"]["average_tests_per_endpoint"]
        if avg_tests < 3:
            recommendations.append({
                "priority": "HIGH",
                "description": "Low test coverage",
                "action": "Increase test cases per endpoint to minimum of 5"
            })
        elif avg_tests < 5:
            recommendations.append({
                "priority": "MEDIUM",
                "description": "Moderate test coverage",
                "action": "Consider adding more edge case and negative test scenarios"
            })
        else:
            recommendations.append({
                "priority": "LOW",
                "description": "Good test coverage",
                "action": "Maintain current testing practices"
            })
        
        # Check for missing test types
        required_types = ["positive", "negative", "edge_case"]
        if "integration" in test_data.get("test_type", ""):
            required_types.append("integration")
            
        missing_types = [t for t in required_types if t not in coverage_by_type]
        if missing_types:
            recommendations.append({
                "priority": "MEDIUM",
                "description": f"Missing test types: {', '.join(missing_types)}",
                "action": f"Add test cases covering {', '.join(missing_types)} scenarios"
            })
        
        analysis["recommendations"] = recommendations
        return analysis