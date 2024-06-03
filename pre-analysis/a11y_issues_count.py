import json
import csv
import os

# Path to your JSON file
root_dir = os.getcwd()
json_file_path = os.path.join(root_dir,'data','github_cache.json')
# json_file_path = r'D:\MiamiUniversity\2nd Semester\CSE620\CSE620_PROJECT\github_cache.json'

# Load the data from the JSON file
if not os.path.exists(json_file_path):
    print("File not found:", json_file_path)
else:
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Extract and analyze the data
    csv_data = [
        ["Name", "URL", "ID", "Number of Accessibility Issues"]
    ]

    for repo in data['repositories']:
        # Check if the repository has recorded issues, assume 'issues' is stored under the repo ID in your JSON structure
        repo_id = str(repo['id'])
        issues = data['issues'].get(repo_id, [])  # Assuming issues are stored with repo ID as the key
        # Filter issues for 'accessibility' label and count them
        accessibility_issues_count = sum(1 for issue in issues)
        # Append the data for CSV
        if accessibility_issues_count > 0:
            csv_data.append([repo['name'], repo['url'], repo['id'], accessibility_issues_count])

    # Save the results to a CSV file
    csv_filepath = os.path.join(root_dir,'analysis-results','a11y-issues-count.csv')
    # csv_filename = r'D:\MiamiUniversity\2nd Semester\CSE620\CSE620_PROJECT\analysis-results\a11y-issues-count2.csv'
    with open(csv_filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(csv_data)

    print(f"Data saved to {csv_filepath}")
