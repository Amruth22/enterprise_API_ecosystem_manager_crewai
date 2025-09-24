from crewai import Agent
from crewai.llm import LLM
from tools.documentation_builder import DocumentationBuilderTool
from tools.sdk_generator import SDKGeneratorTool
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_developer_experience_agent():
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
    
    # Create the developer experience tools
    doc_tool = DocumentationBuilderTool()
    sdk_tool = SDKGeneratorTool()
    
    agent = Agent(
        role="Developer Experience Optimizer",
        goal="Enhance developer productivity and satisfaction",
        backstory="Developer advocate with deep understanding of developer workflows and tooling",
        llm=llm,
        tools=[doc_tool, sdk_tool],
        verbose=True
    )
    
    return agent