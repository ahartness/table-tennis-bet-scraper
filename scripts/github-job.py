import os
import subprocess
import schedule
import time
from dotenv import load_dotenv

def run_command(command):
    """Runs a shell command and returns the output."""
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr.strip()}")
        raise Exception(f"Command failed: {command}")
    return result.stdout.strip()

def run_table_tennis_job():
    try:
        load_dotenv()
        github_token = os.getenv("GITHUB_TOKEN")
        if not github_token:
            raise Exception("GITHUB_TOKEN environment variable is not set")

        # Change to the repository directory
        os.chdir("./") 

        run_command(f"git remote set-url origin https://ahartness:{github_token}@github.com/ahartness/table-tennis-scraper.git")
        print(f"Using token: {github_token}")

        # Pull latest Changes
        run_command("git pull")
        print("pulled latest code")

        # Run the table tennis data job
        print("Starting Pythin script for data refresh")
        run_command("python3 -u scripts/visualizedDataScript.py run_script")
        print("completed data script run")
    except Exception as e:
        print(f"An error Occurred: {e}")

def push_to_github(repo_path, commit_message, branch="main"):
    """
    Pushes changes to GitHub.
    
    Parameters:
    - repo_path: Path to the local Git repository.
    - commit_message: Commit message for the changes.
    - branch: Branch to push to (default is 'main').
    """
    try:
        # Change to the repository directory
        os.chdir(repo_path)

        # Add changes
        run_command("git add data/all_away_plays.json data/all_plays.json data/all_home_plays.json data/all_h2h_plays.json") 
        print("Changes added to staging.")

        # Commit changes
        run_command(f"git commit -m \"{commit_message}\"")
        print("Changes committed.")

        # Push changes
        run_command(f"git push origin {branch}")
        print(f"Changes pushed to {branch} branch.")
    except Exception as e:
        print(f"An error occurred: {e}")

def run_github_script():
    # Example usage
    repo_path = "./"  # Update this to your repository's path
    commit_message = "Automated Data Refresh"  # Customize your commit message

    try:
        run_table_tennis_job()
        push_to_github(repo_path, commit_message)
    except Exception as e:
        print(f"Failed to push changes: {e}")

schedule.every().day.at("00:05").do(run_github_script)
schedule.every().day.at("12:12").do(run_github_script)

while True:
    schedule.run_pending()
    time.sleep(1)

if __name__ == "__main__":
    # Get the function argument from the command line
    if len(sys.argv) > 1:
        function_name = sys.argv[1]
        name = sys.argv[2] if len(sys.argv) > 2 else "World"

        if function_name == "run_github_script":
            run_github_script()
        else:
            print(f"Function '{function_name}' not found.")
    else:
        print("No function name provided.")
