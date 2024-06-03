# CSE 620F Project 
## Project Title: Identifying and Mining Issues Related to Accessibility in Open-source Projects on GitHub and Classifying their Fixing Commits

## Environment

- OS: Windows 11
- Programming Language: Python 3.12.2

#### A. Using PyGithub library for Github APIs requires github access token. Replace GITHUB_ACCESS_TOKEN in .env file with a valid github access token. 

#### B. main.py executes the python scripts for mining and extracting the data from Github
#### C. pre-analysis directory contains scripts for  data analysis 
#### D. analysis-results contains the results from the data analysis

#### Removed cloned_projects folder to exclude it when zipping the project folder

-----------------------------------------------------------------------------------------

To create virtual environment in Windows, run the following command

>   python -m venv  .venv

Activate the virtual env in Windows machine, run the following

> .venv/Scripts/activate

To create virutal environment and activate in Linux, run the following commands
>   virtualenv venv
>   source venv/bin/activate 

If virutalenv package not installed, then install the package

>   pip install virutalenv


-------------------------------------------------------------------------------------------

Install requirements.txt

>   pip install -r requirements.txt
-------------------------------------------------------------------------------------------
Using GITHUB API needs Github API token.
Edit .env file to assign GITHUB_ACCESS_TOKEN your API token. For example:

>   GITHUB_ACCESS_TOKEN=yourapitoken  

Replace yourapitoken with your actual github api key

-------------------------------------------------------------------------------------------

To run main.py, run the following command :

>   python main.py
-------------------------------------------------------------------------------------------

1. The first step consists mining  issues from github.
- *extract_issues.py* file contains the script to mine issues which have closed status from the open-source JS projects in Github.
- Output : Produces *github_cache.json* file stored in data directory

2. Classification of issues into categories
- *classify_issues.py* file contains the script to group the issues into the respective categories
- Output : Produces *categorized_issues.json* file stored in data directory

3. Fetch commits corresponding to the issues referenced by issue#
- *fetch_commits.py* contains the script to fetch the corresponding commits for the issues refernced by their issue#
- Output : Produces *categorized_issues.json* file stored in data directory

4. Categorize commits into their corresponding issue category
- *categorize_commits.py* inside *./pre-analysis* folder contains the script to group the commits into its respective issue category
- Output: Produces *categorized_commits.json* file in data directory and commit_count_by_category.csv in analysis-results directory

5. Clone the projects
- *clone_projects.py* contains the script to clone the projects that had issues related to accessibility
- Output: *cloned_projects* directory which contains the cloned projects


6. Gather the code changes for the commits from the cloned projects
- *commit_changes.py* contains the script to gather the code changes for the commits from the cloned projects
- uses git show commit_sha and extracts the deleted(-) and added(+) part from the changed files
- Output: Produces *commit_changes_by_category.json* in data directory which contains the lines of code changes for the commits

7. pre-analysis folder contains scripts for analyzing the data
- *a11y_issues_count.py* contains script to count the issue by category
- *categorize_commits* contains script to categorize the commits to their respective issue category
- *commit_category_plot* contains script to plot count of commits by category graph
- *issue_category_plot* contains script to plot count of issues by category graph

8. analysis-results folder contains the results obtained from the analysis scripts



