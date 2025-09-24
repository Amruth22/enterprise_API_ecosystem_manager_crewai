from crewai import Task
from agents.performance_agent import create_performance_agent

# Create agent for task definition
agent = create_performance_agent()

performance_task = Task(
    description="""Monitor real-time API performance, analyze usage patterns, identify bottlenecks, plan capacity, and track SLA compliance. 
    Focus on performance pattern analysis and optimization.
    
    Use the Performance Metrics Tool to collect and analyze performance data for common API endpoints.
    Generate a comprehensive performance report with optimization recommendations.""",
    agent=agent,
    expected_output="Performance reports with optimization recommendations, bottleneck analysis, capacity planning data, and SLA compliance tracking."
)