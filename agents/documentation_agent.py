from crewai import Agent
from crewai.llm import LLM
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_documentation_agent():
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
    
    agent = Agent(
        role="Technical Documentation Expert",
        goal="Generate comprehensive, accurate API documentation automatically",
        backstory="Technical writer with expertise in API specifications and developer experience",
        llm=llm,
        verbose=True
    )
    
    return agent