import csv
import subprocess
import os

# Define the path to the CSV file
root_dir = os.getcwd()
csv_file_path = os.path.join(root_dir,'analysis-results','a11y-issues-count.csv')
# csv_file_path = r'D:\MiamiUniversity\2nd Semester\CSE620\CSE620_PROJECT\analysis-results\a11y-issues-count2.csv'

# Define the directory where you want to clone the repositories
clone_directory = os.path.join(root_dir,'cloned_projects')
# clone_directory = r'D:\MiamiUniversity\2nd Semester\CSE620\CSE620_PROJECT\cloned_projects'

def clone_repository(url):
    """Clones the repository from the given URL into the specified directory."""
    try:
        print(f"Cloning {url}...")
        subprocess.run(["git", "clone", url], cwd=clone_directory, check=True)
        print(f"Successfully cloned {url}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to clone {url}. Error: {e}")

def main():
    # Create the directory if it doesn't exist
    if not os.path.exists(clone_directory):
        os.makedirs(clone_directory)

    # Get a list of names of subdirectories in the specified directory
    subfolders = [f.name for f in os.scandir(clone_directory) if f.is_dir()] 
    print(subfolders)

    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
            
        reader = csv.DictReader(file)
        for row in reader:
            repo_name = row['Name'].split('/')[1]
            if repo_name not in subfolders:
                clone_repository(row['URL'])

if __name__ == "__main__":
    main()
