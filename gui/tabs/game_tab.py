"""
Game tab for managing mods for a specific game.
"""
import os
import customtkinter as ctk
from tkinter import messagebox
from utils.character_matcher import match_character
from utils.file_operations import get_directory_contents, find_matching_mods, copy_mod_folder
from gui.widgets.custom_widgets import CharacterImageButton

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
        # Character frame with scrollable area
        self.character_frame = ctk.CTkScrollableFrame(self, width=300, height=400)
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
        self._clear_frames()
        
        ctk.CTkLabel(
            self.mod_frame, 
            text=f"{matched_name} Mods:", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=10)
        
        # Create a frame for available mods
        mods_container = ctk.CTkScrollableFrame(self.mod_frame)
        mods_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        char_path = os.path.join(self.mods_from, folder)
        if not os.path.isdir(char_path):
            ctk.CTkLabel(mods_container, text="(Character folder not found)").pack()
        else:
            subfolders = get_directory_contents(char_path)
            if not subfolders:
                ctk.CTkLabel(mods_container, text="(No mod folders)").pack()
            else:
                # Display all available mods
                for sub in subfolders:
                    btn = ctk.CTkButton(
                        mods_container, 
                        text=sub, 
                        anchor="w",
                        height=35,
                        font=ctk.CTkFont(size=12),
                        command=lambda s=sub: self.select_mod_folder(s)
                    )
                    btn.pack(fill="x", padx=10, pady=3)
        
        # Add a separator
        separator = ctk.CTkFrame(self.mod_frame, height=2)
        separator.pack(fill="x", padx=5, pady=15)
        
        # Display current mod in "to" folder at the bottom
        self._create_current_mod_section(folder)
        
        # Add another separator
        separator2 = ctk.CTkFrame(self.mod_frame, height=2)
        separator2.pack(fill="x", padx=5, pady=15)
        
        # Create download section
        self._create_download_section(folder)

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
            text="Currently Installed:", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(10, 5))
        
        self.current_mod_label = ctk.CTkLabel(
            current_mod_frame, 
            text="",
            font=ctk.CTkFont(size=11),
            wraplength=300
        )
        self.current_mod_label.pack(pady=(0, 10))
        
        # Create download section
        #self._create_download_section(current_mod_frame, folder)
        
        self.display_current_mod(folder)

    def _create_download_section(self, character_folder):
        """Create the download section with its own frame."""
        download_frame = ctk.CTkFrame(self.mod_frame)
        download_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(
            download_frame,
            text="Download More Mods",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(10, 5))
        
        # Add Download More button
        download_btn = ctk.CTkButton(
            download_frame,
            text="Browse GameBanana",
            command=lambda: self.download_more_mods(character_folder),
            fg_color=("green", "darkgreen"),
            hover_color=("darkgreen", "green"),
            height=35,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        download_btn.pack(pady=10)

    def download_more_mods(self, character_folder):
        """Handle downloading more mods for the selected character."""
        matched_name = match_character(character_folder, self.character_list)
        # TODO: Implement the download functionality
        messagebox.showinfo(
            "Download More",
            f"Download functionality for {matched_name} will be implemented here."
        )

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

        # Selected mod info
        info_frame = ctk.CTkFrame(self.action_frame)
        info_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            info_frame, 
            text="Selected Mod:", 
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(pady=(10, 5))
        
        ctk.CTkLabel(
            info_frame, 
            text=mod_folder, 
            font=ctk.CTkFont(size=11),
            wraplength=180
        ).pack(pady=(0, 10))

        # Replace button
        replace_btn = ctk.CTkButton(
            self.action_frame, 
            text="Replace Mod",
            command=self.replace_mod, 
            fg_color=("orange", "darkorange"), 
            hover_color=("darkorange", "orange"),
            height=40,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        replace_btn.pack(pady=20)

    def replace_mod(self):
        """Replace the mod in the destination folder."""
        if not self.selected_character or not self.selected_mod_folder:
            messagebox.showerror("Error", "No mod selected.")
            return

        source_path = os.path.join(self.mods_from, self.selected_character, self.selected_mod_folder)
        dest_path = os.path.join(self.mods_to, self.selected_mod_folder)

        if copy_mod_folder(source_path, dest_path, self.game):
            messagebox.showinfo(
                "Success", 
                f"Successfully installed '{self.selected_mod_folder}'!\n\n"
                f"The mod has been copied to your game directory."
            )
            # Refresh the current mod display
            self.display_current_mod(self.selected_character)