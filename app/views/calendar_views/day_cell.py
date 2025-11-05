"""
Day Cell Component
Individual day cell for month calendar grid
"""
import customtkinter as ctk
from datetime import date
from typing import List, Optional
from app.config import COLORS, FONTS, SPACING


class DayCell(ctk.CTkFrame):
    """
    A single day cell in the month calendar grid
    Shows day number, event dots, and handles clicks
    """
    
    def __init__(self, parent, controller, **kwargs):
        """
        Initialize day cell
        
        Args:
            parent: Parent widget
            controller: MainController instance
        """
        super().__init__(
            parent,
            fg_color=COLORS['bg_white'],
            corner_radius=8,
            border_width=1,
            border_color=COLORS['border_light'],
            cursor="hand2",  # Show pointer cursor
            **kwargs
        )
        
        self.controller = controller
        self.date_obj: Optional[date] = None
        self.events: List = []
        self.is_selected = False
        self.is_today = False
        self.is_current_month = True
        
        self._setup_ui()
        self._bind_events()
    
    def _setup_ui(self):
        """Setup cell UI elements - OPTIMIZED: Create widgets ONCE, reuse forever"""
        # Container for content (to handle padding)
        self.content_frame = ctk.CTkFrame(
            self,
            fg_color='transparent'
        )
        self.content_frame.pack(fill='both', expand=True, padx=SPACING['xs'], pady=SPACING['xs'])
        
        # Day number at top
        self.day_label = ctk.CTkLabel(
            self.content_frame,
            text="",
            font=FONTS['body'],
            text_color=COLORS['text_primary'],
            anchor='nw'  # Align to top-left
        )
        self.day_label.pack(anchor='nw', pady=(0, SPACING['xs']))
        
        # Event dots container
        self.events_container = ctk.CTkFrame(
            self.content_frame,
            fg_color='transparent',
            height=24
        )
        self.events_container.pack(fill='x', side='bottom')
        self.events_container.pack_propagate(False)
        
        # OPTIMIZATION: Pre-create 3 dot labels + "more" label for reuse
        self.dots_frame = ctk.CTkFrame(
            self.events_container,
            fg_color='transparent'
        )
        self.dots_frame.pack(anchor='center')
        
        self._event_dots = []
        for i in range(3):
            dot = ctk.CTkLabel(
                self.dots_frame,
                text="●",
                font=("Arial", 12),
                width=8,
                height=8
            )
            dot.pack(side='left', padx=1)
            dot.pack_forget()  # Hide initially
            self._event_dots.append(dot)
        
        self._more_label = ctk.CTkLabel(
            self.dots_frame,
            text="",
            font=("Arial", 8),
            width=20
        )
        self._more_label.pack(side='left', padx=2)
        self._more_label.pack_forget()  # Hide initially
    
    def _bind_events(self):
        """Bind mouse events"""
        # Bind click to self and all children
        widgets = [self, self.content_frame, self.day_label, self.events_container]
        for widget in widgets:
            widget.bind("<Button-1>", self._on_click)
            widget.bind("<Double-Button-1>", self._on_double_click)  # Double-click to create event
            widget.bind("<Enter>", self._on_hover_enter)
            widget.bind("<Leave>", self._on_hover_leave)
    
    def set_date(self, 
                 date_obj: Optional[date], 
                 is_today: bool = False,
                 is_current_month: bool = True,
                 events: List = None,
                 is_selected: bool = False):
        """
        Update cell with date and events
        
        Args:
            date_obj: Date object for this cell (None for empty cell)
            is_today: Whether this is today's date
            is_current_month: Whether this date is in current month
            events: List of Event objects for this date
            is_selected: Whether this date is currently selected
        """
        self.date_obj = date_obj
        self.is_today = is_today
        self.is_current_month = is_current_month
        self.is_selected = is_selected
        self.events = events or []
        
        if date_obj is None:
            # Empty cell (days from other months not shown)
            self.day_label.configure(text="")
            self.configure(fg_color='transparent', border_width=0)
            return
        
        # Update day number
        self.day_label.configure(text=str(date_obj.day))
        
        # Apply styling
        self._update_styling()
        
        # Update event dots
        self._update_event_dots()
    
    def _update_styling(self):
        """Apply visual styling based on cell state"""
        # Base colors
        bg_color = COLORS['bg_white']
        text_color = COLORS['text_primary']
        border_color = COLORS['border_light']
        border_width = 1
        
        # Other month styling (grayed out)
        if not self.is_current_month:
            text_color = COLORS['text_secondary']
            self.day_label.configure(font=FONTS['caption'])
        else:
            self.day_label.configure(font=FONTS['body'])
        
        # Today styling (blue background and border)
        if self.is_today:
            bg_color = COLORS.get('primary_blue_light', '#E8F0FE')
            border_color = COLORS['primary_blue']
            border_width = 2
            text_color = COLORS['primary_blue']
            self.day_label.configure(font=FONTS['button'])  # Bold for today
        
        # Selected styling (gray background)
        if self.is_selected and not self.is_today:
            bg_color = COLORS.get('bg_gray', '#F1F3F4')
            border_color = COLORS['primary_blue']
            border_width = 2
        
        # Weekend styling (lighter background)
        if self.date_obj and self.date_obj.weekday() >= 5:  # Saturday=5, Sunday=6
            if not self.is_today and not self.is_selected:
                bg_color = COLORS.get('bg_gray', '#FAFAFA')
        
        # Apply colors
        self.configure(
            fg_color=bg_color,
            border_color=border_color,
            border_width=border_width
        )
        self.day_label.configure(text_color=text_color)
    
    def _update_event_dots(self):
        """
        OPTIMIZED: Display event dots WITHOUT destroying/creating widgets
        Reuse pre-created labels, only update text and visibility
        """
        if not self.events:
            # Hide all dots
            for dot in self._event_dots:
                dot.pack_forget()
            self._more_label.pack_forget()
            return
        
        # Show up to 3 events as dots (reuse existing labels)
        visible_events = self.events[:3]
        
        for i, dot in enumerate(self._event_dots):
            if i < len(visible_events):
                # Update and show dot
                event = visible_events[i]
                dot.configure(text_color=event.category_color)
                dot.pack(side='left', padx=1)
            else:
                # Hide unused dot
                dot.pack_forget()
        
        # Show "+N more" if there are more events
        more_count = len(self.events) - 3
        if more_count > 0:
            self._more_label.configure(
                text=f"+{more_count}",
                text_color=COLORS['text_secondary']
            )
            self._more_label.pack(side='left', padx=2)
        else:
            self._more_label.pack_forget()
    
    def _on_click(self, event):
        """Handle cell click - navigate to that date"""
        if self.date_obj and hasattr(self.controller, 'handle_date_selected'):
            self.controller.handle_date_selected(self.date_obj)
    
    def _on_double_click(self, event):
        """Handle cell double-click - create event for that date"""
        if self.date_obj and hasattr(self.controller, 'handle_day_cell_double_click'):
            self.controller.handle_day_cell_double_click(self.date_obj)
    
    def _on_hover_enter(self, event):
        """Handle mouse enter (hover)"""
        if self.date_obj and not self.is_today:
            # Lighten the background on hover
            current_fg = self.cget('fg_color')
            if current_fg == COLORS['bg_white']:
                self.configure(fg_color=COLORS.get('bg_gray_hover', '#F8F9FA'))
    
    def _on_hover_leave(self, event):
        """Handle mouse leave"""
        if self.date_obj:
            # Restore original styling
            self._update_styling()
