import os
import subprocess

# Define the path to the main script
main_script_path = os.path.join(os.path.dirname(__file__), 'app', 'main.py')

# Check if the file exists
if not os.path.isfile(main_script_path):
    raise FileNotFoundError(f"main.py not found at {main_script_path}")

# Run the main script with Streamlit
subprocess.run(['streamlit', 'run', main_script_path], check=True)