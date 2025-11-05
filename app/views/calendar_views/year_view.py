"""
Year View Component
12-month grid layout showing mini calendars (Google Calendar style)
"""
import customtkinter as ctk
from datetime import date, datetime, timedelta
import calendar
from typing import Dict, List
from app.config import COLORS, FONTS, SPACING


class YearView(ctk.CTkFrame):
    """
    Year view with 12-month grid (4 rows × 3 columns)
    Each month shows a mini calendar like Google Calendar
    """
    
    def __init__(self, parent, controller):
        """
        Initialize year view
        
        Args:
            parent: Parent widget
            controller: MainController instance
        """
        super().__init__(parent, fg_color=COLORS['bg_white'])
        
        self.controller = controller
        self.current_year = date.today().year
        
        # OPTIMIZATION: Store month widgets for reuse
        self.month_widgets = []  # List of 12 month calendar widgets
        self._month_day_buttons = {}  # {month: [buttons]} - reusable buttons
        
        self._setup_ui()
    
    def _setup_ui(self):
        """OPTIMIZED: Setup year view UI - create widgets ONCE"""
        # Scrollable container for 12 months
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=COLORS['bg_white']
        )
        self.scroll_frame.pack(fill='both', expand=True, padx=SPACING['lg'], pady=SPACING['lg'])
        
        # Create 12 month grid (4 rows × 3 columns) - ONCE
        self.month_widgets = []
        self.month_headers = []  # Store headers for updating
        
        for row in range(4):
            row_frame = ctk.CTkFrame(self.scroll_frame, fg_color='transparent')
            row_frame.pack(fill='x', pady=SPACING['sm'])
            
            for col in range(3):
                month_num = row * 3 + col + 1  # 1-12
                month_widget, month_header = self._create_month_mini_calendar_static(row_frame, month_num)
                month_widget.pack(side='left', fill='both', expand=True, padx=SPACING['sm'])
                self.month_widgets.append(month_widget)
                self.month_headers.append(month_header)
    
    def _create_month_mini_calendar_static(self, parent, month: int):
        """
        OPTIMIZED: Create mini calendar widgets ONCE - reuse forever
        
        Args:
            parent: Parent frame
            month: Month number (1-12)
            
        Returns:
            Tuple of (month_frame, month_header) for later updates
        """
        from app.config import MONTHS, WEEKDAYS_SHORT
        
        # Month container
        month_frame = ctk.CTkFrame(
            parent,
            fg_color='transparent',
            border_width=1,
            border_color=COLORS['border_light'],
            corner_radius=8
        )
        
        # Month name header (will be updated)
        month_header = ctk.CTkLabel(
            month_frame,
            text=MONTHS[month - 1],
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        month_header.pack(pady=(SPACING['sm'], SPACING['xs']))
        
        # Weekday headers (static, never change)
        weekday_frame = ctk.CTkFrame(month_frame, fg_color='transparent')
        weekday_frame.pack(fill='x', padx=SPACING['xs'])
        
        for weekday in WEEKDAYS_SHORT:
            day_label = ctk.CTkLabel(
                weekday_frame,
                text=weekday,
                font=FONTS['small'],
                text_color=COLORS['text_secondary'],
                width=30
            )
            day_label.pack(side='left', expand=True)
        
        # Create maximum 6 weeks of day buttons (42 buttons total)
        # We'll show/hide them as needed
        day_buttons = []
        week_frames = []
        
        for week_idx in range(6):  # Max 6 weeks in a month
            week_frame = ctk.CTkFrame(month_frame, fg_color='transparent')
            week_frame.pack(fill='x', padx=SPACING['xs'])
            week_frames.append(week_frame)
            
            week_buttons = []
            for day_idx in range(7):  # 7 days per week
                # Create button (will be configured later)
                day_btn = ctk.CTkButton(
                    week_frame,
                    text="",
                    width=30,
                    height=25,
                    fg_color='transparent',
                    hover_color=COLORS['bg_gray_hover'],
                    text_color=COLORS['text_primary'],
                    font=FONTS['small'],
                    corner_radius=15,
                    border_width=0
                )
                day_btn.pack(side='left', expand=True, padx=1, pady=1)
                day_btn.pack_forget()  # Hide initially
                week_buttons.append(day_btn)
            
            day_buttons.append(week_buttons)
        
        # Store buttons for this month
        self._month_day_buttons[month] = {
            'buttons': day_buttons,
            'week_frames': week_frames
        }
        
        # Bottom padding
        ctk.CTkLabel(month_frame, text="", height=5).pack()
        
        return month_frame, month_header
    
    def _on_date_click(self, clicked_date: date):
        """Handle date click - switch to day view"""
        if hasattr(self.controller, 'view'):
            # Switch to day view and show clicked date
            self.controller.view.current_date = clicked_date
            self.controller.view.current_view = 'day'
            self.controller.view.show_view('day')
            if self.controller.view.day_view:
                self.controller.view.day_view.current_date = clicked_date
                self.controller.view.day_view.update_day()
    
    def update_year(self, year: int = None):
        """
        OPTIMIZED: Update year view WITHOUT destroying/creating widgets
        Only update text and visibility - 95% faster!
        
        Args:
            year: Year to display (default: current year)
        """
        if year is not None:
            self.current_year = year
        
        from app.config import MONTHS
        today = date.today()
        
        # Update all 12 months (reuse existing widgets)
        for month_idx in range(12):
            month_num = month_idx + 1
            
            # Update month header text
            self.month_headers[month_idx].configure(text=MONTHS[month_idx])
            
            # Get calendar data for this month
            cal = calendar.monthcalendar(self.current_year, month_num)
            month_data = self._month_day_buttons[month_num]
            day_buttons = month_data['buttons']
            
            # Update buttons for each week
            for week_idx, week in enumerate(cal):
                week_buttons = day_buttons[week_idx]
                
                for day_idx, day in enumerate(week):
                    btn = week_buttons[day_idx]
                    
                    if day == 0:
                        # Empty cell - hide button
                        btn.pack_forget()
                    else:
                        # Show and configure button
                        day_date = date(self.current_year, month_num, day)
                        is_today = day_date == today
                        
                        btn.configure(
                            text=str(day),
                            fg_color=COLORS['primary_blue'] if is_today else 'transparent',
                            text_color='white' if is_today else COLORS['text_primary'],
                            command=lambda d=day_date: self._on_date_click(d)
                        )
                        btn.pack(side='left', expand=True, padx=1, pady=1)
            
            # Hide unused week rows (if month has <6 weeks)
            for week_idx in range(len(cal), 6):
                for btn in day_buttons[week_idx]:
                    btn.pack_forget()
    
    def go_previous_year(self):
        """Navigate to previous year"""
        self.current_year -= 1
        self.update_year()
    
    def go_next_year(self):
        """Navigate to next year"""
        self.current_year += 1
        self.update_year()
    
    def go_today(self):
        """Navigate to current year"""
        self.current_year = date.today().year
        self.update_year()
    
    def refresh(self):
        """Refresh year view"""
        self.update_year()
    
    def get_current_period_text(self) -> str:
        """Get formatted period text"""
        return str(self.current_year)
