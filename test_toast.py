"""
Test script to demonstrate the toast notification system.
"""
import customtkinter as ctk
from gui.widgets.toast import ToastManager, show_success, show_error, show_info, show_warning

class ToastTestApp(ctk.CTk):
    """Simple test app for toast notifications."""
    
    def __init__(self):
        super().__init__()
        self.title("Toast Notification Test")
        self.geometry("400x300")
        
        # Initialize toast manager
        self.toast_manager = ToastManager(self)
        
        # Create test buttons
        self._create_widgets()
    
    def _create_widgets(self):
        """Create test buttons."""
        # Title
        title = ctk.CTkLabel(self, text="Toast Notification Test", font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=20)
        
        # Button frame
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Test buttons
        ctk.CTkButton(
            button_frame,
            text="Show Success Toast",
            command=self._show_success,
            fg_color="green",
            hover_color="darkgreen"
        ).pack(pady=10, padx=20, fill="x")
        
        ctk.CTkButton(
            button_frame,
            text="Show Error Toast",
            command=self._show_error,
            fg_color="red",
            hover_color="darkred"
        ).pack(pady=10, padx=20, fill="x")
        
        ctk.CTkButton(
            button_frame,
            text="Show Info Toast",
            command=self._show_info,
            fg_color="blue",
            hover_color="darkblue"
        ).pack(pady=10, padx=20, fill="x")
        
        ctk.CTkButton(
            button_frame,
            text="Show Warning Toast",
            command=self._show_warning,
            fg_color="orange",
            hover_color="darkorange"
        ).pack(pady=10, padx=20, fill="x")
        
        ctk.CTkButton(
            button_frame,
            text="Show Multiple Toasts",
            command=self._show_multiple,
            fg_color="purple",
            hover_color="darkpurple"
        ).pack(pady=10, padx=20, fill="x")
        
        ctk.CTkButton(
            button_frame,
            text="Dismiss All Toasts",
            command=self._dismiss_all,
            fg_color="gray",
            hover_color="darkgray"
        ).pack(pady=10, padx=20, fill="x")
    
    def _show_success(self):
        """Show a success toast."""
        self.toast_manager.show_toast("Operation completed successfully!", "success", 3000)
    
    def _show_error(self):
        """Show an error toast."""
        self.toast_manager.show_toast("An error occurred while processing the request.", "error", 5000)
    
    def _show_info(self):
        """Show an info toast."""
        self.toast_manager.show_toast("This is an informational message for the user.", "info", 3000)
    
    def _show_warning(self):
        """Show a warning toast."""
        self.toast_manager.show_toast("Please be careful with this operation.", "warning", 4000)
    
    def _show_multiple(self):
        """Show multiple toasts to test stacking."""
        self.toast_manager.show_toast("First notification", "info", 2000)
        self.after(500, lambda: self.toast_manager.show_toast("Second notification", "success", 2000))
        self.after(1000, lambda: self.toast_manager.show_toast("Third notification", "warning", 2000))
    
    def _dismiss_all(self):
        """Dismiss all active toasts."""
        self.toast_manager.dismiss_all()

if __name__ == "__main__":
    app = ToastTestApp()
    app.mainloop() 