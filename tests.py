import unittest
import os
import json
import tempfile
import sys
from unittest.mock import patch, MagicMock

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class TestEnterpriseAPIEcosystem(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Use a relative path from the test file location
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        
    def test_01_api_key_validation(self):
        """Test that API key exists in .env file and is properly formatted"""
        # Check if .env file exists
        env_path = os.path.join(self.project_root, '.env')
        self.assertTrue(os.path.exists(env_path), "Environment file (.env) not found")
        
        # Read the .env file
        with open(env_path, 'r') as f:
            env_content = f.read()
            
        # Check if GEMINI_API_KEY is present
        self.assertIn('GEMINI_API_KEY=', env_content, "GEMINI_API_KEY not found in .env file")
        
        # Verify API key doesn't have extra quotes that could cause issues
        lines = env_content.split('\n')
        for line in lines:
            if line.startswith('GEMINI_API_KEY='):
                api_key = line.split('=', 1)[1]
                # Check that key doesn't start/end with quotes
                self.assertFalse(api_key.startswith('"') and api_key.endswith('"'), 
                               "API key should not be wrapped in quotes")
                self.assertFalse(api_key.startswith("'") and api_key.endswith("'"), 
                               "API key should not be wrapped in single quotes")
                # Check that key has reasonable length
                self.assertGreater(len(api_key), 20, "API key appears too short to be valid")
                break
    
    def test_02_agent_creation(self):
        """Test that all agents can be created successfully"""
        # Test API Discovery Agent creation
        from agents.api_discovery_agent import create_api_discovery_agent
        discovery_agent = create_api_discovery_agent()
        self.assertIsNotNone(discovery_agent, "API Discovery Agent creation failed")
        self.assertEqual(discovery_agent.role, "API Discovery Specialist")
        
        # Test Documentation Agent creation
        from agents.documentation_agent import create_documentation_agent
        documentation_agent = create_documentation_agent()
        self.assertIsNotNone(documentation_agent, "Documentation Agent creation failed")
        self.assertEqual(documentation_agent.role, "Technical Documentation Expert")
        
        # Test Compliance Agent creation
        from agents.compliance_agent import create_compliance_agent
        compliance_agent = create_compliance_agent()
        self.assertIsNotNone(compliance_agent, "Compliance Agent creation failed")
        self.assertEqual(compliance_agent.role, "Security and Compliance Auditor")
        
        # Test Developer Experience Agent creation
        from agents.developer_experience_agent import create_developer_experience_agent
        dev_agent = create_developer_experience_agent()
        self.assertIsNotNone(dev_agent, "Developer Experience Agent creation failed")
        self.assertEqual(dev_agent.role, "Developer Experience Optimizer")
    
    def test_03_task_creation_and_assignment(self):
        """Test that tasks are correctly created and assigned to agents"""
        # Test Discovery Task
        from tasks.discovery_tasks import discovery_task
        self.assertIsNotNone(discovery_task, "Discovery task creation failed")
        self.assertIsNotNone(discovery_task.agent, "Discovery task not assigned to agent")
        self.assertIn("GitHub repository", discovery_task.description, "Discovery task description incorrect")
        
        # Test Documentation Task
        from tasks.documentation_tasks import documentation_task
        self.assertIsNotNone(documentation_task, "Documentation task creation failed")
        self.assertIsNotNone(documentation_task.agent, "Documentation task assigned to agent")
        self.assertIn("OpenAPI specifications", documentation_task.description, "Documentation task description incorrect")
        
        # Test Compliance Task
        from tasks.compliance_tasks import compliance_task
        self.assertIsNotNone(compliance_task, "Compliance task creation failed")
        self.assertIsNotNone(compliance_task.agent, "Compliance task not assigned to agent")
        self.assertIn("OWASP API security", compliance_task.description, "Compliance task description incorrect")
        
        # Test Developer Experience Task
        from tasks.developer_experience_tasks import developer_experience_task
        self.assertIsNotNone(developer_experience_task, "Developer Experience task creation failed")
        self.assertIsNotNone(developer_experience_task.agent, "Developer Experience task not assigned to agent")
        self.assertIn("multi-language SDKs", developer_experience_task.description, "Developer Experience task description incorrect")
    
    def test_04_git_repository_analyzer_tool(self):
        """Test Git repository analyzer tool functionality"""
        from tools.git_analyzer import GitRepositoryAnalyzerTool
        git_tool = GitRepositoryAnalyzerTool()
        self.assertIsNotNone(git_tool, "Git Repository Analyzer Tool creation failed")
        self.assertEqual(git_tool.name, "Git Repository Analyzer Tool")
        
        # Test basic functionality with a simple repo check
        result = git_tool._run()
        self.assertIsInstance(result, str, "Git tool should return string result")
    
    def test_05_network_scanner_tool(self):
        """Test network scanner tool functionality"""
        from tools.network_scanner import NetworkScannerTool
        network_tool = NetworkScannerTool()
        self.assertIsNotNone(network_tool, "Network Scanner Tool creation failed")
        self.assertEqual(network_tool.name, "Network Scanner Tool")
        
        # Test basic functionality
        result = network_tool._run()
        self.assertIsInstance(result, str, "Network tool should return string result")
    
    def test_06_security_scanner_tool(self):
        """Test security scanner tool functionality"""
        from tools.security_scanner import SecurityScannerTool
        security_tool = SecurityScannerTool()
        self.assertIsNotNone(security_tool, "Security Scanner Tool creation failed")
        self.assertEqual(security_tool.name, "Security Scanner Tool")
        
        # Test basic functionality
        result = security_tool._run()
        self.assertIsInstance(result, str, "Security tool should return string result")
        self.assertIn("security_assessment", result, "Security result should contain assessment")
    
    def test_07_documentation_builder_tool(self):
        """Test documentation builder tool functionality"""
        from tools.documentation_builder import DocumentationBuilderTool
        doc_tool = DocumentationBuilderTool()
        self.assertIsNotNone(doc_tool, "Documentation Builder Tool creation failed")
        self.assertEqual(doc_tool.name, "Documentation Builder Tool")
        
        # Test basic functionality
        result = doc_tool._run()
        self.assertIsInstance(result, str, "Documentation tool should return string result")
        self.assertIn("generated_documentation", result, "Documentation result should contain generated docs")
    
    def test_08_sdk_generator_tool(self):
        """Test SDK generator tool functionality"""
        from tools.sdk_generator import SDKGeneratorTool
        sdk_tool = SDKGeneratorTool()
        self.assertIsNotNone(sdk_tool, "SDK Generator Tool creation failed")
        self.assertEqual(sdk_tool.name, "SDK Generator Tool")
        
        # Test basic functionality
        result = sdk_tool._run()
        self.assertIsInstance(result, str, "SDK tool should return string result")
        self.assertIn("generated_sdks", result, "SDK result should contain generated SDKs")
    
    def test_09_main_pipeline_execution(self):
        """Test main pipeline execution flow"""
        # Mock the Crew kickoff to avoid actual API calls
        with patch('crewai.Crew.kickoff') as mock_kickoff:
            mock_kickoff.return_value = "Mock pipeline execution result"
            
            # Import and run the main pipeline function
            from main import run_discovery_to_documentation_pipeline
            result = run_discovery_to_documentation_pipeline()
            
            # Verify the function executed
            self.assertIsNotNone(result, "Main pipeline execution should return a result")
            mock_kickoff.assert_called_once()
    
    def test_10_output_storage(self):
        """Test output storage and file creation"""
        # Create a temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Test save_complete_output function
            from main import save_complete_output
            test_result = "Test output content for storage test"
            success = save_complete_output(test_result)
            
            # Verify the function executed without error
            self.assertIsInstance(success, bool, "save_complete_output should return boolean")
            
            # Test extract_and_save_components function
            from main import extract_and_save_components
            test_content = "# Test Documentation\n\nThis is test content."
            success = extract_and_save_components(test_content)
            
            # Verify the function executed without error
            self.assertIsInstance(success, bool, "extract_and_save_components should return boolean")

if __name__ == '__main__':
    unittest.main()