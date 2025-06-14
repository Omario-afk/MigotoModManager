"""
Custom widget implementations for the Mod Manager.
"""
import customtkinter as ctk
import os
from PIL import Image

class ModButton(ctk.CTkButton):
    """Custom button for mod selection."""
    
    def __init__(self, master, mod_name, on_click, **kwargs):
        super().__init__(master, text=mod_name, command=lambda: on_click(mod_name), **kwargs)
        self.mod_name = mod_name

class CharacterButton(ctk.CTkButton):
    """Custom button for character selection."""
    
    def __init__(self, master, character_name, folder_name, on_click, **kwargs):
        super().__init__(master, text=character_name, command=lambda: on_click(folder_name, character_name), **kwargs)
        self.character_name = character_name
        self.folder_name = folder_name
        
class ImageButton(ctk.CTkFrame):
    """Custom button with image and text label."""
    
    def __init__(self, master, image_path, text, command, width=120, height=140, **kwargs):
        super().__init__(master, width=width, height=height, **kwargs)
        
        self.command = command
        self.text = text
        self.image_path = image_path
        self.is_hovered = False
        
        # Store the original fg_color 
        self.original_fg_color = self.cget("fg_color")
        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)
        
        # Load and display image
        self.image_label = ctk.CTkLabel(self, text="")
        self.image_label.grid(row=0, column=0, sticky="nsew", padx=5, pady=(5, 2))
        
        # Text label
        self.text_label = ctk.CTkLabel(
            self, 
            text=text, 
            font=ctk.CTkFont(size=11, weight="bold"),
            wraplength=width-10
        )
        self.text_label.grid(row=1, column=0, sticky="ew", padx=5, pady=(0, 5))
        
        # Load image
        self.load_image()
        
        # Bind click events
        self.bind("<Button-1>", self._on_click)
        self.image_label.bind("<Button-1>", self._on_click)
        self.text_label.bind("<Button-1>", self._on_click)
        
        # Hover effects
        self.bind("<Enter>", self._on_hover)
        self.bind("<Leave>", self._on_leave)
        self.image_label.bind("<Enter>", self._on_hover)
        self.image_label.bind("<Leave>", self._on_leave)
        self.text_label.bind("<Enter>", self._on_hover)
        self.text_label.bind("<Leave>", self._on_leave)
        
    def load_image(self):
        """Load and display the character image."""
        try:
            if os.path.exists(self.image_path):
                # Load image with PIL
                pil_image = Image.open(self.image_path)
                
                # Resize image to fit button (maintaining aspect ratio)
                img_width, img_height = pil_image.size
                max_size = 80  # Maximum size for the image
                
                if img_width > img_height:
                    new_width = max_size
                    new_height = int((max_size * img_height) / img_width)
                else:
                    new_height = max_size
                    new_width = int((max_size * img_width) / img_height)
                
                pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Create CTkImage instead of PhotoImage
                self.ctk_image = ctk.CTkImage(
                    light_image=pil_image,
                    dark_image=pil_image,
                    size=(new_width, new_height)
                )
                self.image_label.configure(image=self.ctk_image)
            else:
                # Show placeholder if image not found
                self.image_label.configure(text="No Image", font=ctk.CTkFont(size=10))
                
        except Exception as e:
            print(f"Error loading image {self.image_path}: {e}")
            self.image_label.configure(text="Error", font=ctk.CTkFont(size=10))
    
    def _on_click(self, event=None):
        """Handle click event."""
        if self.command:
            self.command()
    
    def _on_hover(self, event=None):
        """Handle hover enter."""
        if not self.is_hovered:
            self.is_hovered = True
            self.configure(fg_color=("gray75", "gray25"))
    
    def _on_leave(self, event=None):
        """Handle hover leave."""
        if self.is_hovered:
            self.is_hovered = False
            # Reset to transparent/default - let the parent handle the color
            self.configure(fg_color=self.original_fg_color)

class CharacterImageButton(ImageButton):
    """Specialized image button for characters."""
    
    def __init__(self, master, character_name, folder_name, game_name, on_click, **kwargs):
        # Construct image path - check for .webp first, then other formats
        base_path = os.path.join("assets", "character_icons", game_name, "icons", folder_name)
        image_path = None
        
        # Check for various image formats including .webp
        for ext in ['.webp', '.png', '.jpg', '.jpeg', '.gif', '.bmp']:
            test_path = f"{base_path}{ext}"
            if os.path.exists(test_path):
                image_path = test_path
                break
        
        # Fallback to original .png path if nothing found
        if image_path is None:
            image_path = f"{base_path}.png"
        
        super().__init__(
            master=master,
            image_path=image_path,
            text=character_name,
            command=lambda: on_click(folder_name, character_name),
            **kwargs
        )
        
        self.character_name = character_name
        self.folder_name = folder_name
        self.game_name = game_name