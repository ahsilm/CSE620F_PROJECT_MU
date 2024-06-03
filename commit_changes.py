import json
import os
import subprocess
import re

def execute_command(command, cwd):
    """ Execute a shell command and return the output """
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, shell=False)
    if result.returncode != 0:
        print(f"Error executing command: {result.stderr}")
    else:
        print(f"Command executed successfully: {command}")
    return result.stdout

def extract_code_changes(commit_output):
    """ Extract code changes from git show output """
    if not commit_output:  # Check if commit_output is None or empty
        print("No output from git show command to process.")
        return "No code changes found."
    lines = commit_output.split('\n')
    code_changes = []
    change_pattern = re.compile(r'^[+-][^+-]')  # Matches lines starting with + or - followed by any character not a + or -
    
    for line in lines:
        if change_pattern.match(line):
            code_changes.append(line)
    
    if not code_changes:
        return "No code changes found."
    
    return "\n".join(code_changes)
  

def main():
    # Load the categorized commits data
    root_dir = os.getcwd()
    categorized_commits_file = os.path.join(root_dir,'data','categorized_commits.json') 
    base_dir = os.path.join(root_dir,'cloned_projects')
    output_file = os.path.join(root_dir,'data','commit_changes_by_category.json')
    
    with open(categorized_commits_file, 'r') as file:
        data = json.load(file)

    results = {}

    for category, entries in data.items():
        results[category] = []
        for entry in entries:
            project_name = entry['project_name'].split('/')[-1]
            project_path = os.path.join(base_dir, project_name)
            for commit in entry['commit_info']:
                sha = commit['sha']
                command = ["git", "show", sha]
                commit_output = execute_command(command, project_path)
                commit_changes = extract_code_changes(commit_output)

                commit_data = {
                    "project_name": entry['project_name'],
                    "issue_number": entry['issue_number'],
                    "commit_sha": sha,
                    "commit_message": commit['message'],
                    "code_changes": commit_changes
                }
                results[category].append(commit_data)

    # Save the results to a JSON file
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)

    print(f"Data saved to {output_file}")

if __name__ == "__main__":
    main()
