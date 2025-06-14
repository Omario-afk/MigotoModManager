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

        # Settings tab
        self.settings_tab = self.tabview.add("Settings")
        self.settings_frame = SettingsTab(self.settings_tab, self.game_paths, self.refresh_game_tabs)
        self.settings_frame.pack(expand=True, fill="both")

        # Game tabs
        self.refresh_game_tabs()

    def refresh_game_tabs(self):
        """Refresh all game tabs with current settings."""
        # Remove old game tabs
        for game in GAME_TABS:
            if game in self.tabs:
                self.tabview.delete(game)
                del self.tabs[game]

        # Add game tabs with current settings
        for game in GAME_TABS:
            mods_from = self.game_paths.get(game, {}).get("from", "")
            mods_to = self.game_paths.get(game, {}).get("to", "")
            character_list = CHARACTER_LISTS.get(game, [])
            tab = self.tabview.add(game)
            self.tabs[game] = tab
            game_tab = GameTab(tab, game, mods_from, mods_to, character_list)
            game_tab.pack(expand=True, fill="both")