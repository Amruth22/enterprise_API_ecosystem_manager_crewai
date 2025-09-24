from crewai import Agent
from crewai.llm import LLM
from tools.security_scanner import SecurityScannerTool
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_compliance_agent():
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
    
    # Create the security scanner tool
    security_tool = SecurityScannerTool()
    
    agent = Agent(
        role="Security and Compliance Auditor",
        goal="Ensure APIs meet security, regulatory, and organizational standards",
        backstory="Cybersecurity expert with deep knowledge of API security frameworks and compliance requirements",
        llm=llm,
        tools=[security_tool],
        verbose=True
    )
    
    return agent