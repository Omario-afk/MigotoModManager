"""
Instructions window for displaying mod instructions.
"""
import customtkinter as ctk

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