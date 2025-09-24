# Enterprise API Ecosystem Manager
# This system automatically discovers, documents, and creates SDKs for enterprise APIs

import os
import json
import re
from dotenv import load_dotenv
from crewai import Crew

load_dotenv()

def run_discovery_to_documentation_pipeline():
    # \"\"\"Run the discovery to documentation pipeline workflow.\"\"\"
    print("Enterprise API Ecosystem Manager")
    print("================================")
    print("Running Discovery-to-Documentation Pipeline...")
    
    # Import all agents
    from agents.api_discovery_agent import create_api_discovery_agent
    from agents.documentation_agent import create_documentation_agent
    from agents.compliance_agent import create_compliance_agent
    from agents.developer_experience_agent import create_developer_experience_agent

    # Create all agents
    api_discovery_agent = create_api_discovery_agent()
    documentation_agent = create_documentation_agent()
    compliance_agent = create_compliance_agent()
    developer_experience_agent = create_developer_experience_agent()

    # Import all tasks
    from tasks.discovery_tasks import discovery_task
    from tasks.documentation_tasks import documentation_task
    from tasks.compliance_tasks import compliance_task
    from tasks.developer_experience_tasks import developer_experience_task

    # Create the crew with all agents and tasks
    api_ecosystem_crew = Crew(
        agents=[
            api_discovery_agent,
            documentation_agent,
            compliance_agent,
            developer_experience_agent
        ],
        tasks=[
            discovery_task,
            documentation_task,
            compliance_task,
            developer_experience_task
        ],
        verbose=True
    )

    # Execute the crew and get the result
    result = api_ecosystem_crew.kickoff()
    return result

def save_complete_output(result):
    # \"\"\"Save the complete output to a text file.\"\"\"
    try:
        # Ensure outputs directory exists
        os.makedirs("outputs", exist_ok=True)
            
        # Save the result to a file
        with open("outputs/complete_output.txt", "w", encoding="utf-8") as f:
            f.write(str(result))
            
        print("[SUCCESS] Complete output saved to outputs/complete_output.txt")
        return True
        
    except Exception as e:
        print(f"[ERROR] Error saving complete output: {e}")
        return False

def extract_and_save_components(content):
    # \"\"\"Extract components from the complete output and save them separately.\"\"\"
    try:
        # Create directories
        os.makedirs("outputs/docs", exist_ok=True)
        os.makedirs("outputs/sdks/python", exist_ok=True)
        os.makedirs("outputs/sdks/javascript", exist_ok=True)
        
        print("[INFO] Extracting and saving components...")
        
        # Try to extract Python SDK
        python_sdk_pattern = r"```python\s*\n(.*?class\s+.*?Client.*?)\s*```"
        python_sdk_match = re.search(python_sdk_pattern, content, re.DOTALL | re.IGNORECASE)
        
        if python_sdk_match:
            python_sdk = python_sdk_match.group(1)
            with open("outputs/sdks/python/enterprise_api_client.py", "w", encoding="utf-8") as f:
                f.write(python_sdk)
            print("[SUCCESS] Python SDK saved to outputs/sdks/python/enterprise_api_client.py")
        else:
            print("[INFO] No Python SDK found in output")
        
        # Try to extract JavaScript SDK
        js_sdk_pattern = r"```javascript\s*\n(.*?class\s+.*?Client.*?)\s*```"
        js_sdk_match = re.search(js_sdk_pattern, content, re.DOTALL | re.IGNORECASE)
        
        if js_sdk_match:
            js_sdk = js_sdk_match.group(1)
            with open("outputs/sdks/javascript/enterprise_api_client.js", "w", encoding="utf-8") as f:
                f.write(js_sdk)
            print("[SUCCESS] JavaScript SDK saved to outputs/sdks/javascript/enterprise_api_client.js")
        else:
            print("[INFO] No JavaScript SDK found in output")
        
        # Save documentation
        with open("outputs/docs/api_documentation.md", "w", encoding="utf-8") as f:
            f.write(content)
        print("[SUCCESS] Documentation saved to outputs/docs/api_documentation.md")
        
        print("\n[SUCCESS] Component extraction and saving completed!")
        return True
        
    except Exception as e:
        print(f"[ERROR] Error extracting and saving components: {e}")
        return False

def main():
    try:
        # Run the discovery to documentation pipeline
        result = run_discovery_to_documentation_pipeline()
        
        print("\nPipeline execution completed!")
        print("=" * 50)
        
        # Save the complete output
        if save_complete_output(result):
            # Extract and save individual components
            try:
                with open("outputs/complete_output.txt", "r", encoding="utf-8") as f:
                    content = f.read()
                extract_and_save_components(content)
            except Exception as e:
                print(f"[ERROR] Error reading complete output for extraction: {e}")
        else:
            print("[ERROR] Failed to save complete output")
        
        print("\n[SUCCESS] Pipeline completed successfully!")
        print("[INFO] All outputs have been saved to the 'outputs' directory")
        
    except Exception as e:
        print(f"\n[ERROR] Pipeline failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()