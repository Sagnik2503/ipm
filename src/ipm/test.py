import json

# Define the file path
file_path = "/Users/sagniksengupta/Documents/CrewAI/ipm/output/project_overview.json"

# Read the JSON file and extract the project description
def extract_project_description(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)  # Load JSON data
            return data.get("project_description", "No description found.")  # Extract project_description
    except FileNotFoundError:
        return "Error: File not found."
    except json.JSONDecodeError:
        return "Error: Invalid JSON format."

# Get project description
project_description = extract_project_description(file_path)
print(project_description) 
print(type(project_description))