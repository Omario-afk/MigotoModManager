"""
Character name matching utilities.
"""
from difflib import get_close_matches

def match_character(name, character_list):
    """
    Match a character name against a list of known characters.
    
    Args:
        name (str): The character name to match
        character_list (list): List of known character names
    
    Returns:
        str: The matched character name or original name if no match
    """
    matches = get_close_matches(name, character_list, n=1, cutoff=0.6)
    return matches[0] if matches else name