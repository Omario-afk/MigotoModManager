"""
Mod card widget for displaying individual mods.
"""
import os
import customtkinter as ctk
from PIL import Image

class ModCard:
    """Helper class for creating mod cards."""
    
    @staticmethod
    def create_mod_card(parent_frame, mod_folder, is_current, is_archive, 
                       has_instructions, callbacks):
        """Create a mod card widget."""
        # Main card frame
        card_frame = ctk.CTkFrame(
            parent_frame,
            width=200,
            height=280,
            corner_radius=10
        )
        
        # Add green background if currently installed
        if is_current:
            card_frame.configure(fg_color=("lightgreen", "darkgreen"))
        
        # Image frame
        image_frame = ctk.CTkFrame(card_frame, height=150, corner_radius=8)
        image_frame.pack(fill="x", padx=10, pady=(10, 5))
        image_frame.pack_propagate(False)
        
        # Image (placeholder for now)
        if is_archive:
            image_path = "assets/static/file-archive.svg"
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
        
        # Mod name
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
        
        # Action buttons frame
        buttons_frame = ctk.CTkFrame(card_frame, height=40)
        buttons_frame.pack(fill="x", padx=10, pady=(0, 10), side="bottom")
        buttons_frame.pack_propagate(False)
        
        # Delete button
        ModCard._create_delete_button(buttons_frame, mod_folder, callbacks['delete'])
        
        # Right side buttons frame
        right_buttons_frame = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        right_buttons_frame.pack(side="right", padx=(0, 5))
        
        # Instructions button (only for folders)
        if not is_archive:
            ModCard._create_instructions_button(right_buttons_frame, mod_folder, 
                                              has_instructions, callbacks['instructions'])
        
        # Action button
        ModCard._create_action_button(right_buttons_frame, mod_folder, is_archive, 
                                    is_current, callbacks)
        
        return card_frame
    
    @staticmethod
    def _create_delete_button(buttons_frame, mod_folder, delete_callback):
        """Create the delete button."""
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
                command=lambda: delete_callback(mod_folder)
            )
        except Exception as e:
            delete_btn = ctk.CTkButton(
                buttons_frame,
                text="🗑️",
                width=30,
                height=30,
                font=ctk.CTkFont(size=14),
                fg_color="red",
                hover_color="darkred",
                command=lambda: delete_callback(mod_folder)
            )
        delete_btn.pack(side="left", padx=(5, 0))
    
    @staticmethod
    def _create_instructions_button(right_buttons_frame, mod_folder, has_instructions, instructions_callback):
        """Create the instructions button."""
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
                command=lambda: instructions_callback(mod_folder) if has_instructions else None,
                state="normal" if has_instructions else "disabled"
            )
        except Exception as e:
            instructions_btn = ctk.CTkButton(
                right_buttons_frame,
                text="📄",
                width=30,
                height=30,
                font=ctk.CTkFont(size=14),
                fg_color="blue" if has_instructions else "gray",
                hover_color="darkblue" if has_instructions else "darkgray",
                command=lambda: instructions_callback(mod_folder) if has_instructions else None,
                state="normal" if has_instructions else "disabled"
            )
        instructions_btn.pack(side="left", padx=(0, 2))
    
    @staticmethod
    def _create_action_button(right_buttons_frame, mod_folder, is_archive, is_current, callbacks):
        """Create the action button (install/extract)."""
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
                    command=lambda: callbacks['extract'](mod_folder)
                )
            except Exception as e:
                action_btn = ctk.CTkButton(
                    right_buttons_frame,
                    text="📦",
                    width=30,
                    height=30,
                    font=ctk.CTkFont(size=14),
                    fg_color="orange",
                    hover_color="darkorange",
                    command=lambda: callbacks['extract'](mod_folder)
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
                    command=lambda: callbacks['install'](mod_folder) if not is_current else None,
                    state="normal" if not is_current else "disabled"
                )
            except Exception as e:
                action_btn = ctk.CTkButton(
                    right_buttons_frame,
                    text="⬇️",
                    width=30,
                    height=30,
                    font=ctk.CTkFont(size=14),
                    fg_color="green" if not is_current else "gray",
                    hover_color="darkgreen" if not is_current else "darkgray",
                    command=lambda: callbacks['install'](mod_folder) if not is_current else None,
                    state="normal" if not is_current else "disabled"
                )
        action_btn.pack(side="left", padx=(0, 0)) 