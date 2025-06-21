"""
Game tab for managing mods for a specific game.
"""
import os
import threading
import customtkinter as ctk
from PIL import Image
from utils.character_matcher import match_character
from utils.file_operations import get_directory_contents, find_matching_mods, copy_mod_folder
from gui.widgets.custom_widgets import CharacterImageButton
from utils.zip.extract import extract_archive
from gui.widgets.extraction_progress import ExtractionProgressWindow
import re

class InstructionsWindow(ctk.CTkToplevel):
    """Window to display mod instructions."""
    
    def __init__(self, parent, mod_name, instructions_text):
        super().__init__(parent)
        self.title(f"Instructions - {mod_name}")
        self.geometry("500x400")
        self.resizable(True, True)
        
        # Make it modal
        self.transient(parent)
        self.grab_set()
        
        # Create layout
        self._create_layout(instructions_text)
        
        # Center the window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.winfo_screenheight() // 2) - (400 // 2)
        self.geometry(f"500x400+{x}+{y}")

    def _create_layout(self, instructions_text):
        """Create the window layout."""
        # Title
        title_label = ctk.CTkLabel(
            self, 
            text="Mod Instructions", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(20, 10))
        
        # Instructions text area
        text_area = ctk.CTkTextbox(
            self,
            width=460,
            height=300,
            font=ctk.CTkFont(size=12)
        )
        text_area.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Insert the instructions text
        text_area.insert("1.0", instructions_text)
        text_area.configure(state="disabled")  # Make it read-only
        
        # Close button
        close_btn = ctk.CTkButton(
            self,
            text="Close",
            command=self.destroy,
            width=100
        )
        close_btn.pack(pady=(0, 20))

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
        self.progress_window = None

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
        # Main card frame
        card_frame = ctk.CTkFrame(
            parent_frame,
            width=200,
            height=280,  # Back to original height
            corner_radius=10
        )
        
        # Add green background if currently installed
        if is_current:
            card_frame.configure(fg_color=("lightgreen", "darkgreen"))
        
        # Image frame - back to original proportions
        image_frame = ctk.CTkFrame(card_frame, height=150, corner_radius=8)
        image_frame.pack(fill="x", padx=10, pady=(10, 5))
        image_frame.pack_propagate(False)
        
        # Image (placeholder for now)
        if is_archive:
            image_path = "assets/static/file-archive.png"
        else:
            image_path = "assets/static/placeholder.webp"
        
        try:
            image = ctk.CTkImage(
                light_image=Image.open(image_path),
                dark_image=Image.open(image_path),
                size=(180, 140)
            )
            image_label = ctk.CTkLabel(image_frame, image=image, text="")
            image_label.pack(expand=True, fill="both", padx=5, pady=5)
        except Exception as e:
            # Fallback if image fails to load
            image_label = ctk.CTkLabel(
                image_frame, 
                text="📁" if not is_archive else "📦",
                font=ctk.CTkFont(size=48)
            )
            image_label.pack(expand=True, fill="both")
        
        # Mod name - this will expand to fill available space
        mod_display_name = mod_folder
        if is_current:
            mod_display_name += " (Current)"
            
        name_label = ctk.CTkLabel(
            card_frame,
            text=mod_display_name,
            font=ctk.CTkFont(size=12, weight="bold"),
            wraplength=180
        )
        name_label.pack(pady=(0, 5), fill="x", expand=True)
        
        # Action buttons frame - stuck to bottom
        buttons_frame = ctk.CTkFrame(card_frame, height=40)
        buttons_frame.pack(fill="x", padx=10, pady=(0, 10), side="bottom")
        buttons_frame.pack_propagate(False)
        
        # Delete button with trash icon
        try:
            delete_icon = ctk.CTkImage(
                light_image=Image.open("assets/static/trash-2.png"),
                dark_image=Image.open("assets/static/trash-2.png"),
                size=(16, 16)
            )
            delete_btn = ctk.CTkButton(
                buttons_frame,
                image=delete_icon,
                text="",
                width=30,
                height=30,
                fg_color="red",
                hover_color="darkred",
                command=lambda: self._delete_mod(mod_folder)
            )
        except Exception as e:
            # Fallback to text if icon fails to load
            delete_btn = ctk.CTkButton(
                buttons_frame,
                text="🗑️",
                width=30,
                height=30,
                font=ctk.CTkFont(size=14),
                fg_color="red",
                hover_color="darkred",
                command=lambda: self._delete_mod(mod_folder)
            )
        delete_btn.pack(side="left", padx=(5, 0))
        
        # Right side buttons frame (for info and action buttons)
        right_buttons_frame = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        right_buttons_frame.pack(side="right", padx=(0, 5))
        
        # Instructions button (only for folders, not archives)
        if not is_archive:
            has_instructions = self._check_for_instructions(mod_folder) is not None
            try:
                info_icon = ctk.CTkImage(
                    light_image=Image.open("assets/static/info.png"),
                    dark_image=Image.open("assets/static/info.png"),
                    size=(16, 16)
                )
                instructions_btn = ctk.CTkButton(
                    right_buttons_frame,
                    image=info_icon,
                    text="",
                    width=30,
                    height=30,
                    fg_color="blue" if has_instructions else "gray",
                    hover_color="darkblue" if has_instructions else "darkgray",
                    command=lambda: self._show_instructions(mod_folder) if has_instructions else None,
                    state="normal" if has_instructions else "disabled"
                )
            except Exception as e:
                # Fallback to text if icon fails to load
                instructions_btn = ctk.CTkButton(
                    right_buttons_frame,
                    text="📄",
                    width=30,
                    height=30,
                    font=ctk.CTkFont(size=14),
                    fg_color="blue" if has_instructions else "gray",
                    hover_color="darkblue" if has_instructions else "darkgray",
                    command=lambda: self._show_instructions(mod_folder) if has_instructions else None,
                    state="normal" if has_instructions else "disabled"
                )
            instructions_btn.pack(side="left", padx=(0, 2))
        
        # Action button (download/extract icon)
        if is_archive:
            try:
                extract_icon = ctk.CTkImage(
                    light_image=Image.open("assets/static/package-open.png"),
                    dark_image=Image.open("assets/static/package-open.png"),
                    size=(16, 16)
                )
                action_btn = ctk.CTkButton(
                    right_buttons_frame,
                    image=extract_icon,
                    text="",
                    width=30,
                    height=30,
                    fg_color="orange",
                    hover_color="darkorange",
                    command=lambda: self._extract_mod(mod_folder)
                )
            except Exception as e:
                # Fallback to text if icon fails to load
                action_btn = ctk.CTkButton(
                    right_buttons_frame,
                    text="📦",
                    width=30,
                    height=30,
                    font=ctk.CTkFont(size=14),
                    fg_color="orange",
                    hover_color="darkorange",
                    command=lambda: self._extract_mod(mod_folder)
                )
        else:
            try:
                install_icon = ctk.CTkImage(
                    light_image=Image.open("assets/static/arrow-down-from-line.png"),
                    dark_image=Image.open("assets/static/arrow-down-from-line.png"),
                    size=(16, 16)
                )
                action_btn = ctk.CTkButton(
                    right_buttons_frame,
                    image=install_icon,
                    text="",
                    width=30,
                    height=30,
                    fg_color="green" if not is_current else "gray",
                    hover_color="darkgreen" if not is_current else "darkgray",
                    command=lambda: self._install_mod(mod_folder) if not is_current else None,
                    state="normal" if not is_current else "disabled"
                )
            except Exception as e:
                # Fallback to text if icon fails to load
                action_btn = ctk.CTkButton(
                    right_buttons_frame,
                    text="⬇️",
                    width=30,
                    height=30,
                    font=ctk.CTkFont(size=14),
                    fg_color="green" if not is_current else "gray",
                    hover_color="darkgreen" if not is_current else "darkgray",
                    command=lambda: self._install_mod(mod_folder) if not is_current else None,
                    state="normal" if not is_current else "disabled"
                )
        action_btn.pack(side="left", padx=(0, 0))
        
        return card_frame

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

    def _delete_mod(self, mod_folder):
        """Delete a mod folder."""
        if not self.selected_character:
            if self.toast_manager:
                self.toast_manager.show_toast("No character selected.", "error", 3000)
            return
        
        mod_path = os.path.join(self.mods_from, self.selected_character, mod_folder)
        
        try:
            import shutil
            if os.path.isdir(mod_path):
                shutil.rmtree(mod_path)
            else:
                os.remove(mod_path)
            
            if self.toast_manager:
                self.toast_manager.show_toast(f"Deleted {mod_folder}", "success", 3000)
            
            # Refresh the mod list
            self.show_character_mods(
                self.selected_character,
                match_character(self.selected_character, self.character_list)
            )
        except Exception as e:
            if self.toast_manager:
                self.toast_manager.show_toast(f"Failed to delete {mod_folder}: {str(e)}", "error", 5000)

    def _extract_mod(self, mod_folder):
        """Extract an archive mod."""
        if not self.selected_character:
            if self.toast_manager:
                self.toast_manager.show_toast("No character selected.", "error", 3000)
            return

        char_path = os.path.join(self.mods_from, self.selected_character)
        archive_path = os.path.join(char_path, mod_folder)
        
        # Create progress window
        self.progress_window = ExtractionProgressWindow(self, total_files=1)
        
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
            if self.toast_manager:
                self.toast_manager.show_toast(
                    f"Successfully extracted {mod_folder}!",
                    "success",
                    3000
                )
            # Refresh the mod list after a short delay
            self.after(1000, lambda: self.show_character_mods(
                self.selected_character,
                match_character(self.selected_character, self.character_list)
            ))
        else:
            self.progress_window.update_progress(mod_folder, False)
            if self.toast_manager:
                self.toast_manager.show_toast(
                    f"Failed to extract {mod_folder}.",
                    "error",
                    5000
                )

    def _install_mod(self, mod_folder):
        """Install a mod folder."""
        if not self.selected_character:
            if self.toast_manager:
                self.toast_manager.show_toast("No character selected.", "error", 3000)
            return

        source_path = os.path.join(self.mods_from, self.selected_character, mod_folder)
        dest_path = os.path.join(self.mods_to, mod_folder)

        if copy_mod_folder(source_path, dest_path, self.game):
            if self.toast_manager:
                self.toast_manager.show_toast(
                    f"Successfully installed '{mod_folder}'!\nThe mod has been copied to your game directory.",
                    "success",
                    4000
                )
            # Refresh the mod list to update the green border
            self.show_character_mods(
                self.selected_character,
                match_character(self.selected_character, self.character_list)
            )
        else:
            if self.toast_manager:
                self.toast_manager.show_toast(
                    f"Failed to install '{mod_folder}'.",
                    "error",
                    5000
                )