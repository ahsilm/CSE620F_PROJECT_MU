import json
import os
import csv

root_dir = os.getcwd()

first_file = os.path.join(root_dir,'data','categorized_issues.json')
second_file = os.path.join(root_dir,'data','commits_output.json') 

# first_file = r'D:\MiamiUniversity\2nd Semester\CSE620\CSE620_PROJECT\data\categorized_issues.json' 
# second_file= r'D:\MiamiUniversity\2nd Semester\CSE620\CSE620_PROJECT\data\commits_output2.json'

# Load JSON files
with open(first_file, 'r') as file:
    first_file_data = json.load(file)

with open(second_file, 'r') as file:
    second_file_data = json.load(file)

# Create a dictionary to map issue numbers to categories
issue_category_mapping = {issue['issue_number']: issue['issue_category'] for issue in first_file_data}

# Dictionary to store categorized commits
categorized_commits = {}

# Iterate through repositories
for repository in second_file_data['repositories']:
    project_name = repository['name']
    for issue in repository['issues']:
        issue_number = issue['number']
        if issue_number in issue_category_mapping:
            category = issue_category_mapping[issue_number]
            if category not in categorized_commits:
                categorized_commits[category] = []
            commit_info = {
                'project_name': project_name,
                'issue_number': issue_number,
                'issue_title': issue['title'],
                'commit_info': issue['commits']
            }
            categorized_commits[category].append(commit_info)

categorized_commits_file = os.path.join(root_dir,'data','categorized_commits.json')
# Save categorized commits to a file
with open(categorized_commits_file, 'w') as file:
    json.dump(categorized_commits, file, indent=4)

# Count number of commits in each category
commit_count_by_category = {category: sum(len(commit_info['commit_info']) for commit_info in commits) for category, commits in categorized_commits.items()}

output_file = os.path.join(root_dir,'analysis-results','commit_count_by_category.csv')
# Write data to CSV file
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Category", "Commit Count"])
    for category, count in commit_count_by_category.items():
        print(f"Category: {category}, Commit Count: {count}")
        writer.writerow([category, count])

