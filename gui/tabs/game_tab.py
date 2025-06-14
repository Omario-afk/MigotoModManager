"""
Game tab for managing mods for a specific game.
"""
import os
import customtkinter as ctk
from tkinter import messagebox
from utils.character_matcher import match_character
from utils.file_operations import get_directory_contents, find_matching_mods, copy_mod_folder

class GameTab(ctk.CTkFrame):
    """Game tab for mod management."""
    
    def __init__(self, master, game, mods_from, mods_to, character_list):
        super().__init__(master)
        self.game = game
        self.mods_from = mods_from
        self.mods_to = mods_to
        self.character_list = character_list
        self.character_buttons = []
        self.selected_character = None
        self.selected_mod_folder = None

        self._create_layout()
        self.populate_characters()

    def _create_layout(self):
        """Create the main layout."""
        self.character_frame = ctk.CTkFrame(self)
        self.character_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.mod_frame = ctk.CTkFrame(self)
        self.mod_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.action_frame = ctk.CTkFrame(self)
        self.action_frame.pack(side="right", fill="y", padx=10, pady=10)

        self.mod_label = ctk.CTkLabel(self.mod_frame, text="Select a character to view mods.")
        self.mod_label.pack(pady=10)

        self.current_mod_label = ctk.CTkLabel(self.mod_frame, text="")
        self.current_mod_label.pack(pady=5)

        self.action_label = ctk.CTkLabel(self.action_frame, text="Select a mod to see actions.")
        self.action_label.pack(pady=10)

    def populate_characters(self):
        """Populate the character list."""
        # Clear existing buttons
        for btn in self.character_buttons:
            btn.destroy()
        self.character_buttons.clear()

        ctk.CTkLabel(self.character_frame, text="Characters:", font=ctk.CTkFont(weight="bold")).pack(pady=5)

        if not self.mods_from or not os.path.isdir(self.mods_from):
            ctk.CTkLabel(self.character_frame, text="(Directory not found)").pack()
            return

        subfolders = get_directory_contents(self.mods_from)
        if not subfolders:
            ctk.CTkLabel(self.character_frame, text="(No character folders found)").pack()
            return

        for folder in subfolders:
            matched = match_character(folder, self.character_list)
            btn = ctk.CTkButton(
                self.character_frame, 
                text=matched, 
                width=180, 
                anchor="w",
                command=lambda f=folder, m=matched: self.show_character_mods(f, m)
            )
            btn.pack(pady=2, fill="x")
            self.character_buttons.append(btn)

    def show_character_mods(self, folder, matched_name):
        """Show mods for the selected character."""
        self.selected_character = folder
        self._clear_frames()
        
        ctk.CTkLabel(self.mod_frame, text=f"{matched_name} Mods:", font=ctk.CTkFont(weight="bold")).pack(pady=5)
        
        # Create a frame for available mods
        mods_container = ctk.CTkFrame(self.mod_frame)
        mods_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        char_path = os.path.join(self.mods_from, folder)
        if not os.path.isdir(char_path):
            ctk.CTkLabel(mods_container, text="(Character folder not found)").pack()
            return
        
        subfolders = get_directory_contents(char_path)
        if not subfolders:
            ctk.CTkLabel(mods_container, text="(No mod folders)").pack()
            return
        
        # Display all available mods
        for sub in subfolders:
            btn = ctk.CTkButton(
                mods_container, 
                text=sub, 
                anchor="w",
                command=lambda s=sub: self.select_mod_folder(s)
            )
            btn.pack(fill="x", padx=10, pady=2)
        
        # Add a separator
        ctk.CTkFrame(self.mod_frame, height=2).pack(fill="x", padx=5, pady=10)
        
        # Display current mod in "to" folder at the bottom
        self._create_current_mod_section(folder)

    def _clear_frames(self):
        """Clear mod and action frames."""
        for widget in self.mod_frame.winfo_children():
            widget.destroy()
        self.current_mod_label = ctk.CTkLabel(self.mod_frame, text="")
        self.current_mod_label.pack(pady=5)
        for widget in self.action_frame.winfo_children():
            widget.destroy()
        self.action_label = ctk.CTkLabel(self.action_frame, text="Select a mod to see actions.")
        self.action_label.pack(pady=10)

    def _create_current_mod_section(self, folder):
        """Create the current mod display section."""
        current_mod_frame = ctk.CTkFrame(self.mod_frame)
        current_mod_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(
            current_mod_frame, 
            text="Current Mod in Game Folder:", 
            font=ctk.CTkFont(weight="bold")
        ).pack(pady=5)
        
        self.current_mod_label = ctk.CTkLabel(current_mod_frame, text="")
        self.current_mod_label.pack(pady=5)
        
        self.display_current_mod(folder)

    def display_current_mod(self, character_folder):
        """Display the current mod in the destination folder."""
        if not self.mods_to:
            self.current_mod_label.configure(text="Destination folder not set.")
            return

        if not os.path.isdir(self.mods_to):
            self.current_mod_label.configure(text="Destination folder not found.")
            return

        # Get the character name and create search terms
        matched_name = match_character(character_folder, self.character_list)
        search_terms = matched_name.lower().split()
        
        # Find matching mods
        matching_subfolders = find_matching_mods(self.mods_to, matched_name, search_terms)
        
        if not matching_subfolders:
            self.current_mod_label.configure(text="No matching mods found.")
            return

        # Display each matching subfolder on a new line
        mod_text = "\n".join(matching_subfolders)
        self.current_mod_label.configure(text=mod_text)

    def select_mod_folder(self, mod_folder):
        """Select a mod folder for actions."""
        self.selected_mod_folder = mod_folder

        for widget in self.action_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self.action_frame, 
            text=f"Selected: {mod_folder}", 
            font=ctk.CTkFont(weight="bold")
        ).pack(pady=10)

        replace_btn = ctk.CTkButton(
            self.action_frame, 
            text="Replace",
            command=self.replace_mod, 
            fg_color="orange", 
            hover_color="darkorange"
        )
        replace_btn.pack(pady=10)

    def replace_mod(self):
        """Replace the mod in the destination folder."""
        if not self.selected_character or not self.selected_mod_folder:
            messagebox.showerror("Error", "No mod selected.")
            return

        source_path = os.path.join(self.mods_from, self.selected_character, self.selected_mod_folder)
        dest_path = os.path.join(self.mods_to, self.selected_mod_folder)

        if copy_mod_folder(source_path, dest_path):
            messagebox.showinfo("Success", f"Successfully replaced '{self.selected_mod_folder}' in the destination folder!")
            # Refresh the current mod display
            self.display_current_mod(self.selected_character)