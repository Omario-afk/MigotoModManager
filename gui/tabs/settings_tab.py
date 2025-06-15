"""
Settings tab for configuring game mod directories.
"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
# ====== THREADING IMPORTS - NEW ======
import threading
import queue
# ====================================
from config.constants import GAME_TABS
from config.settings import save_data
from utils.icons.get_icons import get_icons
import os
import sys

class SettingsTab(ctk.CTkFrame):
    """Settings tab for configuring mod directories."""
    
    def __init__(self, master, game_paths, on_save):
        super().__init__(master)
        self.game_paths = game_paths
        self.on_save = on_save
        self.entries = {}
        # ====== BUTTON TRACKING - NEW ======
        self.get_buttons = {}  # Track get buttons for status updates
        self.download_queue = queue.Queue()  # Queue for thread communication
        # ==================================

        self._create_widgets()
        self._load_saved_values()
        # ====== START QUEUE MONITORING - NEW ======
        self._check_download_queue()
        # =========================================

    def _create_path_widget(self, game):
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
    
    def _create_get_icons_widget(self, game):
        frame = ctk.CTkFrame(self)
        frame.pack(fill="x", padx=2, pady=1)  # Minimal padding

        ctk.CTkLabel(
            frame, 
            text=game, 
            anchor="w", 
            font=ctk.CTkFont(weight="bold")
        ).grid(row=0, column=0, padx=5, sticky="w")

        get_btn = ctk.CTkButton(
            frame, 
            text="Get", 
            width=50,
            command=lambda e=game: self._get_icons(e)
        )
        get_btn.grid(row=0, column=1, padx=(2, 5), sticky="w")

        # ====== STORE BUTTON REFERENCE - NEW ======
        self.get_buttons[game] = get_btn
        # =========================================

        frame.grid_columnconfigure(0, weight=1)

    # ====== THREADING AND STATUS METHODS - NEW ======
    def _get_icons(self, game):
        """Start icon download in separate thread."""
        # Update button to show downloading status
        button = self.get_buttons[game]
        button.configure(
        text="Downloading...",
        fg_color="#FF6600",
        state="disabled"
        )
        
        # Start download in separate thread
        thread = threading.Thread(target=self._download_icons_thread, args=(game,), daemon=True)
        thread.start()
    
    def _download_icons_thread(self, game):
        """Download icons in separate thread."""
        try:
            get_icons(game=game, crop=True)
            # Signal completion via queue
            self.download_queue.put(("success", game))
        except Exception as e:
            # Signal error via queue
            self.download_queue.put(("error", game, str(e)))
    
    def _check_download_queue(self):
        """Check for download completion messages from threads."""
        try:
            while True:
                message = self.download_queue.get_nowait()
                if message[0] == "success":
                    game = message[1]
                    button = self.get_buttons[game]
                    button.configure(text="Done", fg_color="#28A745", hover_color="#218838")
                    button.configure(state="normal")
                    # Reset button after 3 seconds
                    self.after(3000, lambda g=game: self._reset_button(g))
                elif message[0] == "error":
                    game = message[1]
                    error = message[2]
                    button = self.get_buttons[game]
                    button.configure(text="Error", fg_color="#DC3545", hover_color="#C82333")
                    button.configure(state="normal")
                    messagebox.showerror("Download Error", f"Failed to download icons for {game}:\n{error}")
                    # Reset button after 3 seconds
                    self.after(3000, lambda g=game: self._reset_button(g))
        except queue.Empty:
            pass
        
        # Schedule next check
        self.after(100, self._check_download_queue)
    
    def _reset_button(self, game):
        """Reset button to original state."""
        button = self.get_buttons[game]
        button.configure(text="Get", fg_color=["#3B8ED0", "#1F6AA5"], hover_color=["#36719F", "#144870"])
    # =============================================
        
    def _create_widgets(self):
        """Create and layout widgets."""
        ctk.CTkLabel(
            self, 
            text="Set 'Mods From' and 'Mods To' folders for each game:", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)

        for game in GAME_TABS:
            self._create_path_widget(game)
        
        ctk.CTkLabel(
            self, 
            text="Update Characters", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        for game in GAME_TABS:
            self._create_get_icons_widget(game)
        
        save_btn = ctk.CTkButton(self, text="Save Settings", command=self.save_settings)
        save_btn.pack(pady=15)
        
        restart_button = ctk.CTkButton(self, text="Reload App", command=self._restart_app, fg_color="#c36424")
        restart_button.pack(pady=10)

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

    def _restart_app(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)
        
    def save_settings(self):
        """Save current settings."""
        for game, (from_entry, to_entry) in self.entries.items():
            self.game_paths[game] = {
                "from": from_entry.get().strip().replace('\\', '/'),
                "to": to_entry.get().strip().replace('\\', '/')
            }
        save_data(self.game_paths)
        self.on_save()
        messagebox.showinfo("Saved", "Settings saved successfully.")