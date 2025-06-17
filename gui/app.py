"""
Main application window for the Mod Manager.
"""
import customtkinter as ctk
from config.constants import GAME_TABS, CHARACTER_LISTS
from config.settings import load_data
from .tabs.settings_tab import SettingsTab
from .tabs.game_tab import GameTab

class App(ctk.CTk):
    """Main application class."""
    
    def __init__(self):
        super().__init__()
        self.title("Modern Mod Manager")
        self.geometry("1100x650")

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(expand=True, fill="both", padx=10, pady=10)

        self.game_paths = load_data()
        self.tabs = {}
        
        # Create tabs in specific order - Settings will be last
        self.tab_order = ["Settings"] + GAME_TABS  # Settings first in list means it will be last in UI
        
        # Create all tabs first to maintain order
        for tab_name in reversed(self.tab_order):  # Create in reverse order to maintain desired order
            self.tabview.add(tab_name)
        
        # Game tabs
        self.refresh_game_tabs()
        
        # Settings tab
        self.settings_tab = self.tabview.tab("Settings")
        self.settings_frame = SettingsTab(self.settings_tab, self.game_paths, self.refresh_game_tabs)
        self.settings_frame.pack(expand=True, fill="both")

    def refresh_game_tabs(self):
        """Refresh all game tabs with current settings."""
        # Remove old game tabs
        for game in GAME_TABS:
            if game in self.tabs:
                self.tabs[game].destroy()
                del self.tabs[game]

        # Add game tabs with current settings
        for game in GAME_TABS:
            mods_from = self.game_paths.get(game, {}).get("from", "")
            mods_to = self.game_paths.get(game, {}).get("to", "")
            character_list = CHARACTER_LISTS.get(game, [])
            
            # Get the tab frame
            tab_frame = self.tabview.tab(game)
            
            # Create a new frame inside the tab
            frame = ctk.CTkFrame(tab_frame)
            frame.pack(expand=True, fill="both")
            
            # Create the game tab with the new frame
            self.tabs[game] = frame
            game_tab = GameTab(frame, game, mods_from, mods_to, character_list)
            game_tab.pack(expand=True, fill="both")