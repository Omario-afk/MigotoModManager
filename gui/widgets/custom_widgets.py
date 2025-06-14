"""
Custom widget implementations for the Mod Manager.
"""
import customtkinter as ctk

class ModButton(ctk.CTkButton):
    """Custom button for mod selection."""
    
    def __init__(self, master, mod_name, on_click, **kwargs):
        super().__init__(master, text=mod_name, command=lambda: on_click(mod_name), **kwargs)
        self.mod_name = mod_name

class CharacterButton(ctk.CTkButton):
    """Custom button for character selection."""
    
    def __init__(self, master, character_name, folder_name, on_click, **kwargs):
        super().__init__(master, text=character_name, command=lambda: on_click(folder_name, character_name), **kwargs)
        self.character_name = character_name
        self.folder_name = folder_name