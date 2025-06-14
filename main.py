"""
Main entry point for the Mod Manager application.
"""
import customtkinter as ctk
from gui.app import App

def main():
    """Initialize and run the application."""
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()