import subprocess

def run_script(filename):
    print(f"Running {filename}...")
    # Run the Python file and capture the output
    result = subprocess.run(['python', filename], capture_output=True, text=True)
    # Print the stdout and stderr from the subprocess
    print("Output:")
    print(result.stdout)
    # print("Errors:")
    # print(result.stderr)
    print("-" * 60)

if __name__ == "__main__":
    scripts = [
        'extract_issues.py',
        'classify_issues.py',
        'fetch_commits.py',
        'clone_projects.py',
        'commit_changes.py'
    ]

    for script in scripts:
        run_script(script)
