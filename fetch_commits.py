import json
from github import Github
import os
import re

# Initialize GitHub with your token
github_access_token = os.getenv('GITHUB_ACCESS_TOKEN')
g = Github(github_access_token)



def fetch_commits_for_issue(repo, issue_number, commits):
    relevant_commits = []
    
   # Prepare a regex pattern to match the exact issue number in commit messages
    # This pattern looks for the issue number preceded by a # and either followed by a space, punctuation, or end of line
    pattern = re.compile(r'\B#' + str(issue_number) + r'\b')

    for commit in commits:
        # Search for the pattern in the commit message
        if re.search(pattern, commit.commit.message):
            print("Commit reference found.")
            relevant_commits.append({
                "sha": commit.sha,
                "message": commit.commit.message,
                "date": commit.commit.author.date.strftime("%Y-%m-%d %H:%M:%S"),
                "url": commit.html_url
            })
    print(f"Number of commits fetched for {issue_number}: {len(relevant_commits)}")
    print(relevant_commits)
    rate_limit = g.get_rate_limit()
    print(rate_limit.core)
    return relevant_commits

def load_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def save_data(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def append_data(repo_data, filename):
    """ Append a single repository's data to the JSON file. """
    try:
        with open(filename, 'r+') as file:
            file_data = json.load(file)  # Load existing data
            file_data['repositories'].append(repo_data)
            file.seek(0)  # Rewind to the beginning of the file
            json.dump(file_data, file, indent=4)
            file.truncate()  # Truncate file to new data size
    except json.JSONDecodeError:
        # Handle empty file by initializing the file with the data
        with open(filename, 'w') as file:
            json.dump({'repositories': [repo_data]}, file, indent=4)
    except FileNotFoundError:
        # If the file does not exist, create it with the data
        with open(filename, 'w') as file:
            json.dump({'repositories': [repo_data]}, file, indent=4)



def find_repo_by_id(repo_id, data):
    """Find repository data by ID."""
    for repo in data['repositories']:
        if str(repo['id']) == str(repo_id):
            return repo
    return None  # Return None if no repository matches

def process_repository(repo_data, repo, issues):
    """Process individual repository and return the processed data."""
    processed_data = {'name': repo_data['name'], 'issues': []}
    commits = repo.get_commits()
    print("GET COMMITS SUCCESSFUL", commits)
    for issue_data in issues:
        issue_number = issue_data['number']
        fetched_commits = fetch_commits_for_issue(repo, issue_number, commits)
        # commits = fetch_commits_for_issue(repo, 4163, commits)
        if fetched_commits:
            issue_data['commits'] = fetched_commits
            processed_data['issues'].append(issue_data)
    print("PROCESSED DATA:", processed_data)
    return processed_data

def main():

    root_dir = os.getcwd()
    data_filename = os.path.join(root_dir, 'data', 'github_cache.json')
    output_filename = os.path.join(root_dir, 'data', 'commits_output.json')
    
    # Check if the output file already exists
    if os.path.exists(output_filename):
        print("Output file already exists. Skipping extraction.")
    else:
        data = load_data(data_filename)
        for repo_id, issues in data['issues'].items():
            try:
                if len(issues) > 0:
                
                    print(f'Repository ID: {repo_id}')
                    repo_data = find_repo_by_id(repo_id, data)

                    if repo_data:
                        repo = g.get_repo(repo_data['name'])
                        print(f"Fetching for repository {repo_data['name']}")
                        output_data = process_repository(repo_data, repo, issues)
                        print("Data to be written:", output_data)
                        append_data(output_data, output_filename)  # Save each repository's data after processing
                        
                    else:
                        print(f"No repository data found for ID {repo_id}")
                    
            except Exception as e:
                print(f"Error processing {repo_data['name']}: {e}")


if __name__ == "__main__":
    main()
    