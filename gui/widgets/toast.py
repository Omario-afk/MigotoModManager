"""
Toast notification widget for displaying non-intrusive messages.
"""
import customtkinter as ctk
import threading
import time
from typing import Optional, Literal

class ToastNotification(ctk.CTkToplevel):
    """A modern toast notification widget."""
    
    def __init__(
        self, 
        parent, 
        message: str, 
        toast_type: Literal["success", "error", "info", "warning"] = "info",
        duration: int = 3000,
        position: Literal["top-right", "top-left", "bottom-right", "bottom-left", "center"] = "top-right"
    ):
        super().__init__(parent)
        
        self.message = message
        self.toast_type = toast_type
        self.duration = duration
        self.position = position
        
        # Configure window
        self.title("")
        self.geometry("300x80")
        self.resizable(False, False)
        self.overrideredirect(True)  # Remove window decorations
        
        # Make window stay on top
        self.attributes('-topmost', True)
        
        # Set transparency
        self.attributes('-alpha', 0.95)
        
        # Configure appearance based on type
        self._configure_appearance()
        
        # Create widgets
        self._create_widgets()
        
        # Position window
        self._position_window()
        
        # Start auto-dismiss timer
        self._start_dismiss_timer()
        
        # Add fade-in animation
        self._fade_in()
    
    def _configure_appearance(self):
        """Configure colors and styling based on toast type."""
        if self.toast_type == "success":
            self.bg_color = ("#d4edda", "#155724")  # Green
            self.border_color = ("#c3e6cb", "#155724")
            self.text_color = ("#155724", "#d4edda")
            self.icon = "✓"
        elif self.toast_type == "error":
            self.bg_color = ("#f8d7da", "#721c24")  # Red
            self.border_color = ("#f5c6cb", "#721c24")
            self.text_color = ("#721c24", "#f8d7da")
            self.icon = "✗"
        elif self.toast_type == "warning":
            self.bg_color = ("#fff3cd", "#856404")  # Yellow
            self.border_color = ("#ffeaa7", "#856404")
            self.text_color = ("#856404", "#fff3cd")
            self.icon = "⚠"
        else:  # info
            self.bg_color = ("#d1ecf1", "#0c5460")  # Blue
            self.border_color = ("#bee5eb", "#0c5460")
            self.text_color = ("#0c5460", "#d1ecf1")
            self.icon = "ℹ"
    
    def _create_widgets(self):
        """Create the toast content."""
        # Main frame with border
        self.main_frame = ctk.CTkFrame(
            self,
            fg_color=self.bg_color,
            corner_radius=8,
            border_width=2,
            border_color=self.border_color
        )
        self.main_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Content frame
        content_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Icon and message
        icon_label = ctk.CTkLabel(
            content_frame,
            text=self.icon,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.text_color,
            width=30
        )
        icon_label.pack(side="left", padx=(0, 10))
        
        # Message label
        self.message_label = ctk.CTkLabel(
            content_frame,
            text=self.message,
            font=ctk.CTkFont(size=12),
            text_color=self.text_color,
            wraplength=220,
            justify="left"
        )
        self.message_label.pack(side="left", fill="both", expand=True)
        
        # Close button
        close_btn = ctk.CTkButton(
            content_frame,
            text="×",
            width=20,
            height=20,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="transparent",
            hover_color=("rgba(0,0,0,0.1)", "rgba(255,255,255,0.1)"),
            text_color=self.text_color,
            command=self.dismiss,
            corner_radius=10
        )
        close_btn.pack(side="right", padx=(5, 0))
        
        # Bind click events for dismissal
        self.bind("<Button-1>", lambda e: self.dismiss())
        self.main_frame.bind("<Button-1>", lambda e: self.dismiss())
        content_frame.bind("<Button-1>", lambda e: self.dismiss())
    
    def _position_window(self):
        """Position the toast window based on the specified position."""
        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Get window dimensions
        self.update_idletasks()
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        
        # Calculate position
        if self.position == "top-right":
            x = screen_width - window_width - 20
            y = 20
        elif self.position == "top-left":
            x = 20
            y = 20
        elif self.position == "bottom-right":
            x = screen_width - window_width - 20
            y = screen_height - window_height - 20
        elif self.position == "bottom-left":
            x = 20
            y = screen_height - window_height - 20
        else:  # center
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
        
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    def _start_dismiss_timer(self):
        """Start the auto-dismiss timer."""
        def dismiss_after_delay():
            time.sleep(self.duration / 1000)
            self.after(0, self.dismiss)
        
        timer_thread = threading.Thread(target=dismiss_after_delay, daemon=True)
        timer_thread.start()
    
    def _fade_in(self):
        """Animate the fade-in effect."""
        self.attributes('-alpha', 0.0)
        
        def fade_step(alpha=0.0):
            if alpha < 0.95:
                self.attributes('-alpha', alpha)
                self.after(10, lambda: fade_step(alpha + 0.05))
        
        fade_step()
    
    def _fade_out(self):
        """Animate the fade-out effect."""
        def fade_step(alpha=0.95):
            if alpha > 0.0:
                self.attributes('-alpha', alpha)
                self.after(10, lambda: fade_step(alpha - 0.05))
            else:
                self.destroy()
        
        fade_step()
    
    def dismiss(self):
        """Dismiss the toast with fade-out animation."""
        self._fade_out()


class ToastManager:
    """Manager for multiple toast notifications."""
    
    def __init__(self, parent):
        self.parent = parent
        self.active_toasts = []
        self.toast_queue = []
        self.max_toasts = 3
        self.toast_spacing = 10
    
    def show_toast(
        self, 
        message: str, 
        toast_type: Literal["success", "error", "info", "warning"] = "info",
        duration: int = 3000,
        position: Literal["top-right", "top-left", "bottom-right", "bottom-left", "center"] = "top-right"
    ):
        """Show a toast notification."""
        # Create toast
        toast = ToastNotification(
            self.parent,
            message,
            toast_type,
            duration,
            position
        )
        
        # Add to active toasts
        self.active_toasts.append(toast)
        
        # Position toasts to avoid overlap
        self._reposition_toasts()
        
        # Remove from active list when dismissed
        toast.bind("<Destroy>", lambda e: self._remove_toast(toast))
        
        return toast
    
    def _remove_toast(self, toast):
        """Remove toast from active list."""
        if toast in self.active_toasts:
            self.active_toasts.remove(toast)
            self._reposition_toasts()
    
    def _reposition_toasts(self):
        """Reposition all active toasts to avoid overlap."""
        if not self.active_toasts:
            return
        
        # Get screen dimensions
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        
        # Position each toast
        for i, toast in enumerate(self.active_toasts):
            if not toast.winfo_exists():
                continue
                
            # Get toast dimensions
            toast.update_idletasks()
            window_width = toast.winfo_width()
            window_height = toast.winfo_height()
            
            # Calculate position (stacked from top-right)
            x = screen_width - window_width - 20
            y = 20 + (i * (window_height + self.toast_spacing))
            
            # Ensure toast doesn't go off screen
            if y + window_height > screen_height - 20:
                y = screen_height - window_height - 20
            
            toast.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    def dismiss_all(self):
        """Dismiss all active toasts."""
        for toast in self.active_toasts[:]:  # Copy list to avoid modification during iteration
            if toast.winfo_exists():
                toast.dismiss()


# Convenience functions for easy usage
def show_success(parent, message: str, duration: int = 3000):
    """Show a success toast."""
    return ToastNotification(parent, message, "success", duration)

def show_error(parent, message: str, duration: int = 5000):
    """Show an error toast."""
    return ToastNotification(parent, message, "error", duration)

def show_info(parent, message: str, duration: int = 3000):
    """Show an info toast."""
    return ToastNotification(parent, message, "info", duration)

def show_warning(parent, message: str, duration: int = 4000):
    """Show a warning toast."""
    return ToastNotification(parent, message, "warning", duration) 