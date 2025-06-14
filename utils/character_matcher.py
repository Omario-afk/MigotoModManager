"""
Character name matching utilities.
"""
from difflib import get_close_matches
import re

def match_character(name, character_list):
    """
    Match a character name against a list of known characters.
    Uses multiple matching strategies for better accuracy.
    
    Args:
        name (str): The character name to match
        character_list (list): List of known character names
    
    Returns:
        str: The matched character name or original name if no match
    """
    if not name or not character_list:
        return name
    
    # Clean the input name for matching
    cleaned_name = clean_name_for_matching(name)
    
    # Strategy 1: Direct substring match (case insensitive)
    for character in character_list:
        if character.lower() in cleaned_name.lower() or cleaned_name.lower() in character.lower():
            return character
    
    # Strategy 2: Word-based matching
    name_words = cleaned_name.lower().split()
    for character in character_list:
        character_words = character.lower().split()
        for char_word in character_words:
            if len(char_word) > 2:  # Only check meaningful words
                for name_word in name_words:
                    if char_word in name_word or name_word in char_word:
                        return character
    
    # Strategy 3: Fuzzy matching with lower cutoff
    matches = get_close_matches(cleaned_name, character_list, n=1, cutoff=0.4)
    if matches:
        return matches[0]
    
    # Strategy 4: Fuzzy matching against individual words
    for character in character_list:
        character_words = character.lower().split()
        for char_word in character_words:
            if len(char_word) > 2:
                matches = get_close_matches(cleaned_name.lower(), [char_word], n=1, cutoff=0.4)
                if matches:
                    return character
    
    return name

def clean_name_for_matching(name):
    """
    Clean a name for better matching by removing common mod suffixes/prefixes.
    
    Args:
        name (str): The name to clean
    
    Returns:
        str: Cleaned name
    """
    # Remove common mod-related terms
    mod_terms = ['mod', 'skin', 'costume', 'outfit', 'fix', 'v1', 'v2', 'v3', 'final', 'update']
    
    # Replace underscores and dashes with spaces
    cleaned = re.sub(r'[_\-]', ' ', name)
    
    # Remove numbers at the end (like "14fix")
    cleaned = re.sub(r'\d+\w*$', '', cleaned)
    
    # Remove mod terms
    words = cleaned.split()
    filtered_words = [word for word in words if word.lower() not in mod_terms]
    
    return ' '.join(filtered_words).strip()