"""
Mod operations for installing, extracting, and deleting mods.
"""
import os
import threading
import customtkinter as ctk
from utils.file_operations import copy_mod_folder
from utils.zip.extract import extract_archive
from gui.widgets.extraction_progress import ExtractionProgressWindow

class ModOperations:
    """Helper class for mod operations."""
    
    def __init__(self, game_tab):
        self.game_tab = game_tab
        self.progress_window = None
    
    def delete_mod(self, mod_folder):
        """Delete a mod folder."""
        if not self.game_tab.selected_character:
            if self.game_tab.toast_manager:
                self.game_tab.toast_manager.show_toast("No character selected.", "error", 3000)
            return
        
        mod_path = os.path.join(self.game_tab.mods_from, self.game_tab.selected_character, mod_folder)
        
        try:
            import shutil
            if os.path.isdir(mod_path):
                shutil.rmtree(mod_path)
            else:
                os.remove(mod_path)
            
            if self.game_tab.toast_manager:
                self.game_tab.toast_manager.show_toast(f"Deleted {mod_folder}", "success", 3000)
            
            # Refresh the mod list
            self._refresh_mod_list()
        except Exception as e:
            if self.game_tab.toast_manager:
                self.game_tab.toast_manager.show_toast(f"Failed to delete {mod_folder}: {str(e)}", "error", 5000)

    def extract_mod(self, mod_folder):
        """Extract an archive mod."""
        if not self.game_tab.selected_character:
            if self.game_tab.toast_manager:
                self.game_tab.toast_manager.show_toast("No character selected.", "error", 3000)
            return

        char_path = os.path.join(self.game_tab.mods_from, self.game_tab.selected_character)
        archive_path = os.path.join(char_path, mod_folder)
        
        # Create progress window
        self.progress_window = ExtractionProgressWindow(self.game_tab, total_files=1)
        
        # Start extraction in a separate thread
        thread = threading.Thread(
            target=self._extract_archive_thread,
            args=(archive_path, char_path, mod_folder),
            daemon=True
        )
        thread.start()

    def _extract_archive_thread(self, archive_path, char_path, mod_folder):
        """Thread function for archive extraction."""
        success = extract_archive(archive_path, char_path, self.progress_window)
        
        if success:
            self.progress_window.update_progress(mod_folder, True)
            if self.game_tab.toast_manager:
                self.game_tab.toast_manager.show_toast(
                    f"Successfully extracted {mod_folder}!",
                    "success",
                    3000
                )
            # Refresh the mod list after a short delay
            self.game_tab.after(1000, self._refresh_mod_list)
        else:
            self.progress_window.update_progress(mod_folder, False)
            if self.game_tab.toast_manager:
                self.game_tab.toast_manager.show_toast(
                    f"Failed to extract {mod_folder}.",
                    "error",
                    5000
                )

    def install_mod(self, mod_folder):
        """Install a mod folder."""
        if not self.game_tab.selected_character:
            if self.game_tab.toast_manager:
                self.game_tab.toast_manager.show_toast("No character selected.", "error", 3000)
            return

        source_path = os.path.join(self.game_tab.mods_from, self.game_tab.selected_character, mod_folder)
        dest_path = os.path.join(self.game_tab.mods_to, mod_folder)

        if copy_mod_folder(source_path, dest_path, self.game_tab.game):
            if self.game_tab.toast_manager:
                self.game_tab.toast_manager.show_toast(
                    f"Successfully installed '{mod_folder}'!\nThe mod has been copied to your game directory.",
                    "success",
                    4000
                )
            # Refresh the mod list to update the green border
            self._refresh_mod_list()
        else:
            if self.game_tab.toast_manager:
                self.game_tab.toast_manager.show_toast(
                    f"Failed to install '{mod_folder}'.",
                    "error",
                    5000
                )
    
    def _refresh_mod_list(self):
        """Refresh the mod list display."""
        from utils.character_matcher import match_character
        self.game_tab.show_character_mods(
            self.game_tab.selected_character,
            match_character(self.game_tab.selected_character, self.game_tab.character_list)
        ) 