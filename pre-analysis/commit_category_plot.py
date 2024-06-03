# Plots a chart for "Number of commits across Issue categories"
import matplotlib.pyplot as plt
import numpy as np  # Needed for creating color intervals

categories = ['Contrast', 'Keyboard navigation', 'Links', 
              'Text Issues', 'General Accessibility', 'Content Description', 
              'aria', 'Font Issues']
counts = [57, 141, 28, 51, 80, 18, 34, 4]

colors = plt.get_cmap('viridis')(np.linspace(0, 1, len(categories)))  # Using Viridis colormap

# Plotting the bar diagram
plt.figure(figsize=(10, 6), dpi=150)  # Increase DPI for higher resolution
bars = plt.bar(categories, counts, color=colors)
plt.xlabel('Categories')
plt.ylabel('Number of Commits')
plt.title('Distribution of Commits across Issue Categories')
plt.xticks(rotation=45, ha='right')  # Adjusting text alignment for better readability

# Add text labels above the bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), va='bottom', ha='center', fontweight='bold', color='white')

plt.tight_layout()

# Save the chart as a JPG file with high quality
chart_filename = r".\analysis-results\accessibility_commits_chart.jpg"
plt.savefig(chart_filename, format='jpg' )
plt.show()