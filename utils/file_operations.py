"""
File and directory operations for mod management.
"""
import os
import shutil
from tkinter import messagebox
from config.constants import CHARACTER_LISTS
from utils.character_matcher import match_character

def copy_mod_folder(source_path, dest_path, game_name=None):
    print("source path:", source_path)
    print("destination path:", dest_path)
    
    """
    Copy a mod folder from source to destination, organizing by character subdirectories.
    Uses the source folder structure to determine the target character folder.
    
    Args:
        source_path (str): Path to source mod folder
        dest_path (str): Path to destination mod folder
        game_name (str, optional): Game name for character matching (used as fallback)
    
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
        dest_dir = os.path.dirname(dest_path)
        mod_folder_name = os.path.basename(source_path)
        
        # Get the character folder name from the source path
        source_dir = os.path.dirname(source_path)
        character_folder = os.path.basename(source_dir)
        
        # Create character-specific subdirectory if it doesn't exist
        character_dir = os.path.join(dest_dir, character_folder)
        if not os.path.exists(character_dir):
            os.makedirs(character_dir)
        
        # Update destination path to be in character subdirectory
        dest_path = os.path.join(character_dir, mod_folder_name)
        
        # Find existing mods for this character using find_matching_mods
        existing_mods = find_matching_mods(dest_dir, character_folder, [character_folder])
        
        # Remove all matching mods but preserve the character directory
        for mod_path in existing_mods:
            full_mod_path = os.path.join(dest_dir, mod_path)
            print(f"Removing existing mod: {full_mod_path}")
            if os.path.exists(full_mod_path):
                shutil.rmtree(full_mod_path)
        
        # Copy the new mod
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
    Searches within character-specific subdirectories.
    
    Args:
        dest_path (str): Path to destination folder
        character_name (str): Character folder name
        search_terms (list): List of search terms (unused in new system)
    
    Returns:
        list: List of matching mod folder names
    """
    if not os.path.isdir(dest_path):
        return []
    
    # Get the character directory
    character_dir = os.path.join(dest_path, character_name)
    if not os.path.isdir(character_dir):
        return []
    
    # Get all mod folders within the character directory
    mod_folders = get_directory_contents(character_dir)
    if not mod_folders:
        return []
    
    # Return full relative paths for all mods in the character directory
    return [os.path.join(character_name, mod_folder) for mod_folder in mod_folders]