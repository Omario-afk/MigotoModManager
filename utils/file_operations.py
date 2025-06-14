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
    Copy a mod folder from source to destination, removing all existing mods 
    for the same character first.
    
    Args:
        source_path (str): Path to source mod folder
        dest_path (str): Path to destination mod folder
        game_name (str, optional): Game name for character matching
    
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
        
        # If game_name provided, find and remove ALL mods for the same character
        if game_name and game_name in CHARACTER_LISTS:
            character_list = CHARACTER_LISTS[game_name]
            # Identify which character this new mod is for
            target_character = match_character(mod_folder_name, character_list)
            
            print(f"New mod '{mod_folder_name}' identified as character: {target_character}")
            
            # Find ALL existing folders that match this character
            existing_folders = get_directory_contents(dest_dir)
            folders_to_remove = []
            
            for folder in existing_folders:
                folder_character = match_character(folder, character_list)
                if folder_character == target_character:
                    folders_to_remove.append(folder)
                    print(f"Found existing mod for {target_character}: {folder}")
            
            # Remove all matching folders
            for folder in folders_to_remove:
                folder_path = os.path.join(dest_dir, folder)
                print(f"Removing existing mod: {folder_path}")
                shutil.rmtree(folder_path)
                
        else:
            # Fallback to original behavior - just remove exact destination if exists
            if os.path.exists(dest_path):
                if os.path.isdir(dest_path):
                    shutil.rmtree(dest_path)
                else:
                    os.remove(dest_path)
        
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