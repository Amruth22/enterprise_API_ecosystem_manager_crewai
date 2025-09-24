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