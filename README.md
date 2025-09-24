# Enterprise API Ecosystem Manager

## 🎯 **Project Overview**

This is an **Enterprise API Ecosystem Manager** - an automated system that discovers, documents, and creates SDKs for enterprise APIs using a multi-agent AI approach. The system consists of 6 specialized AI agents working together through the CrewAI framework to handle the entire API lifecycle from discovery to developer enablement.

## 🧠 **Core Components**

### **6 Specialized AI Agents**

1. **API Discovery Agent** - Finds and catalogs APIs from GitHub repositories and local networks
2. **Documentation Agent** - Generates comprehensive API documentation
3. **Compliance Agent** - Ensures security and regulatory compliance
4. **Performance Agent** - Monitors and optimizes API performance
5. **Integration Agent** - Tests compatibility and breaking changes
6. **Developer Experience Agent** - Enhances developer productivity with SDKs and tools

### **3 Primary Workflows**

1. **Discovery-to-Documentation Pipeline**
2. **Continuous Monitoring Workflow**
3. **Quality Assurance Pipeline**

### **25+ Custom Tools**

- Network Scanner
- Git Repository Analyzer
- Security Scanner
- Performance Metrics Collector
- Contract Validator
- Test Generator
- SDK Generator
- Documentation Builder
- And more...

## 📁 **Project Structure**

```
D:\GEN_AI_PRO\AGENTIC-AI\enterprise_api_ecosystem_iamneo\Project\
├── agents\                      # AI Agents for specialized tasks
│   ├── api_discovery_agent.py
│   ├── compliance_agent.py
│   ├── developer_experience_agent.py
│   ├── documentation_agent.py
│   ├── integration_agent.py
│   └── performance_agent.py
├── configs\                     # Configuration files
│   └── app_config.json
├── docs\                       # Documentation files
├── outputs\                    # Generated outputs (created during runtime)
│   ├── docs\
│   ├── sdks\
│   └── complete_output.txt
├── tasks\                      # Task definitions for each agent
│   ├── discovery_tasks.py
│   ├── documentation_tasks.py
│   ├── compliance_tasks.py
│   ├── performance_tasks.py
│   ├── integration_tasks.py
│   └── developer_experience_tasks.py
├── tools\                      # Custom tools for specialized functionality
│   ├── network_scanner.py
│   ├── git_analyzer.py
│   ├── security_scanner.py
│   ├── performance_metrics.py
│   ├── contract_validator.py
│   ├── test_generator.py
│   ├── documentation_builder.py
│   ├── sdk_generator.py
│   └── __init__.py
├── utils\                      # Utility functions
├── workflows\                 # Workflow orchestration
│   ├── discovery_to_docs.py
│   ├── monitoring.py
│   └── quality_assurance.py
├── .env                        # Environment variables (API keys)
├── Dockerfile                  # Docker configuration
├── main.py                     # Main entry point
├── PROJECT_STRUCTURE.md
├── question_description.md
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
└── tests.py                    # Test suite
```

## ⚙️ **Prerequisites**

1. **Python 3.8+**
2. **Google API key for Gemini 2.0 Flash**
3. **Docker** (optional, for containerized deployment)

## ▶️ **Installation**

```bash
# 1. Clone the repository (if not already cloned)
# git clone <repository-url>
# cd enterprise_api_ecosystem

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment variables
# Copy .env.example to .env and edit with your actual API keys and configuration
# cp .env.example .env  # (Note: .env.example may not exist, see Configuration section)
```

## ⚙️ **Configuration**

Edit the `.env` file with your:
- Google Gemini API key
- Database connection strings
- Redis configuration
- Other service credentials

**Required Environment Variables:**
```env
# Gemini API Configuration
GEMINI_API_KEY=your_actual_gemini_api_key_here
GEMINI_MODEL=gemini/gemini-2.0-flash

# Database Configuration
DATABASE_URL=sqlite:///api_ecosystem.db

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Application Settings
DEBUG=True
LOG_LEVEL=INFO
```

**LLM Configuration** (in `configs/app_config.json`):
```json
{
  "llm_config": {
    "model": "gemini/gemini-2.0-flash",
    "max_tokens": 3000,
    "temperature": 0.3,
    "timeout": 30
  },
  "database": {
    "url": "sqlite:///api_ecosystem.db"
  },
  "redis": {
    "url": "redis://localhost:6379/0"
  }
}
```

## ▶️ **How to Run the System**

```bash
# Run the system
python main.py
```

**Default Configuration:**
- **Network Settings**: The system scans `192.168.20.0/24` by default
  - Modify the network range in the discovery agent if needed
- **GitHub Repository**: 
  - Currently configured to analyze: `https://github.com/Amruth22/W1D10S3-Agent-Deployment-RabbitMQ-queue`
  - Modify in the discovery agent to analyze different repositories

## 📁 **What Gets Created**

When you run `python main.py`, the system will automatically create:

```
outputs/
├── docs/
│   └── api_documentation.md          # Complete API documentation
├── sdks/
│   ├── python/
│   │   └── enterprise_api_client.py  # Python SDK (when generated)
│   └── javascript/
│       └── enterprise_api_client.js  # JavaScript SDK (when generated)
└── complete_output.txt               # Full system execution log
```

## 🚀 **Features**

- **Multi-Agent Orchestration**: 6 specialized AI agents working together
- **Automatic Documentation**: Generates complete API documentation
- **Multi-Language SDKs**: Creates SDKs for Python, JavaScript, and more
- **Network Discovery**: Scans local networks for API services
- **Security Compliance**: Checks for security vulnerabilities and compliance
- **Performance Monitoring**: Analyzes API performance and optimization
- **Developer Tools**: Creates interactive API explorers and developer portals
- **Integration Testing**: Validates API contracts and breaking changes
- **Quality Assurance**: Comprehensive testing and validation processes

## 📊 **Output Examples**

The system generates:
- **API Documentation** with endpoints, parameters, and examples
- **Code Samples** in multiple programming languages
- **SDK Implementations** with ready-to-use classes
- **Security Reports** with vulnerability assessments
- **Performance Analysis** with optimization recommendations

## 🐳 **Docker Deployment** (Optional)

For containerized deployment:

```bash
# Build the Docker image
docker build -t enterprise-api-ecosystem .

# Run the container
docker run -it --rm enterprise-api-ecosystem
```

## 🧪 **Testing**

Run the test suite to verify the system is working correctly:

```bash
# Run all tests
python -m pytest tests.py -v

# Run a specific test
python -m pytest tests.py::TestEnterpriseAPIEcosystem::test_01_api_key_validation -v
```

## 🛠️ **Customization**

You can customize the behavior of each agent by modifying:
- Agent prompts in the agent files
- Task definitions in the tasks directory
- Tool implementations in the tools directory
- Workflow compositions in the workflows directory

## 📈 **Monitoring**

The system provides:
- Structured JSON logging
- Performance metrics
- Audit trails for all agent actions
- Compliance event recording

## 📞 **Support**

For issues or questions:
1. Check the `outputs/complete_output.txt` for detailed execution logs
2. Verify your API keys are correctly set in `.env`
3. Ensure all dependencies are installed with `pip install -r requirements.txt`
4. Run the test suite to verify system integrity

## ✅ **System Status**

**READY FOR PRODUCTION USE** - All core components implemented and tested