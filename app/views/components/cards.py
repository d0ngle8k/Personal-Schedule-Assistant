"""
Reusable Card Components
Google Calendar styled cards and containers
"""
import customtkinter as ctk
from app.config import COLORS, FONTS, SPACING, LAYOUT


class Card(ctk.CTkFrame):
    """Basic card container"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            fg_color=COLORS['bg_white'],
            corner_radius=LAYOUT['card_corner_radius'],
            border_width=1,
            border_color=COLORS['border_light'],
            **kwargs
        )


class EventCard(ctk.CTkFrame):
    """Event display card with colored border"""
    
    def __init__(self, parent, event_data=None, **kwargs):
        super().__init__(
            parent,
            fg_color=COLORS['bg_white'],
            corner_radius=4,
            border_width=0,
            **kwargs
        )
        
        if event_data:
            self._render_event(event_data)
    
    def _render_event(self, event):
        """Render event content"""
        # Left colored border
        color_bar = ctk.CTkFrame(
            self,
            width=4,
            fg_color=event.get('color', COLORS['event_work']),
            corner_radius=0
        )
        color_bar.pack(side="left", fill="y")
        
        # Content area
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(side="left", fill="both", expand=True, padx=SPACING['sm'], pady=SPACING['xs'])
        
        # Event title
        title = ctk.CTkLabel(
            content,
            text=event.get('title', 'Untitled'),
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary'],
            anchor="w"
        )
        title.pack(fill="x")
        
        # Event time
        time_text = f"{event.get('start_time', '')} - {event.get('end_time', '')}"
        time_label = ctk.CTkLabel(
            content,
            text=time_text,
            font=FONTS['caption'],
            text_color=COLORS['text_secondary'],
            anchor="w"
        )
        time_label.pack(fill="x")
        
        # Location (if available)
        if event.get('location'):
            location = ctk.CTkLabel(
                content,
                text=f"📍 {event['location']}",
                font=FONTS['caption'],
                text_color=COLORS['text_secondary'],
                anchor="w"
            )
            location.pack(fill="x")


class StatCard(ctk.CTkFrame):
    """Statistics card with title and value"""
    
    def __init__(self, parent, title="", value="", icon="📊", **kwargs):
        super().__init__(
            parent,
            fg_color=COLORS['bg_white'],
            corner_radius=LAYOUT['card_corner_radius'],
            border_width=1,
            border_color=COLORS['border_light'],
            **kwargs
        )
        
        # Icon
        icon_label = ctk.CTkLabel(
            self,
            text=icon,
            font=("Segoe UI", 32),
            text_color=COLORS['primary_blue']
        )
        icon_label.pack(pady=(SPACING['md'], SPACING['xs']))
        
        # Value (big number)
        value_label = ctk.CTkLabel(
            self,
            text=str(value),
            font=("Segoe UI", 36, "bold"),
            text_color=COLORS['text_primary']
        )
        value_label.pack()
        
        # Title
        title_label = ctk.CTkLabel(
            self,
            text=title,
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        title_label.pack(pady=(SPACING['xs'], SPACING['md']))


class MiniCalendarCard(ctk.CTkFrame):
    """Mini calendar card for sidebar"""
    
    def __init__(self, parent, current_date=None, **kwargs):
        super().__init__(
            parent,
            fg_color=COLORS['bg_white'],
            corner_radius=LAYOUT['card_corner_radius'],
            border_width=1,
            border_color=COLORS['border_light'],
            **kwargs
        )
        
        from datetime import date
        self.current_date = current_date or date.today()
        
        # Header with month/year
        header = ctk.CTkLabel(
            self,
            text=f"📅 {self.current_date.strftime('%B %Y')}",
            font=FONTS['subheading'],
            text_color=COLORS['text_primary']
        )
        header.pack(pady=SPACING['sm'])
        
        # Placeholder for calendar grid
        placeholder = ctk.CTkLabel(
            self,
            text="Mini calendar grid\n(Phase 2 implementation)",
            font=FONTS['caption'],
            text_color=COLORS['text_secondary']
        )
        placeholder.pack(pady=SPACING['md'])


class SectionHeader(ctk.CTkFrame):
    """Section header with title and optional action button"""
    
    def __init__(self, parent, title="", action_text="", action_command=None, **kwargs):
        super().__init__(
            parent,
            fg_color="transparent",
            **kwargs
        )
        
        # Title
        title_label = ctk.CTkLabel(
            self,
            text=title,
            font=FONTS['subheading'],
            text_color=COLORS['text_primary'],
            anchor="w"
        )
        title_label.pack(side="left", fill="x", expand=True)
        
        # Action button (optional)
        if action_text and action_command:
            action_btn = ctk.CTkButton(
                self,
                text=action_text,
                fg_color="transparent",
                text_color=COLORS['primary_blue'],
                hover_color=COLORS['bg_gray_hover'],
                font=FONTS['body'],
                width=80,
                height=28,
                corner_radius=4,
                command=action_command
            )
            action_btn.pack(side="right")
