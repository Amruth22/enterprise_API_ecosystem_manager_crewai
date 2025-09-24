from crewai import Task
from agents.documentation_agent import create_documentation_agent

# Create agent for task definition
agent = create_documentation_agent()

documentation_task = Task(
    description="Generate OpenAPI specifications, interactive documentation, multi-language code samples, version documentation, and migration guides based on the discovered APIs. Focus on clear, comprehensive documentation generation with technical accuracy.",
    agent=agent,
    expected_output="Complete API documentation in OpenAPI specs, Markdown, and HTML formats, along with multi-language code samples and version-specific documentation."
)