from crewai import Task
from agents.compliance_agent import create_compliance_agent

# Create agent for task definition
agent = create_compliance_agent()

compliance_task = Task(
    description="""Perform OWASP API security validation, regulatory compliance checking, authentication/authorization audits, 
    rate limiting verification, and security vulnerability assessment on all discovered APIs. 
    Focus on security analysis and compliance validation.
    
    Use the Security Scanner Tool to perform comprehensive security assessments and compliance checks.
    Generate detailed compliance reports and security scorecards.""",
    agent=agent,
    expected_output="Comprehensive compliance reports and security scorecards for each API, highlighting vulnerabilities, compliance issues, and recommended remediations."
)