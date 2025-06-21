"""
Game tab for managing mods for a specific game.
"""
import os
import re
import customtkinter as ctk
from utils.character_matcher import match_character
from utils.file_operations import get_directory_contents, find_matching_mods
from gui.widgets.custom_widgets import CharacterImageButton
from .instructions_window import InstructionsWindow
from .mod_card import ModCard
from .mod_operations import ModOperations

class GameTab(ctk.CTkFrame):
    """Game tab for mod management."""
    
    def __init__(self, master, game, mods_from, mods_to, character_list, toast_manager=None):
        super().__init__(master)
        self.game = game
        self.mods_from = mods_from
        self.mods_to = mods_to
        self.character_list = character_list
        self.toast_manager = toast_manager
        self.character_buttons = []
        self.selected_character = None
        
        # Initialize mod operations
        self.mod_operations = ModOperations(self)

        self._create_layout()
        self.populate_characters()

    def _create_layout(self):
        """Create the main layout."""
        # Character frame with scrollable area
        self.character_frame = ctk.CTkScrollableFrame(self, width=300, height=400)
        self.character_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Main content frame
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Mods display frame
        self.mods_frame = ctk.CTkScrollableFrame(self.content_frame)
        self.mods_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Initial message
        self.initial_label = ctk.CTkLabel(
            self.mods_frame, 
            text="Select a character to view mods.",
            font=ctk.CTkFont(size=16)
        )
        self.initial_label.pack(pady=50)

    def populate_characters(self):
        """Populate the character list with image buttons."""
        # Clear existing buttons
        for btn in self.character_buttons:
            btn.destroy()
        self.character_buttons.clear()

        # Use grid for the label as well
        ctk.CTkLabel(
            self.character_frame, 
            text="Characters:", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, columnspan=2, pady=10)  # Span two columns

        if not self.mods_from or not os.path.isdir(self.mods_from):
            ctk.CTkLabel(self.character_frame, text="(Directory not found)").grid(row=1, column=0, columnspan=2)
            return

        subfolders = get_directory_contents(self.mods_from)
        if not subfolders:
            ctk.CTkLabel(self.character_frame, text="(No character folders found)").grid(row=1, column=0, columnspan=2)
            return

        # Create a grid layout for character buttons
        chars_per_row = 2  # Number of characters per row
        
        for i, folder in enumerate(subfolders):
            matched = match_character(folder, self.character_list)
            
            # Create image button
            char_btn = CharacterImageButton(
                master=self.character_frame,
                character_name=matched,
                folder_name=folder,
                game_name=self.game,
                on_click=self.show_character_mods,
                width=130,
                height=150
            )
            
            # Calculate grid position
            row = (i // chars_per_row) + 1  # Start rows after the label
            col = i % chars_per_row
            
            char_btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            self.character_buttons.append(char_btn)
    
        # Configure grid weights for responsive layout
        for col in range(chars_per_row):
            self.character_frame.grid_columnconfigure(col, weight=1)

    def show_character_mods(self, folder, matched_name):
        """Show mods for the selected character."""
        self.selected_character = folder
        
        # Clear the mods frame
        for widget in self.mods_frame.winfo_children():
            widget.destroy()
        
        # Title
        title_label = ctk.CTkLabel(
            self.mods_frame, 
            text=f"{matched_name} Mods", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(10, 20))
        
        char_path = os.path.join(self.mods_from, folder)
        if not os.path.isdir(char_path):
            ctk.CTkLabel(self.mods_frame, text="(Character folder not found)").pack()
            return
        
        subfolders = get_directory_contents(char_path)
        if not subfolders:
            ctk.CTkLabel(self.mods_frame, text="(No mods found)").pack()
            return

        # Get currently installed mods for comparison
        current_mods = self._get_current_mods(folder)
        
        # Create a frame for the grid layout
        grid_frame = ctk.CTkFrame(self.mods_frame)
        grid_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configure grid
        mods_per_row = 3
        for i in range(mods_per_row):
            grid_frame.grid_columnconfigure(i, weight=1)
        
        # Display each mod as a card
        for i, mod_folder in enumerate(subfolders):
            row = i // mods_per_row
            col = i % mods_per_row
            
            # Check if this mod is currently installed
            is_current = mod_folder in current_mods
            is_archive = mod_folder.lower().endswith(('.zip', '.rar'))
            
            print(f"Debug: Checking mod '{mod_folder}' - is_current: {is_current}")
            
            # Create mod card
            mod_card = self._create_mod_card(grid_frame, mod_folder, is_current, is_archive)
            mod_card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

    def _get_current_mods(self, character_folder):
        """Get list of currently installed mods for the character."""
        if not self.mods_to or not os.path.isdir(self.mods_to):
            print(f"Debug: No mods_to directory or not set")
            return []
        
        # Use the original character folder name, not the matched name
        # The destination directory likely uses the original folder structure
        print(f"Debug: Character folder: {character_folder}")
        
        search_terms = character_folder.lower().split()
        matching_mods = find_matching_mods(self.mods_to, character_folder, search_terms)
        print(f"Debug: Matching mods found: {matching_mods}")
        
        # Extract just the mod folder names (remove character folder prefix)
        current_mod_names = []
        for mod_path in matching_mods:
            # Split on both / and \ to get the folder name
            mod_name = re.split(r"[\\/]+", mod_path)[-1]
            current_mod_names.append(mod_name)
        
        print(f"Debug: Current mod names: {current_mod_names}")
        return current_mod_names

    def _create_mod_card(self, parent_frame, mod_folder, is_current, is_archive):
        """Create a mod card widget."""
        # Check for instructions
        has_instructions = self._check_for_instructions(mod_folder) is not None
        
        # Create callbacks dictionary
        callbacks = {
            'delete': self.mod_operations.delete_mod,
            'instructions': self._show_instructions,
            'extract': self.mod_operations.extract_mod,
            'install': self.mod_operations.install_mod
        }
        
        # Create the mod card using the ModCard helper
        return ModCard.create_mod_card(
            parent_frame, mod_folder, is_current, is_archive, 
            has_instructions, callbacks
        )

    def _check_for_instructions(self, mod_folder):
        """Check if a mod folder has an instructions file and return its content."""
        if not self.selected_character:
            return None
        
        mod_path = os.path.join(self.mods_from, self.selected_character, mod_folder)
        
        # Look for .txt files in the mod folder
        try:
            for file in os.listdir(mod_path):
                if file.lower().endswith('.txt'):
                    txt_path = os.path.join(mod_path, file)
                    with open(txt_path, 'r', encoding='utf-8', errors='ignore') as f:
                        return f.read()
        except Exception as e:
            print(f"Error reading instructions for {mod_folder}: {e}")
        
        return None

    def _show_instructions(self, mod_folder):
        """Show instructions window for a mod."""
        instructions = self._check_for_instructions(mod_folder)
        if instructions:
            InstructionsWindow(self, mod_folder, instructions)
        else:
            if self.toast_manager:
                self.toast_manager.show_toast("No instructions file found.", "info", 3000) 