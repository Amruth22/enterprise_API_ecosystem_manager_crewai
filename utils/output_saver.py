import os
import json
from datetime import datetime

def ensure_directory_exists(directory):
    """Ensure that a directory exists, creating it if necessary."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_output_to_file(content, filename, directory="outputs"):
    """Save content to a file in the specified directory."""
    # Ensure the directory exists
    full_directory = os.path.join(directory)
    ensure_directory_exists(full_directory)
    
    # Create the full file path
    file_path = os.path.join(full_directory, filename)
    
    # Save the content
    try:
        if isinstance(content, dict):
            # If content is a dictionary, save as JSON
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=2, ensure_ascii=False)
        else:
            # Save as text
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(content))
        
        print(f"Output saved to: {file_path}")
        return file_path
    except Exception as e:
        print(f"Error saving output to {file_path}: {str(e)}")
        return None

def save_sdk(sdk_content, language, directory="outputs/sdks"):
    """Save SDK content to appropriate language directory."""
    # Ensure the SDK directory exists
    lang_directory = os.path.join(directory, language)
    ensure_directory_exists(lang_directory)
    
    # Save the SDK code
    filename = f"enterprise_api_client.{get_file_extension(language)}"
    file_path = os.path.join(lang_directory, filename)
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(sdk_content)
        print(f"{language.upper()} SDK saved to: {file_path}")
        return file_path
    except Exception as e:
        print(f"Error saving {language} SDK to {file_path}: {str(e)}")
        return None

def get_file_extension(language):
    """Get appropriate file extension for a programming language."""
    extensions = {
        "python": "py",
        "javascript": "js",
        "java": "java",
        "typescript": "ts",
        "go": "go",
        "csharp": "cs"
    }
    return extensions.get(language.lower(), "txt")

def save_documentation(content, format_type, directory="outputs/docs"):
    """Save documentation in various formats."""
    # Ensure the documentation directory exists
    ensure_directory_exists(directory)
    
    # Determine filename based on format
    filename = f"api_documentation.{get_doc_extension(format_type)}"
    file_path = os.path.join(directory, filename)
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"{format_type.upper()} documentation saved to: {file_path}")
        return file_path
    except Exception as e:
        print(f"Error saving {format_type} documentation to {file_path}: {str(e)}")
        return None

def get_doc_extension(format_type):
    """Get appropriate file extension for documentation format."""
    extensions = {
        "markdown": "md",
        "html": "html",
        "openapi": "yaml",
        "json": "json"
    }
    return extensions.get(format_type.lower(), "txt")

def save_security_report(report_data, directory="outputs/security"):
    """Save security analysis report."""
    # Ensure the security directory exists
    ensure_directory_exists(directory)
    
    # Create timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"security_analysis_{timestamp}.json"
    file_path = os.path.join(directory, filename)
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        print(f"Security report saved to: {file_path}")
        return file_path
    except Exception as e:
        print(f"Error saving security report to {file_path}: {str(e)}")
        return None

def save_performance_report(report_data, directory="outputs/performance"):
    """Save performance analysis report."""
    # Ensure the performance directory exists
    ensure_directory_exists(directory)
    
    # Create timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"performance_report_{timestamp}.json"
    file_path = os.path.join(directory, filename)
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        print(f"Performance report saved to: {file_path}")
        return file_path
    except Exception as e:
        print(f"Error saving performance report to {file_path}: {str(e)}")
        return None

def save_test_suite(test_data, test_type, directory="outputs/tests"):
    """Save test suite data."""
    # Ensure the tests directory exists
    test_dir = os.path.join(directory, test_type)
    ensure_directory_exists(test_dir)
    
    # Create timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{test_type}_tests_{timestamp}.json"
    file_path = os.path.join(test_dir, filename)
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, indent=2, ensure_ascii=False)
        print(f"{test_type.capitalize()} test suite saved to: {file_path}")
        return file_path
    except Exception as e:
        print(f"Error saving {test_type} test suite to {file_path}: {str(e)}")
        return None