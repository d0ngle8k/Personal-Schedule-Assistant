"""
Mini Calendar Widget
Small calendar widget for sidebar navigation (Google Calendar style)
"""
import customtkinter as ctk
from datetime import date, timedelta
import calendar
from app.config import COLORS, FONTS, SPACING, WEEKDAYS_SHORT


class MiniCalendar(ctk.CTkFrame):
    """
    Mini calendar widget for sidebar
    Shows current month with clickable dates
    """
    
    def __init__(self, parent, controller, on_date_click=None):
        """
        Initialize mini calendar
        
        Args:
            parent: Parent widget
            controller: MainController instance
            on_date_click: Callback function(date) when date is clicked
        """
        super().__init__(
            parent,
            fg_color=COLORS['bg_white'],
            corner_radius=8,
            border_width=1,
            border_color=COLORS['border_light']
        )
        
        self.controller = controller
        self.on_date_click = on_date_click
        self.current_date = date.today()
        self.display_year = self.current_date.year
        self.display_month = self.current_date.month
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup mini calendar UI"""
        # Header with month/year and navigation
        self._create_header()
        
        # Weekday labels
        self._create_weekday_labels()
        
        # Calendar grid
        self.calendar_grid_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.calendar_grid_frame.pack(fill='both', expand=True, padx=SPACING['xs'], pady=(0, SPACING['xs']))
        
        # Initial calendar display
        self.update_calendar()
    
    def _create_header(self):
        """Create header with month/year and navigation arrows"""
        header = ctk.CTkFrame(self, fg_color='transparent')
        header.pack(fill='x', padx=SPACING['xs'], pady=(SPACING['xs'], 0))
        
        # Previous month button
        prev_btn = ctk.CTkButton(
            header,
            text="◀",
            width=24,
            height=24,
            fg_color='transparent',
            text_color=COLORS['text_primary'],
            hover_color=COLORS['bg_gray_hover'],
            font=FONTS['caption'],
            corner_radius=12,
            command=self._go_previous_month
        )
        prev_btn.pack(side='left', padx=(SPACING['xs'], 0))
        
        # Month/Year label
        self.month_year_label = ctk.CTkLabel(
            header,
            text=self._get_month_year_text(),
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        self.month_year_label.pack(side='left', expand=True)
        
        # Next month button
        next_btn = ctk.CTkButton(
            header,
            text="▶",
            width=24,
            height=24,
            fg_color='transparent',
            text_color=COLORS['text_primary'],
            hover_color=COLORS['bg_gray_hover'],
            font=FONTS['caption'],
            corner_radius=12,
            command=self._go_next_month
        )
        next_btn.pack(side='right', padx=(0, SPACING['xs']))
    
    def _create_weekday_labels(self):
        """Create weekday header row"""
        weekday_frame = ctk.CTkFrame(self, fg_color='transparent')
        weekday_frame.pack(fill='x', padx=SPACING['xs'], pady=(SPACING['xs'], 0))
        
        for weekday in WEEKDAYS_SHORT:
            label = ctk.CTkLabel(
                weekday_frame,
                text=weekday,
                font=FONTS['small'],
                text_color=COLORS['text_secondary'],
                width=28
            )
            label.pack(side='left', expand=True)
    
    def _get_month_year_text(self) -> str:
        """Get formatted month/year text"""
        months_vi = [
            "Tháng 1", "Tháng 2", "Tháng 3", "Tháng 4",
            "Tháng 5", "Tháng 6", "Tháng 7", "Tháng 8",
            "Tháng 9", "Tháng 10", "Tháng 11", "Tháng 12"
        ]
        return f"{months_vi[self.display_month - 1]} {self.display_year}"
    
    def update_calendar(self):
        """Update calendar display"""
        # Clear existing calendar
        for widget in self.calendar_grid_frame.winfo_children():
            widget.destroy()
        
        # Get calendar for current month
        cal = calendar.monthcalendar(self.display_year, self.display_month)
        
        # Create date buttons
        for week in cal:
            week_frame = ctk.CTkFrame(self.calendar_grid_frame, fg_color='transparent')
            week_frame.pack(fill='x')
            
            for day_num in week:
                if day_num == 0:
                    # Empty cell
                    empty_label = ctk.CTkLabel(
                        week_frame,
                        text="",
                        width=28,
                        height=24
                    )
                    empty_label.pack(side='left', expand=True)
                else:
                    # Day button
                    day_date = date(self.display_year, self.display_month, day_num)
                    is_today = day_date == date.today()
                    is_selected = day_date == self.current_date
                    
                    # Determine button style
                    if is_today:
                        fg_color = COLORS['primary_blue']
                        text_color = 'white'
                        font = FONTS['body_bold']
                    elif is_selected:
                        fg_color = COLORS['primary_blue_light']
                        text_color = COLORS['primary_blue']
                        font = FONTS['body']
                    else:
                        fg_color = 'transparent'
                        text_color = COLORS['text_primary']
                        font = FONTS['caption']
                    
                    day_btn = ctk.CTkButton(
                        week_frame,
                        text=str(day_num),
                        width=28,
                        height=24,
                        fg_color=fg_color,
                        hover_color=COLORS['bg_gray_hover'] if not is_today else COLORS['primary_blue_hover'],
                        text_color=text_color,
                        font=font,
                        corner_radius=12,
                        border_width=0,
                        command=lambda d=day_date: self._on_day_click(d)
                    )
                    day_btn.pack(side='left', expand=True, padx=1, pady=1)
        
        # Update month/year label
        self.month_year_label.configure(text=self._get_month_year_text())
    
    def _on_day_click(self, clicked_date: date):
        """Handle day click"""
        self.current_date = clicked_date
        self.update_calendar()
        
        # Call callback if provided
        if self.on_date_click:
            self.on_date_click(clicked_date)
        
        # Navigate main calendar to this date
        if hasattr(self.controller, 'view'):
            view = self.controller.view
            view.current_date = clicked_date
            
            # Update appropriate view
            if view.current_view == 'month' and view.month_view:
                view.month_view.current_year = clicked_date.year
                view.month_view.current_month = clicked_date.month
                view.month_view.update_calendar()
            elif view.current_view == 'day' and view.day_view:
                view.day_view.current_date = clicked_date
                view.day_view.update_day()
            elif view.current_view == 'week' and view.week_view:
                view.week_view.week_start = view.week_view._get_week_start(clicked_date)
                view.week_view.current_date = clicked_date
                view.week_view.update_week()
    
    def _go_previous_month(self):
        """Go to previous month"""
        if self.display_month == 1:
            self.display_month = 12
            self.display_year -= 1
        else:
            self.display_month -= 1
        
        self.update_calendar()
    
    def _go_next_month(self):
        """Go to next month"""
        if self.display_month == 12:
            self.display_month = 1
            self.display_year += 1
        else:
            self.display_month += 1
        
        self.update_calendar()
    
    def go_to_today(self):
        """Navigate to today"""
        today = date.today()
        self.display_year = today.year
        self.display_month = today.month
        self.current_date = today
        self.update_calendar()
