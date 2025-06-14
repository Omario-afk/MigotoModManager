"""
Settings management for the Mod Manager.
"""
import os
import json
from tkinter import messagebox
from .constants import SAVE_FILE

def save_data(game_paths):
    """Save game paths to JSON file."""
    try:
        with open(SAVE_FILE, 'w') as f:
            json.dump(game_paths, f, indent=2)
    except Exception as e:
        messagebox.showerror("Save Error", f"Failed to save data: {str(e)}")

def load_data():
    """Load game paths from JSON file."""
    try:
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        messagebox.showerror("Load Error", f"Failed to load data: {str(e)}")
    return {}