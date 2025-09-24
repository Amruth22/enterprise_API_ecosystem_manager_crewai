from crewai import Task
from agents.integration_agent import create_integration_agent

# Create agent for task definition
agent = create_integration_agent()

integration_task = Task(
    description="""Execute contract testing, detect breaking changes, validate backward compatibility, 
    perform integration testing, and conduct regression testing for all APIs. 
    Focus on test case generation and compatibility analysis.
    
    Use the Contract Validator Tool to check for API contract violations and breaking changes.
    Use the Test Generator Tool to create comprehensive test suites for integration scenarios.
    Generate compatibility matrices and test results.""",
    agent=agent,
    expected_output="Complete test suites, compatibility matrices, breaking change reports, and integration test results for all APIs."
)