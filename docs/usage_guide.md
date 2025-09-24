# Enterprise API Ecosystem Manager - Usage Guide

## Overview
This system implements a multi-agent approach to manage enterprise APIs using CrewAI with Gemini 2.0 Flash integration.

## Prerequisites
1. Python 3.8+
2. Google API key for Gemini 2.0 Flash
3. Docker (for containerized deployment)

## Installation
```bash
# Clone the repository
git clone <repository-url>
cd enterprise_api_ecosystem

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your actual API keys and configuration
```

## Configuration
Edit the `.env` file with your:
- Google Gemini API key
- Database connection strings
- Redis configuration
- Other service credentials

## Running the System
```bash
# Run the main application
python main.py
```

## Workflows
The system supports three primary workflows:

1. **Discovery-to-Documentation Pipeline**
   - Discovers APIs across the enterprise
   - Generates comprehensive documentation
   - Ensures compliance and publishes to developer portal

2. **Continuous Monitoring Workflow**
   - Monitors API performance
   - Analyzes integration test results
   - Ensures ongoing compliance
   - Optimizes performance

3. **Quality Assurance Pipeline**
   - Executes integration testing
   - Performs security audits
   - Monitors performance
   - Updates documentation

## Customization
You can customize the behavior of each agent by modifying:
- Agent prompts in the agent files
- Task definitions in the tasks directory
- Tool implementations in the tools directory
- Workflow compositions in the workflows directory

## Deployment
For production deployment:
```bash
# Using Docker Compose
docker-compose up -d
```

## Monitoring
The system provides:
- Structured JSON logging
- Performance metrics
- Audit trails for all agent actions
- Compliance event recording