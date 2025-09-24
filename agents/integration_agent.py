from crewai import Agent
from crewai.llm import LLM
from tools.contract_validator import ContractValidatorTool
from tools.test_generator import TestGeneratorTool
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_integration_agent():
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
    
    # Create the integration testing tools
    contract_tool = ContractValidatorTool()
    test_tool = TestGeneratorTool()
    
    agent = Agent(
        role="API Integration Testing Specialist",
        goal="Automated testing for compatibility and breaking changes",
        backstory="QA engineer with expertise in API testing and contract validation",
        llm=llm,
        tools=[contract_tool, test_tool],
        verbose=True
    )
    
    return agent