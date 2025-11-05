"""
Reusable Button Components
Google Calendar styled buttons
"""
import customtkinter as ctk
from app.config import COLORS, FONTS, SPACING, LAYOUT


class PrimaryButton(ctk.CTkButton):
    """Primary action button (blue, prominent)"""
    
    def __init__(self, parent, text="Button", command=None, **kwargs):
        super().__init__(
            parent,
            text=text,
            command=command,
            fg_color=COLORS['primary_blue'],
            hover_color=COLORS['primary_blue_hover'],
            text_color=COLORS['text_light'],
            font=FONTS['button'],
            corner_radius=LAYOUT['button_corner_radius'],
            height=LAYOUT['button_height'],
            **kwargs
        )


class SecondaryButton(ctk.CTkButton):
    """Secondary action button (outlined)"""
    
    def __init__(self, parent, text="Button", command=None, **kwargs):
        super().__init__(
            parent,
            text=text,
            command=command,
            fg_color="transparent",
            text_color=COLORS['text_primary'],
            border_width=1,
            border_color=COLORS['border_light'],
            hover_color=COLORS['bg_gray_hover'],
            font=FONTS['body_bold'],
            corner_radius=4,
            height=36,
            **kwargs
        )


class IconButton(ctk.CTkButton):
    """Icon-only button (circular)"""
    
    def __init__(self, parent, text="●", command=None, size=40, **kwargs):
        super().__init__(
            parent,
            text=text,
            command=command,
            width=size,
            height=size,
            fg_color="transparent",
            text_color=COLORS['text_primary'],
            hover_color=COLORS['bg_gray_hover'],
            font=FONTS['heading'],
            corner_radius=size//2,
            **kwargs
        )


class CreateButton(ctk.CTkButton):
    """Special 'Create' button with + icon"""
    
    def __init__(self, parent, command=None, **kwargs):
        super().__init__(
            parent,
            text="+ Tạo mới",
            command=command,
            width=kwargs.pop('width', LAYOUT['sidebar_width'] - (SPACING['md'] * 2)),
            height=LAYOUT['button_height'],
            fg_color=COLORS['primary_blue'],
            hover_color=COLORS['primary_blue_hover'],
            text_color=COLORS['text_light'],
            font=FONTS['button'],
            corner_radius=LAYOUT['button_corner_radius'],
            **kwargs
        )


class TodayButton(ctk.CTkButton):
    """'Today' navigation button"""
    
    def __init__(self, parent, command=None, **kwargs):
        super().__init__(
            parent,
            text="Hôm nay",
            command=command,
            width=90,
            height=36,
            fg_color="transparent",
            text_color=COLORS['text_primary'],
            border_width=1,
            border_color=COLORS['border_light'],
            hover_color=COLORS['bg_gray_hover'],
            font=FONTS['body_bold'],
            corner_radius=4,
            **kwargs
        )


class NavButton(ctk.CTkButton):
    """Navigation arrow button"""
    
    def __init__(self, parent, direction="left", command=None, **kwargs):
        arrow = "◀" if direction == "left" else "▶"
        super().__init__(
            parent,
            text=arrow,
            command=command,
            width=36,
            height=36,
            fg_color="transparent",
            text_color=COLORS['text_primary'],
            hover_color=COLORS['bg_gray_hover'],
            font=FONTS['heading'],
            corner_radius=18,
            **kwargs
        )
