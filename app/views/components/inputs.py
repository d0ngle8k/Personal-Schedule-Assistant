"""
Reusable Input Components
Google Calendar styled input fields
"""
import customtkinter as ctk
from app.config import COLORS, FONTS, SPACING, LAYOUT


class StyledEntry(ctk.CTkEntry):
    """Standard text input field"""
    
    def __init__(self, parent, placeholder="", **kwargs):
        super().__init__(
            parent,
            placeholder_text=placeholder,
            height=LAYOUT['input_height'],
            corner_radius=4,
            border_width=1,
            border_color=COLORS['border_light'],
            fg_color=COLORS['bg_white'],
            text_color=COLORS['text_primary'],
            placeholder_text_color=COLORS['text_secondary'],
            font=FONTS['body'],
            **kwargs
        )
        
        # Bind focus events for border color
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)
    
    def _on_focus_in(self, event):
        """Change border color on focus"""
        self.configure(border_color=COLORS['border_focus'])
    
    def _on_focus_out(self, event):
        """Reset border color on blur"""
        self.configure(border_color=COLORS['border_light'])


class SearchEntry(ctk.CTkEntry):
    """Search input with icon"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            placeholder_text="🔍 Tìm kiếm...",
            height=40,
            corner_radius=20,
            border_width=1,
            border_color=COLORS['border_light'],
            fg_color=COLORS['bg_gray'],
            text_color=COLORS['text_primary'],
            placeholder_text_color=COLORS['text_secondary'],
            font=FONTS['body'],
            **kwargs
        )


class TextArea(ctk.CTkTextbox):
    """Multi-line text input"""
    
    def __init__(self, parent, placeholder="", **kwargs):
        super().__init__(
            parent,
            corner_radius=4,
            border_width=1,
            border_color=COLORS['border_light'],
            fg_color=COLORS['bg_white'],
            text_color=COLORS['text_primary'],
            font=FONTS['body'],
            **kwargs
        )
        
        if placeholder:
            self.insert("1.0", placeholder)
            self.configure(text_color=COLORS['text_secondary'])
            self.bind("<FocusIn>", lambda e: self._clear_placeholder(placeholder))
    
    def _clear_placeholder(self, placeholder):
        """Clear placeholder on focus"""
        if self.get("1.0", "end-1c") == placeholder:
            self.delete("1.0", "end")
            self.configure(text_color=COLORS['text_primary'])


class Dropdown(ctk.CTkComboBox):
    """Styled dropdown/select"""
    
    def __init__(self, parent, values=[], **kwargs):
        super().__init__(
            parent,
            values=values,
            height=LAYOUT['input_height'],
            corner_radius=4,
            border_width=1,
            border_color=COLORS['border_light'],
            fg_color=COLORS['bg_white'],
            button_color=COLORS['primary_blue'],
            button_hover_color=COLORS['primary_blue_hover'],
            text_color=COLORS['text_primary'],
            font=FONTS['body'],
            **kwargs
        )


class Checkbox(ctk.CTkCheckBox):
    """Styled checkbox"""
    
    def __init__(self, parent, text="", color=None, **kwargs):
        fg_color = color if color else COLORS['primary_blue']
        super().__init__(
            parent,
            text=text,
            fg_color=fg_color,
            hover_color=fg_color,
            font=FONTS['body'],
            text_color=COLORS['text_primary'],
            checkbox_width=18,
            checkbox_height=18,
            corner_radius=3,
            **kwargs
        )


class Switch(ctk.CTkSwitch):
    """Toggle switch"""
    
    def __init__(self, parent, text="", **kwargs):
        super().__init__(
            parent,
            text=text,
            fg_color=COLORS['primary_blue'],
            progress_color=COLORS['primary_blue_hover'],
            button_color=COLORS['bg_white'],
            button_hover_color=COLORS['bg_gray'],
            font=FONTS['body'],
            text_color=COLORS['text_primary'],
            **kwargs
        )
