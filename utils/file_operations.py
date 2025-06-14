"""
File and directory operations for mod management.
"""
import os
import shutil
from tkinter import messagebox

def copy_mod_folder(source_path, dest_path):
    """
    Copy a mod folder from source to destination, replacing if exists.
    
    Args:
        source_path (str): Path to source mod folder
        dest_path (str): Path to destination mod folder
    
    Returns:
        bool: True if successful, False otherwise
    """
    if not os.path.exists(source_path):
        messagebox.showerror("Error", f"Source folder not found: {source_path}")
        return False

    if not os.path.exists(os.path.dirname(dest_path)):
        messagebox.showerror("Error", f"Destination directory not found: {os.path.dirname(dest_path)}")
        return False

    try:
        if os.path.exists(dest_path):
            if os.path.isdir(dest_path):
                shutil.rmtree(dest_path)
            else:
                os.remove(dest_path)
        shutil.copytree(source_path, dest_path)
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to copy mod: {str(e)}")
        return False

def get_directory_contents(path):
    """
    Get list of subdirectories in a given path.
    
    Args:
        path (str): Path to check
    
    Returns:
        list: List of subdirectory names
    """
    if not path or not os.path.isdir(path):
        return []
    
    return [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

def find_matching_mods(dest_path, character_name, search_terms):
    """
    Find mods in destination folder that match character search terms.
    
    Args:
        dest_path (str): Path to destination folder
        character_name (str): Character name
        search_terms (list): List of search terms
    
    Returns:
        list: List of matching mod folder names
    """
    if not os.path.isdir(dest_path):
        return []
    
    subfolders = get_directory_contents(dest_path)
    if not subfolders:
        return []
    
    matching_subfolders = []
    
    for subfolder in subfolders:
        # Normalize subfolder name - replace special chars with spaces and lowercase
        normalized = ''.join(c if c.isalnum() else ' ' for c in subfolder).lower()
        
        # Check if any term matches
        for term in search_terms:
            if len(term) > 2 and term in normalized:  # Only check terms longer than 2 chars
                matching_subfolders.append(subfolder)
                break
    
    return matching_subfolders