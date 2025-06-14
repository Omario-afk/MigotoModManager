"""
Settings tab for configuring game mod directories.
"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
from config.constants import GAME_TABS
from config.settings import save_data

class SettingsTab(ctk.CTkFrame):
    """Settings tab for configuring mod directories."""
    
    def __init__(self, master, game_paths, on_save):
        super().__init__(master)
        self.game_paths = game_paths
        self.on_save = on_save
        self.entries = {}

        self._create_widgets()
        self._load_saved_values()

    def _create_widgets(self):
        """Create and layout widgets."""
        ctk.CTkLabel(
            self, 
            text="Set 'Mods From' and 'Mods To' folders for each game:", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)

        for game in GAME_TABS:
            frame = ctk.CTkFrame(self)
            frame.pack(fill="x", padx=10, pady=5)

            ctk.CTkLabel(
                frame, 
                text=game, 
                width=18, 
                anchor="w", 
                font=ctk.CTkFont(weight="bold")
            ).grid(row=0, column=0, padx=5, sticky="w")

            from_entry = ctk.CTkEntry(frame, placeholder_text="Mods From")
            from_entry.grid(row=0, column=1, padx=5, sticky="ew")
            from_btn = ctk.CTkButton(
                frame, 
                text="Browse", 
                width=10, 
                command=lambda e=from_entry: self._browse_dir(e)
            )
            from_btn.grid(row=0, column=2, padx=5)

            to_entry = ctk.CTkEntry(frame, placeholder_text="Mods To")
            to_entry.grid(row=0, column=3, padx=5, sticky="ew")
            to_btn = ctk.CTkButton(
                frame, 
                text="Browse", 
                width=10, 
                command=lambda e=to_entry: self._browse_dir(e)
            )
            to_btn.grid(row=0, column=4, padx=5)

            frame.grid_columnconfigure(1, weight=1)
            frame.grid_columnconfigure(3, weight=1)

            self.entries[game] = (from_entry, to_entry)

        save_btn = ctk.CTkButton(self, text="Save Settings", command=self.save_settings)
        save_btn.pack(pady=15)

    def _load_saved_values(self):
        """Load saved values into entry fields."""
        for game, (from_entry, to_entry) in self.entries.items():
            if game in self.game_paths:
                from_entry.insert(0, self.game_paths[game].get("from", ""))
                to_entry.insert(0, self.game_paths[game].get("to", ""))

    def _browse_dir(self, entry):
        """Browse for directory and update entry."""
        dir_ = filedialog.askdirectory(title="Select Directory")
        if dir_:
            entry.delete(0, "end")
            entry.insert(0, dir_)

    def save_settings(self):
        """Save current settings."""
        for game, (from_entry, to_entry) in self.entries.items():
            self.game_paths[game] = {
                "from": from_entry.get().strip(),
                "to": to_entry.get().strip()
            }
        save_data(self.game_paths)
        self.on_save()
        messagebox.showinfo("Saved", "Settings saved successfully.")