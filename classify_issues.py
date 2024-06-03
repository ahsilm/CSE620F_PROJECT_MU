import json
import os

categories = {
    "Contrast": ["color", "contrast", "colors"],
    "Keyboard navigation": ["keyboard", "navigation", "keys", "tabindex", "buttons", "button"],
    "Content Description": ["content", "alt text", "alternative text"],
    "Text Issues": ["labels", "text", "heading", "describedby", "labelledby"],
    "Font Issues": ["font", "font size"],
    "Links": ["link", "anchor"],
    "aria": ["assistive technology", "AT", "aria"],
    "Hearing Impairment": ["audio", "sound"],
    "General Accessibility": ["accessibility", "accessible", "screen reader", "disabled"]
}

def categorize_issues(issues_dict, categories):
    categorized_issues = []
    for issues in issues_dict.values():
        for issue in issues:
            found = False
            for category, keywords in categories.items():
                if any(keyword in issue['title'].lower() for keyword in keywords):
                    categorized_issues.append({
                        "issue_number": issue['number'],
                        "issue_title": issue['title'],
                        "issue_category": category
                    })
                    found = True
                    break
            if not found:
                categorized_issues.append({
                    "issue_number": issue['number'],
                    "issue_title": issue['title'],
                    "issue_category": "Uncategorized"
                })
    return categorized_issues


def save_categorized_issues(categorized_issues, output_file):
    with open(output_file, 'w') as f:
        json.dump(categorized_issues, f, indent=4)


root_dir = os.getcwd()
filepath = os.path.join(root_dir, 'data', 'github_cache.json')

with open(filepath, 'r') as f:
    data = json.load(f)
    issues = data['issues']

categorized_issues = categorize_issues(issues, categories)

# Save categorized issues to a JSON file
output_filepath = os.path.join(root_dir, 'data', 'categorized_issues.json')
# output_filepath = r"D:\MiamiUniversity\2nd Semester\CSE620\CSE620_PROJECT\data\categorized_issues.json"
save_categorized_issues(categorized_issues, output_filepath)

print(f"Categorized issues have been saved to {output_filepath}")
