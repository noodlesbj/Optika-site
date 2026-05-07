import os
import subprocess
import sys

def run_command(command):
    print(f"Running: {command}")
    process = subprocess.run(command, shell=True)
    if process.returncode != 0:
        print(f"Error executing: {command}")
        sys.exit(1)

def main():
    print("Starting setup for Optics Educational Platform...")
    
    # 1. Install dependencies
    run_command("pip install -r requirements.txt")
    
    # 2. Run migrations
    run_command("python manage.py makemigrations core")
    run_command("python manage.py migrate")
    
    # 3. Load initial data
    fixture_path = os.path.join("core", "fixtures", "initial_data.json")
    if os.path.exists(fixture_path):
        run_command(f"python manage.py loaddata {fixture_path}")
    else:
        print(f"Warning: Fixture file not found at {fixture_path}")
    
    print("\nSetup complete! Run: python manage.py runserver")

if __name__ == "__main__":
    main()
