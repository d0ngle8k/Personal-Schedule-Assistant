"""
Month View Component
Main calendar grid showing a full month
"""
import customtkinter as ctk
from calendar import monthcalendar, month_name, day_name
from datetime import date, timedelta
from typing import Dict, List
from app.config import COLORS, FONTS, SPACING, LAYOUT
from app.views.calendar_views.day_cell import DayCell


class MonthView(ctk.CTkFrame):
    """
    Month calendar grid view (Google Calendar style)
    Displays a 7x6 grid of days with events
    """
    
    def __init__(self, parent, controller):
        """
        Initialize month view
        
        Args:
            parent: Parent widget
            controller: MainController instance
        """
        super().__init__(parent, fg_color=COLORS['bg_white'])
        
        self.controller = controller
        self.current_year = date.today().year
        self.current_month = date.today().month
        self.selected_date = date.today()
        self.day_cells: List[List[DayCell]] = []
        
        # PERFORMANCE: Cache for instant view switching
        self._events_cache = {}
        self._last_cache_key = None
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup month view UI"""
        # Main container with padding
        self.container = ctk.CTkFrame(
            self,
            fg_color='transparent'
        )
        self.container.pack(fill='both', expand=True, padx=SPACING['lg'], pady=SPACING['md'])
        
        # Weekday headers
        self._create_weekday_headers()
        
        # Calendar grid (6 rows x 7 columns)
        self._create_calendar_grid()
    
    def _create_weekday_headers(self):
        """Create weekday header row"""
        self.header_frame = ctk.CTkFrame(
            self.container,
            fg_color='transparent',
            height=40
        )
        self.header_frame.pack(fill='x', pady=(0, SPACING['sm']))
        self.header_frame.pack_propagate(False)
        
        # Vietnamese weekday names (Monday = T2, Sunday = CN)
        weekdays_vi = ['T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'CN']
        
        for i, day in enumerate(weekdays_vi):
            # Create header label
            header = ctk.CTkLabel(
                self.header_frame,
                text=day,
                font=FONTS['caption'],
                text_color=COLORS['text_secondary'],
                anchor='center'
            )
            header.grid(row=0, column=i, sticky='ew', padx=2)
            
            # Configure column weight for equal distribution
            self.header_frame.grid_columnconfigure(i, weight=1)
    
    def _create_calendar_grid(self):
        """Create 6x7 grid of day cells"""
        self.grid_frame = ctk.CTkFrame(
            self.container,
            fg_color='transparent'
        )
        self.grid_frame.pack(fill='both', expand=True)
        
        # Create 6 rows (weeks)
        for row in range(6):
            row_cells = []
            
            # Create 7 columns (days)
            for col in range(7):
                cell = DayCell(self.grid_frame, self.controller)
                cell.grid(row=row, column=col, padx=2, pady=2, sticky='nsew')
                row_cells.append(cell)
                
                # Configure column weight for responsive layout
                self.grid_frame.grid_columnconfigure(col, weight=1)
            
            # Configure row weight for responsive layout
            self.grid_frame.grid_rowconfigure(row, weight=1)
            
            self.day_cells.append(row_cells)
    
    def update_calendar(self, year: int = None, month: int = None, selected_date: date = None):
        """
        Update calendar display with dates and events
        
        Args:
            year: Year to display (default: current year)
            month: Month to display (default: current month)
            selected_date: Date to highlight as selected
        """
        if year is not None:
            self.current_year = year
        if month is not None:
            self.current_month = month
        if selected_date is not None:
            self.selected_date = selected_date
        
        # Get calendar data for this month
        cal = monthcalendar(self.current_year, self.current_month)
        today = date.today()
        
        # Get all events for this month from controller
        events_by_date = self._get_events_for_month()
        
        # Calculate dates for empty cells at start/end
        # Get first and last actual dates in calendar
        first_week = cal[0]
        last_week = cal[-1]
        
        # Find first non-zero day
        first_day_of_month = next((day for day in first_week if day != 0), 1)
        first_date = date(self.current_year, self.current_month, first_day_of_month)
        
        # Calculate previous month dates
        prev_month_dates = []
        if 0 in first_week:
            # Need dates from previous month
            prev_month_last_date = first_date - timedelta(days=1)
            days_needed = first_week.index(first_day_of_month)
            for i in range(days_needed):
                prev_date = prev_month_last_date - timedelta(days=days_needed - 1 - i)
                prev_month_dates.append(prev_date)
        
        # Calculate next month dates
        next_month_dates = []
        if 0 in last_week:
            # Need dates from next month
            last_day_of_month = next((day for day in reversed(last_week) if day != 0), 1)
            last_date = date(self.current_year, self.current_month, last_day_of_month)
            days_needed = last_week[::-1].index(last_day_of_month)
            for i in range(days_needed):
                next_date = last_date + timedelta(days=i + 1)
                next_month_dates.append(next_date)
        
        # Fill calendar grid
        prev_month_idx = 0
        next_month_idx = 0
        
        for week_idx, week in enumerate(cal):
            for day_idx, day in enumerate(week):
                cell = self.day_cells[week_idx][day_idx]
                
                if day == 0:
                    # Empty cell - fill with prev or next month date
                    if week_idx == 0 and prev_month_idx < len(prev_month_dates):
                        # Previous month date
                        date_obj = prev_month_dates[prev_month_idx]
                        prev_month_idx += 1
                        is_current_month = False
                    elif week_idx > 0 and next_month_idx < len(next_month_dates):
                        # Next month date
                        date_obj = next_month_dates[next_month_idx]
                        next_month_idx += 1
                        is_current_month = False
                    else:
                        # Truly empty
                        cell.set_date(None)
                        continue
                else:
                    # Current month date
                    date_obj = date(self.current_year, self.current_month, day)
                    is_current_month = True
                
                # Check if this is today
                is_today = date_obj == today
                
                # Check if this is selected date
                is_selected = date_obj == self.selected_date
                
                # Get events for this date
                events = events_by_date.get(date_obj, [])
                
                # Update cell
                cell.set_date(
                    date_obj=date_obj,
                    is_today=is_today,
                    is_current_month=is_current_month,
                    events=events,
                    is_selected=is_selected
                )
    
    def _get_events_for_month(self) -> Dict[date, List]:
        """
        Get events grouped by date for current month
        
        Returns:
            Dictionary mapping date to list of Event objects
        ULTRA OPTIMIZED: Cache events for instant view switches
        """
        if not hasattr(self.controller, 'model'):
            return {}
        
        try:
            # Generate cache key
            cache_key = f"{self.current_year}-{self.current_month:02d}"
            
            # OPTIMIZATION: Return cached data if same month (instant!)
            if cache_key == self._last_cache_key and self._events_cache:
                return self._events_cache
            
            # Get first and last day of month
            first_day = date(self.current_year, self.current_month, 1)
            
            # Get last day of month
            if self.current_month == 12:
                last_day = date(self.current_year + 1, 1, 1) - timedelta(days=1)
            else:
                last_day = date(self.current_year, self.current_month + 1, 1) - timedelta(days=1)
            
            # Also get a few days before and after for prev/next month dates
            start_date = first_day - timedelta(days=7)
            end_date = last_day + timedelta(days=7)
            
            # Get events from model
            events = self.controller.model.get_events_for_date_range(start_date, end_date)
            
            # Group by date
            events_by_date = self.controller.model.group_events_by_date(events)
            
            # CACHE the result for instant future access
            self._events_cache = events_by_date
            self._last_cache_key = cache_key
            
            return events_by_date
        
        except Exception as e:
            print(f"Error getting events for month: {e}")
            return {}
    
    def clear_cache(self):
        """Clear events cache when data changes"""
        self._events_cache = {}
        self._last_cache_key = None
    
    def refresh(self):
        """Refresh calendar display (uses cached data if available)"""
        self.update_calendar(
            year=self.current_year,
            month=self.current_month,
            selected_date=self.selected_date
        )
    
    def go_to_date(self, target_date: date):
        """
        Navigate to specific date
        
        Args:
            target_date: Date to display
        """
        self.current_year = target_date.year
        self.current_month = target_date.month
        self.selected_date = target_date
        self.refresh()
    
    def go_previous_month(self):
        """Navigate to previous month"""
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.refresh()
    
    def go_next_month(self):
        """Navigate to next month"""
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.refresh()
    
    def go_today(self):
        """Navigate to today"""
        today = date.today()
        self.current_year = today.year
        self.current_month = today.month
        self.selected_date = today
        self.refresh()
    
    def get_current_period_text(self) -> str:
        """
        Get formatted period text for display
        
        Returns:
            String like "Tháng 11, 2025"
        """
        months_vi = [
            "Tháng 1", "Tháng 2", "Tháng 3", "Tháng 4",
            "Tháng 5", "Tháng 6", "Tháng 7", "Tháng 8",
            "Tháng 9", "Tháng 10", "Tháng 11", "Tháng 12"
        ]
        return f"{months_vi[self.current_month - 1]}, {self.current_year}"
