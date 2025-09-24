from crewai import Agent
from crewai.llm import LLM
from tools.performance_metrics import PerformanceMetricsTool
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_performance_agent():
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
    
    # Create the performance metrics tool
    performance_tool = PerformanceMetricsTool()
    
    agent = Agent(
        role="Performance Analytics Specialist",
        goal="Monitor API performance and identify optimization opportunities",
        backstory="Performance engineer with expertise in system optimization and capacity planning",
        llm=llm,
        tools=[performance_tool],
        verbose=True
    )
    
    return agent