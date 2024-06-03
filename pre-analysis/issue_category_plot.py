# Plots a chart for "Number of issues by defined categories"

import json
import matplotlib.pyplot as plt
import numpy as np  # Needed for creating color intervals
import os

# Get the directory of the current script
root_dir = os.getcwd()
# Join the script directory with the relative path to the JSON file

filepath = os.path.join(root_dir, 'data', 'categorized_issues.json')
print(filepath)
# Load categorized issues from the JSON file
with open(filepath, 'r') as f:
    categorized_issues = json.load(f)

# Count the frequency of each category
category_counts = {}
for issue in categorized_issues:
    category = issue['issue_category']
    if category in category_counts:
        category_counts[category] += 1
    else:
        category_counts[category] = 1

# Prepare data for plotting
categories = list(category_counts.keys())
categories.remove('Uncategorized')
counts = [category_counts[cat] for cat in categories]
colors = plt.get_cmap('viridis')(np.linspace(0, 1, len(categories)))  # Using Viridis colormap

# Plotting the bar diagram
plt.figure(figsize=(10, 6), dpi=150)  # Increase DPI for higher resolution
bars = plt.bar(categories, counts, color=colors)
plt.xlabel('Categories')
plt.ylabel('Number of Issues')
plt.title('Distribution of Accessibility Issue Categories')
plt.xticks(rotation=45, ha='right')  # Adjusting text alignment for better readability

# Add text labels above the bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), va='bottom', ha='center', fontweight='bold', color='white')

plt.tight_layout()

# Save the chart as a JPG file with high quality
chart_filename = r".\analysis-results\accessibility_issues_chart.jpg"
plt.savefig(chart_filename, format='jpg' )#, quality=95)  # Set quality for JPG
plt.show()