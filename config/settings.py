"""
Settings management for the Mod Manager.
"""
import os
import json
from .constants import SAVE_FILE

def save_data(game_paths):
    """Save game paths to JSON file."""
    try:
        with open(SAVE_FILE, 'w') as f:
            json.dump(game_paths, f, indent=2)
        return True, None
    except Exception as e:
        return False, f"Failed to save data: {str(e)}"

def load_data():
    """Load game paths from JSON file."""
    try:
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Load Error: Failed to load data: {str(e)}")
    return {}