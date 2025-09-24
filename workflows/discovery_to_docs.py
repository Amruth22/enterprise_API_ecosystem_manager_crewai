from crewai import Crew
from agents.api_discovery_agent import create_api_discovery_agent
from agents.documentation_agent import create_documentation_agent
from agents.compliance_agent import create_compliance_agent
from agents.developer_experience_agent import create_developer_experience_agent

def discovery_to_documentation_pipeline():
    """
    Discovery-to-Documentation Pipeline Workflow
    """
    # Create agents
    discovery_agent = create_api_discovery_agent()
    documentation_agent = create_documentation_agent()
    compliance_agent = create_compliance_agent()
    dev_experience_agent = create_developer_experience_agent()
    
    # For this workflow, we would define specific tasks for each step
    # This is a simplified version showing the structure
    
    workflow = {
        "name": "Discovery-to-Documentation Pipeline",
        "agents": [
            discovery_agent,
            documentation_agent,
            compliance_agent,
            dev_experience_agent
        ],
        "description": "Pipeline that moves from API discovery through to documentation publication"
    }
    
    return workflow