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