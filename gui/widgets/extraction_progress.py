"""
Extraction progress window for archive operations.
"""
import customtkinter as ctk
from tkinter import ttk

class ExtractionProgressWindow(ctk.CTkToplevel):
    """Window to show extraction progress."""
    
    def __init__(self, parent, total_files=1):
        super().__init__(parent)
        self.title("Extracting Archives")
        self.geometry("400x200")
        self.resizable(False, False)
        
        # Make window modal
        self.transient(parent)
        self.grab_set()
        
        # Center window
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        # Create widgets
        self.progress_label = ctk.CTkLabel(
            self,
            text="Preparing to extract...",
            font=ctk.CTkFont(size=12)
        )
        self.progress_label.pack(pady=(20, 10))
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(
            self,
            orient="horizontal",
            length=350,
            mode="determinate"
        )
        self.progress_bar.pack(pady=10)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=11),
            wraplength=350
        )
        self.status_label.pack(pady=10)
        
        # Close button (initially disabled)
        self.close_button = ctk.CTkButton(
            self,
            text="Close",
            command=self.destroy,
            state="disabled"
        )
        self.close_button.pack(pady=10)
        
        # Initialize progress
        self.total_files = total_files
        self.current_file = 0
        self.progress_bar["maximum"] = total_files
        
    def update_progress(self, filename, success=True):
        """Update progress with current file status."""
        self.current_file += 1
        self.progress_bar["value"] = self.current_file
        
        status = "✓" if success else "✗"
        self.status_label.configure(
            text=f"{status} {filename}"
        )
        
        if self.current_file >= self.total_files:
            self.progress_label.configure(text="Extraction Complete!")
            self.close_button.configure(state="normal")
            
    def show_error(self, message):
        """Show error message."""
        self.progress_label.configure(text="Extraction Failed!")
        self.status_label.configure(text=message)
        self.close_button.configure(state="normal") 