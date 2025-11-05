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
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup year view UI"""
        # Scrollable container for 12 months
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=COLORS['bg_white']
        )
        self.scroll_frame.pack(fill='both', expand=True, padx=SPACING['lg'], pady=SPACING['lg'])
        
        # Create 12 month grid (4 rows × 3 columns)
        self.month_frames = []
        for row in range(4):
            row_frame = ctk.CTkFrame(self.scroll_frame, fg_color='transparent')
            row_frame.pack(fill='x', pady=SPACING['sm'])
            
            for col in range(3):
                month_num = row * 3 + col + 1  # 1-12
                month_widget = self._create_month_mini_calendar(row_frame, month_num)
                month_widget.pack(side='left', fill='both', expand=True, padx=SPACING['sm'])
                self.month_frames.append(month_widget)
    
    def _create_month_mini_calendar(self, parent, month: int):
        """
        Create mini calendar for one month
        
        Args:
            parent: Parent frame
            month: Month number (1-12)
            
        Returns:
            Frame containing mini calendar
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
        
        # Month name header
        month_header = ctk.CTkLabel(
            month_frame,
            text=MONTHS[month - 1],
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        month_header.pack(pady=(SPACING['sm'], SPACING['xs']))
        
        # Weekday headers
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
        
        # Calendar grid
        cal = calendar.monthcalendar(self.current_year, month)
        
        for week in cal:
            week_frame = ctk.CTkFrame(month_frame, fg_color='transparent')
            week_frame.pack(fill='x', padx=SPACING['xs'])
            
            for day in week:
                if day == 0:
                    # Empty cell
                    empty_label = ctk.CTkLabel(
                        week_frame,
                        text="",
                        width=30,
                        height=25
                    )
                    empty_label.pack(side='left', expand=True)
                else:
                    # Day cell
                    day_date = date(self.current_year, month, day)
                    is_today = day_date == date.today()
                    
                    day_btn = ctk.CTkButton(
                        week_frame,
                        text=str(day),
                        width=30,
                        height=25,
                        fg_color=COLORS['primary_blue'] if is_today else 'transparent',
                        hover_color=COLORS['bg_gray_hover'],
                        text_color='white' if is_today else COLORS['text_primary'],
                        font=FONTS['small'],
                        corner_radius=15,
                        border_width=0,
                        command=lambda d=day_date: self._on_date_click(d)
                    )
                    day_btn.pack(side='left', expand=True, padx=1, pady=1)
        
        # Bottom padding
        ctk.CTkLabel(month_frame, text="", height=5).pack()
        
        return month_frame
    
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
        Update year view
        
        Args:
            year: Year to display (default: current year)
        """
        if year is not None:
            self.current_year = year
        
        # Rebuild month grids
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        self.month_frames = []
        for row in range(4):
            row_frame = ctk.CTkFrame(self.scroll_frame, fg_color='transparent')
            row_frame.pack(fill='x', pady=SPACING['sm'])
            
            for col in range(3):
                month_num = row * 3 + col + 1
                month_widget = self._create_month_mini_calendar(row_frame, month_num)
                month_widget.pack(side='left', fill='both', expand=True, padx=SPACING['sm'])
                self.month_frames.append(month_widget)
    
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
