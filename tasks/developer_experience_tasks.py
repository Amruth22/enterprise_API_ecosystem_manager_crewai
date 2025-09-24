from crewai import Task
from agents.developer_experience_agent import create_developer_experience_agent

# Create agent for task definition
agent = create_developer_experience_agent()

developer_experience_task = Task(
    description="""Generate multi-language SDKs, create interactive API explorers, maintain developer portals, 
    generate boilerplate code, and create troubleshooting guides. 
    Focus on developer-friendly content generation.
    
    Use the Documentation Builder Tool to create comprehensive API documentation in multiple formats.
    Use the SDK Generator Tool to create SDKs for popular programming languages.
    Generate developer portal content and code examples.""",
    agent=agent,
    expected_output="Multi-language SDKs, interactive API explorer tools, updated developer portal content, boilerplate code samples, and comprehensive troubleshooting guides."
)