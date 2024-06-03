from github import Github
import os
import json
from dotenv import load_dotenv
from github import RateLimitExceededException, GithubException

load_dotenv()


# Access the environment variable
github_access_token = os.getenv('GITHUB_ACCESS_TOKEN')
g = Github(github_access_token)

root_dir = os.getcwd()
filepath = os.path.join(root_dir, 'data', 'github_cache.json')

# Caching the intermediary results to a file
def load_cache(filename=filepath):
    """Load cached data from a JSON file."""
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return {}  # Return an empty dictionary if the file does not exist

def save_cache(data, filename=filepath):
    """Save data to a JSON file."""
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)



def fetch_repositories():
    """Fetch top JavaScript repositories and cache them."""
    # Load cached data
    cache = load_cache()
    
    # Check if the repositories are already fetched
    if 'repositories' not in cache:
        repositories = g.search_repositories(query="language:javascript", sort="stars", order="desc")
        repo_data = []
        for repo in repositories[:1000]:
            if repo.open_issues_count > 0:  # Check if there are any open issues
                repo_data.append({'name': repo.full_name, 'url': repo.html_url, 'id': repo.id, 'issues_count': repo.open_issues_count})
        cache['repositories'] = repo_data
        save_cache(cache)  # Save updated cache with repositories

    return cache['repositories']

repositories = fetch_repositories()
print("Fetched Repositories:", len(repositories))


def fetch_issues(repo_id, repo_name):
    """Fetch accessibility issues for a given repository and cache them."""
    cache = load_cache()
    
    # Initialize issues in cache if not present
    if 'issues' not in cache:
        cache['issues'] = {}

    if repo_id not in cache['issues']:
        repo = g.get_repo(repo_name)
        issues = repo.get_issues(state="closed", labels=["accessibility"])
        issue_data = [{'number': issue.number, 'title': issue.title, 'state': issue.state} for issue in issues]
        cache['issues'][repo_id] = issue_data
        save_cache(cache)  # Save updated cache with issues

    return cache['issues'][repo_id]

# Fetch and print issues for the repositories
if len(repositories) > 0:
    for repo in repositories[:1000]:
        issues = fetch_issues(repo['id'], repo['name'])
        print("Issues for repository:", repo['name'], len(issues))
