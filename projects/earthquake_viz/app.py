# Redirect Streamlit to the actual entry point
import os
import sys

# Ensure app folder is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "app")))

# Run the actual Streamlit app
import main
