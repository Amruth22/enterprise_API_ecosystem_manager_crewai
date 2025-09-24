# Enterprise API Ecosystem Manager - Project Description

## 🎯 Project Overview

This is an **Enterprise API Ecosystem Manager** - an automated system that discovers, documents, and creates SDKs for enterprise APIs using a multi-agent AI approach. The system consists of 6 specialized AI agents working together through the CrewAI framework to handle the entire API lifecycle from discovery to developer enablement.

## 🏗️ Project Structure

```
D:\GEN_AI_PRO\AGENTIC-AI\enterprise_api_ecosystem\
├── agents\                      # AI Agents for specialized tasks
│   ├── api_discovery_agent.py
│   ├── compliance_agent.py
│   ├── developer_experience_agent.py
│   ├── documentation_agent.py
│   ├── integration_agent.py
│   └── performance_agent.py
├── configs\                     # Configuration files
│   └── app_config.json
├── docs\                       # Documentation files
│   └── project_overview.md
├── outputs\                    # Generated outputs (created during runtime)
│   ├── docs\
│   ├── sdks\
│   └── complete_output.txt
├── tasks\                      # Task definitions for each agent
│   ├── discovery_tasks.py
│   ├── documentation_tasks.py
│   ├── compliance_tasks.py
│   ├── performance_tasks.py
│   ├── integration_tasks.py
│   └── developer_experience_tasks.py
├── tools\                      # Custom tools for specialized functionality
│   ├── network_scanner.py
│   ├── git_analyzer.py
│   ├── security_scanner.py
│   ├── performance_metrics.py
│   ├── contract_validator.py
│   ├── test_generator.py
│   ├── documentation_builder.py
│   ├── sdk_generator.py
│   └── __init__.py
├── utils\                      # Utility functions
│   └── __init__.py
├── workflows\                 # Workflow orchestration
│   ├── discovery_to_docs.py
│   ├── monitoring.py
│   └── quality_assurance.py
├── .env                        # Environment variables (API keys)
├── Dockerfile                  # Docker configuration
├── main.py                     # Main entry point
├── README.md                   # Project documentation
└── requirements.txt            # Python dependencies
```

## 🧠 Core Components

### 6 Specialized AI Agents

1. **API Discovery Agent** - Finds and catalogs APIs from GitHub repositories and local networks
2. **Documentation Agent** - Generates comprehensive API documentation
3. **Compliance Agent** - Ensures security and regulatory compliance
4. **Performance Agent** - Monitors and optimizes API performance
5. **Integration Agent** - Tests compatibility and breaking changes
6. **Developer Experience Agent** - Enhances developer productivity with SDKs and tools

### 3 Primary Workflows

1. **Discovery-to-Documentation Pipeline**
2. **Continuous Monitoring Workflow**
3. **Quality Assurance Pipeline**

### 25+ Custom Tools

- Network Scanner
- Git Repository Analyzer
- Security Scanner
- Performance Metrics Collector
- Contract Validator
- Test Generator
- SDK Generator
- And more...

## 🚀 Implementation Guide

### Step 1: Setup Project Structure

Create the directory structure as shown above and implement the following components:

### Step 2: Install Dependencies

Create a `requirements.txt` file with:
```
crewai
python-dotenv
GitPython
requests
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment

Create a `.env` file:
```env
# Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini/gemini-2.0-flash

# Database Configuration
DATABASE_URL=sqlite:///api_ecosystem.db

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Application Settings
DEBUG=True
LOG_LEVEL=INFO
```

### Step 4: Create Configuration File

Create `configs/app_config.json`:
```json
{
  "llm_config": {
    "model": "gemini/gemini-2.0-flash",
    "max_tokens": 3000,
    "temperature": 0.3,
    "timeout": 30
  },
  "database": {
    "url": "sqlite:///api_ecosystem.db"
  },
  "redis": {
    "url": "redis://localhost:6379/0"
  }
}
```

### Step 5: Implement Agents

Create agent files in the `agents/` directory. Here's a sample implementation for the API Discovery Agent:

**agents/api_discovery_agent.py**:
```python
from crewai import Agent
from crewai.llm import LLM
from tools.git_analyzer import GitRepositoryAnalyzerTool
from tools.network_scanner import NetworkScannerTool
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_api_discovery_agent():
    # Load LLM configuration
    with open('configs/app_config.json') as f:
        config = json.load(f)
    
    # Get API key from environment
    api_key = os.getenv('GEMINI_API_KEY')
    
    # Use CrewAI's LLM wrapper instead of direct LangChain integration
    llm = LLM(
        model=config['llm_config']['model'],
        api_key=api_key,
        max_tokens=config['llm_config']['max_tokens'],
        temperature=config['llm_config']['temperature']
    )
    
    # Create the tools
    git_tool = GitRepositoryAnalyzerTool()
    network_tool = NetworkScannerTool()
    
    agent = Agent(
        role="API Discovery Specialist",
        goal="Continuously discover and catalog all APIs across the enterprise",
        backstory="Expert system administrator with deep knowledge of network protocols and API architectures",
        llm=llm,
        tools=[git_tool, network_tool],
        verbose=True
    )
    
    return agent
```

### Step 6: Implement Custom Tools

Create tool files in the `tools/` directory. Here's a sample implementation for the Git Repository Analyzer Tool:

**tools/git_analyzer.py**:
```python
from crewai.tools import BaseTool
import git
import os
import tempfile
import json
import re

class GitRepositoryAnalyzerTool(BaseTool):
    name: str = "Git Repository Analyzer Tool"
    description: str = "Parse repositories for API definitions and related files"

    def _run(self, repo_path: str = None, repo_url: str = None) -> str:
        # Clone repository if URL is provided
        if repo_url:
            # Create a temporary directory to clone the repository
            temp_dir = tempfile.mkdtemp()
            try:
                # Clone the repository
                git.Repo.clone_from(repo_url, temp_dir)
                repo_path = temp_dir
            except Exception as e:
                return f"Failed to clone repository: {str(e)}"
        
        # If no repo_path is provided, use current directory
        if not repo_path:
            repo_path = "."
            
        try:
            # Initialize repository
            repo = git.Repo(repo_path)
            
            # Get basic repository information
            repo_info = {
                "repository": repo_url or repo_path,
                "active_branch": str(repo.active_branch),
                "commit_count": len(list(repo.iter_commits())),
                "file_count": len([item for item in repo.tree().traverse() if item.type == 'blob'])
            }
            
            # Look for common API definition files and related files
            api_files = []
            python_files = []
            config_files = []
            
            for item in repo.tree().traverse():
                if item.type == 'blob':
                    filename = item.name.lower()
                    # Look for common API definition file patterns
                    if any(pattern in filename for pattern in [
                        'openapi', 'swagger', 'api', 'routes', 'endpoints'
                    ]):
                        api_files.append({
                            "name": item.name,
                            "path": item.path,
                            "type": "api_definition"
                        })
                    elif filename.endswith(('.json', '.yaml', '.yml')):
                        api_files.append({
                            "name": item.name,
                            "path": item.path,
                            "type": "config_or_spec"
                        })
                    elif filename.endswith('.py'):
                        python_files.append({
                            "name": item.name,
                            "path": item.path
                        })
                    elif any(pattern in filename for pattern in [
                        'config', 'settings', 'env', '.env', '.ini', '.cfg'
                    ]):
                        config_files.append({
                            "name": item.name,
                            "path": item.path
                        })
            
            # Add file information to repo info
            repo_info["potential_api_files"] = api_files
            repo_info["python_files"] = python_files
            repo_info["config_files"] = config_files
            
            # Get recent commits
            recent_commits = []
            for commit in list(repo.iter_commits())[:5]:  # Last 5 commits
                recent_commits.append({
                    "sha": commit.hexsha[:8],
                    "message": commit.message.strip(),
                    "author": str(commit.author),
                    "date": commit.committed_datetime.isoformat()
                })
            
            repo_info["recent_commits"] = recent_commits
            
            return json.dumps(repo_info, indent=2)
            
        except Exception as e:
            return f"Failed to analyze repository: {str(e)}"
```

### Step 7: Define Tasks

Create task files in the `tasks/` directory. Here's a sample task definition:

**tasks/discovery_tasks.py**:
```python
from crewai import Task
from agents.api_discovery_agent import create_api_discovery_agent

# Create agent for task definition
agent = create_api_discovery_agent()

discovery_task = Task(
    description="""Analyze the GitHub repository at https://github.com/Amruth22/W1D10S3-Agent-Deployment-RabbitMQ-queue to discover any APIs or related functionality. 
    Also scan the local network for active API services.
    
    Focus on:
    1. Identifying Python files that might contain API endpoints or related code in the Git repository
    2. Looking for configuration files that might define API behavior
    3. Analyzing the commit history to understand API evolution
    4. Identifying any API documentation or specification files
    5. Scanning the local network for active API services on common ports
    
    Use the Git Repository Analyzer Tool and Network Scanner Tool to gather information and report your findings.""",
    agent=agent,
    expected_output="A structured JSON report listing all discovered APIs and related functionality with metadata including endpoints, technologies used, potential security concerns, and change history."
)
```

### Step 8: Implement Main Orchestration

Create the main entry point in `main.py`:

```python
# Enterprise API Ecosystem Manager
# This system automatically discovers, documents, and creates SDKs for enterprise APIs

import os
import json
import re
from dotenv import load_dotenv
from crewai import Crew

load_dotenv()

def run_discovery_to_documentation_pipeline():
    # """Run the discovery to documentation pipeline workflow."""
    print("Enterprise API Ecosystem Manager")
    print("================================")
    print("Running Discovery-to-Documentation Pipeline...")
    
    # Import all agents
    from agents.api_discovery_agent import create_api_discovery_agent
    from agents.documentation_agent import create_documentation_agent
    from agents.compliance_agent import create_compliance_agent
    from agents.developer_experience_agent import create_developer_experience_agent

    # Create all agents
    api_discovery_agent = create_api_discovery_agent()
    documentation_agent = create_documentation_agent()
    compliance_agent = create_compliance_agent()
    developer_experience_agent = create_developer_experience_agent()

    # Import all tasks
    from tasks.discovery_tasks import discovery_task
    from tasks.documentation_tasks import documentation_task
    from tasks.compliance_tasks import compliance_task
    from tasks.developer_experience_tasks import developer_experience_task

    # Create the crew with all agents and tasks
    api_ecosystem_crew = Crew(
        agents=[
            api_discovery_agent,
            documentation_agent,
            compliance_agent,
            developer_experience_agent
        ],
        tasks=[
            discovery_task,
            documentation_task,
            compliance_task,
            developer_experience_task
        ],
        verbose=True
    )

    # Execute the crew and get the result
    result = api_ecosystem_crew.kickoff()
    return result

def save_complete_output(result):
    # """Save the complete output to a text file."""
    try:
        # Ensure outputs directory exists
        os.makedirs("outputs", exist_ok=True)
            
        # Save the result to a file
        with open("outputs/complete_output.txt", "w", encoding="utf-8") as f:
            f.write(str(result))
            
        print("[SUCCESS] Complete output saved to outputs/complete_output.txt")
        return True
        
    except Exception as e:
        print(f"[ERROR] Error saving complete output: {e}")
        return False

def extract_and_save_components(content):
    # """Extract components from the complete output and save them separately."""
    try:
        # Create directories
        os.makedirs("outputs/docs", exist_ok=True)
        os.makedirs("outputs/sdks/python", exist_ok=True)
        os.makedirs("outputs/sdks/javascript", exist_ok=True)
        
        print("[INFO] Extracting and saving components...")
        
        # Try to extract Python SDK
        python_sdk_pattern = r"```python\s*\n(.*?class\s+.*?Client.*?)\s*```"
        python_sdk_match = re.search(python_sdk_pattern, content, re.DOTALL | re.IGNORECASE)
        
        if python_sdk_match:
            python_sdk = python_sdk_match.group(1)
            with open("outputs/sdks/python/enterprise_api_client.py", "w", encoding="utf-8") as f:
                f.write(python_sdk)
            print("[SUCCESS] Python SDK saved to outputs/sdks/python/enterprise_api_client.py")
        else:
            print("[INFO] No Python SDK found in output")
        
        # Try to extract JavaScript SDK
        js_sdk_pattern = r"```javascript\s*\n(.*?class\s+.*?Client.*?)\s*```"
        js_sdk_match = re.search(js_sdk_pattern, content, re.DOTALL | re.IGNORECASE)
        
        if js_sdk_match:
            js_sdk = js_sdk_match.group(1)
            with open("outputs/sdks/javascript/enterprise_api_client.js", "w", encoding="utf-8") as f:
                f.write(js_sdk)
            print("[SUCCESS] JavaScript SDK saved to outputs/sdks/javascript/enterprise_api_client.js")
        else:
            print("[INFO] No JavaScript SDK found in output")
        
        # Save documentation
        with open("outputs/docs/api_documentation.md", "w", encoding="utf-8") as f:
            f.write(content)
        print("[SUCCESS] Documentation saved to outputs/docs/api_documentation.md")
        
        print("\n[SUCCESS] Component extraction and saving completed!")
        return True
        
    except Exception as e:
        print(f"[ERROR] Error extracting and saving components: {e}")
        return False

def main():
    try:
        # Run the discovery to documentation pipeline
        result = run_discovery_to_documentation_pipeline()
        
        print("\nPipeline execution completed!")
        print("=" * 50)
        
        # Save the complete output
        if save_complete_output(result):
            # Extract and save individual components
            try:
                with open("outputs/complete_output.txt", "r", encoding="utf-8") as f:
                    content = f.read()
                extract_and_save_components(content)
            except Exception as e:
                print(f"[ERROR] Error reading complete output for extraction: {e}")
        else:
            print("[ERROR] Failed to save complete output")
        
        print("\n[SUCCESS] Pipeline completed successfully!")
        print("[INFO] All outputs have been saved to the 'outputs' directory")
        
    except Exception as e:
        print(f"\n[ERROR] Pipeline failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
```

## 📤 Generated Outputs

When you run the system, it automatically creates:

- **API Documentation** in `outputs/docs/`
- **Multi-language SDKs** in `outputs/sdks/`
- **Complete execution logs** in `outputs/complete_output.txt`

## ▶️ How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up environment variables in .env
# Add your GEMINI_API_KEY

# 3. Run the system
python main.py
```

## ✅ System Features

- **Multi-Agent Orchestration**: 6 specialized AI agents working together
- **Automatic Documentation**: Generates complete API documentation
- **Multi-Language SDKs**: Creates SDKs for Python, JavaScript, and more
- **Network Discovery**: Scans local networks for API services
- **Security Compliance**: Checks for security vulnerabilities and compliance
- **Performance Monitoring**: Analyzes API performance and optimization
- **Developer Tools**: Creates interactive API explorers and developer portals

## 🎓 Learning Objectives

By building this project, students will learn:

1. **Multi-Agent AI Systems**: How to design and implement systems with multiple specialized AI agents
2. **CrewAI Framework**: How to use CrewAI for orchestrating AI workflows
3. **Custom Tool Development**: How to create specialized tools for AI agents
4. **API Discovery and Analysis**: Techniques for finding and analyzing APIs in code repositories
5. **Automated Documentation Generation**: How to automatically generate API documentation
6. **SDK Generation**: How to programmatically create software development kits
7. **Security and Compliance**: How to integrate security scanning into automated workflows
8. **System Architecture**: How to design complex multi-component systems

This project provides a comprehensive learning experience in building enterprise-grade AI systems that automate API management workflows.