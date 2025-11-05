"""
Week View Component
Hourly timeline with 7-day columns showing events
"""
import customtkinter as ctk
from datetime import date, datetime, timedelta
from typing import Dict, List
from app.config import COLORS, FONTS, SPACING


class WeekView(ctk.CTkFrame):
    """
    Week view with hourly timeline (Google Calendar style)
    Shows 7 days (Monday-Sunday) with hourly slots
    """
    
    def __init__(self, parent, controller):
        """
        Initialize week view
        
        Args:
            parent: Parent widget
            controller: MainController instance
        """
        super().__init__(parent, fg_color=COLORS['bg_white'])
        
        self.controller = controller
        self.current_date = date.today()
        self.week_start = self._get_week_start(self.current_date)
        
        self._setup_ui()
    
    def _get_week_start(self, target_date: date) -> date:
        """Get Monday of the week containing target_date"""
        return target_date - timedelta(days=target_date.weekday())
    
    def _setup_ui(self):
        """Setup week view UI"""
        # Main container with scrolling
        self.container = ctk.CTkFrame(self, fg_color='transparent')
        self.container.pack(fill='both', expand=True, padx=SPACING['md'], pady=SPACING['md'])
        
        # Create header with day names and dates
        self._create_week_header()
        
        # Create scrollable timeline area
        self._create_timeline()
    
    def _create_week_header(self):
        """Create header row with day names and dates"""
        header_frame = ctk.CTkFrame(
            self.container,
            fg_color='transparent',
            height=60
        )
        header_frame.pack(fill='x', pady=(0, SPACING['sm']))
        header_frame.pack_propagate(False)
        
        # Time column placeholder (for alignment)
        time_col = ctk.CTkFrame(
            header_frame,
            fg_color='transparent',
            width=60
        )
        time_col.pack(side='left', fill='y')
        
        # Day columns (7 days)
        weekdays_vi = ['THỨ 2', 'THỨ 3', 'THỨ 4', 'THỨ 5', 'THỨ 6', 'THỨ 7', 'CHỦ NHẬT']
        
        self.day_headers = []
        for i in range(7):
            day_date = self.week_start + timedelta(days=i)
            is_today = day_date == date.today()
            
            # Day column header
            day_frame = ctk.CTkFrame(
                header_frame,
                fg_color=COLORS['primary_blue_light'] if is_today else 'transparent'
            )
            day_frame.pack(side='left', fill='both', expand=True, padx=1)
            
            # Weekday name
            weekday_label = ctk.CTkLabel(
                day_frame,
                text=weekdays_vi[i],
                font=FONTS['caption'],
                text_color=COLORS['text_secondary']
            )
            weekday_label.pack(pady=(SPACING['xs'], 0))
            
            # Date number
            date_label = ctk.CTkLabel(
                day_frame,
                text=str(day_date.day),
                font=FONTS['heading'] if is_today else FONTS['body_bold'],
                text_color=COLORS['primary_blue'] if is_today else COLORS['text_primary']
            )
            date_label.pack()
            
            self.day_headers.append(day_frame)
    
    def _create_timeline(self):
        """Create scrollable hourly timeline"""
        # Create scrollable frame
        self.timeline_scroll = ctk.CTkScrollableFrame(
            self.container,
            fg_color='transparent'
        )
        self.timeline_scroll.pack(fill='both', expand=True)
        
        # Timeline grid container
        self.timeline_grid = ctk.CTkFrame(
            self.timeline_scroll,
            fg_color='transparent'
        )
        self.timeline_grid.pack(fill='both', expand=True)
        
        # Create 24 hour rows
        self.hour_rows = []
        for hour in range(24):
            self._create_hour_row(hour)
    
    def _create_hour_row(self, hour: int):
        """Create one hour row in timeline"""
        row_frame = ctk.CTkFrame(
            self.timeline_grid,
            fg_color='transparent',
            height=60
        )
        row_frame.pack(fill='x', pady=1)
        row_frame.pack_propagate(False)
        
        # Time label (left side)
        time_text = f"{hour:02d}:00"
        time_label = ctk.CTkLabel(
            row_frame,
            text=time_text,
            font=FONTS['caption'],
            text_color=COLORS['text_secondary'],
            width=60,
            anchor='ne'
        )
        time_label.pack(side='left', padx=(0, SPACING['sm']))
        
        # Day columns (7 slots)
        day_slots = []
        for day_idx in range(7):
            slot = ctk.CTkFrame(
                row_frame,
                fg_color=COLORS['bg_white'],
                border_width=1,
                border_color=COLORS['border_light']
            )
            slot.pack(side='left', fill='both', expand=True, padx=1)
            day_slots.append(slot)
        
        self.hour_rows.append({
            'hour': hour,
            'frame': row_frame,
            'slots': day_slots
        })
    
    def update_week(self, start_date: date = None):
        """
        Update week view with events
        
        Args:
            start_date: Monday of week to display
        """
        if start_date is not None:
            self.week_start = self._get_week_start(start_date)
            self.current_date = start_date
        
        # Clear existing events from slots
        self._clear_event_blocks()
        
        # Get events for this week
        events_by_date = self._get_events_for_week()
        
        # Place event blocks in timeline
        self._place_event_blocks(events_by_date)
        
        # Update headers
        self._update_headers()
    
    def _clear_event_blocks(self):
        """Clear all event blocks from timeline"""
        for row_data in self.hour_rows:
            for slot in row_data['slots']:
                for widget in slot.winfo_children():
                    widget.destroy()
    
    def _get_events_for_week(self) -> Dict[date, List]:
        """
        Get events grouped by date for current week
        
        Returns:
            Dictionary mapping date to list of Event objects
        """
        if not hasattr(self.controller, 'model'):
            return {}
        
        try:
            # Get events for 7 days
            end_date = self.week_start + timedelta(days=6)
            events = self.controller.model.get_events_for_date_range(self.week_start, end_date)
            return self.controller.model.group_events_by_date(events)
        except Exception as e:
            print(f"Error getting events for week: {e}")
            return {}
    
    def _place_event_blocks(self, events_by_date: Dict[date, List]):
        """
        Place event blocks in timeline slots
        
        Args:
            events_by_date: Events grouped by date
        """
        for day_idx in range(7):
            day_date = self.week_start + timedelta(days=day_idx)
            day_events = events_by_date.get(day_date, [])
            
            for event in day_events:
                if not event.start_time:
                    continue
                
                # Calculate which hour slot this event belongs to
                start_hour = event.start_time.hour
                start_minute = event.start_time.minute
                
                # Calculate duration in hours
                if event.end_time:
                    duration_hours = (event.end_time - event.start_time).total_seconds() / 3600
                else:
                    duration_hours = 1  # Default 1 hour
                
                # Create event block
                self._create_event_block(day_idx, start_hour, start_minute, duration_hours, event)
    
    def _create_event_block(self, day_idx: int, start_hour: int, start_minute: int, 
                           duration_hours: float, event):
        """
        Create an event block in the timeline
        
        Args:
            day_idx: Day index (0-6)
            start_hour: Starting hour (0-23)
            start_minute: Starting minute (0-59)
            duration_hours: Duration in hours
            event: Event object
        """
        if start_hour >= 24:
            return
        
        # Find the slot
        slot = self.hour_rows[start_hour]['slots'][day_idx]
        
        # Calculate vertical position and height
        # Each hour slot is 60px, position based on minutes
        y_offset = int((start_minute / 60) * 60)
        block_height = max(20, int(duration_hours * 60))  # Min 20px
        
        # Get slot width for block width calculation
        slot.update_idletasks()
        slot_width = max(100, slot.winfo_width() - 4)  # Leave 4px padding
        
        # Create event block
        event_block = ctk.CTkFrame(
            slot,
            width=slot_width,
            height=block_height,
            fg_color=event.category_color,
            corner_radius=4
        )
        
        event_block.place(x=2, y=y_offset)
        
        # Event text (truncate if needed)
        event_text = event.event_name[:20] + "..." if len(event.event_name) > 20 else event.event_name
        
        event_label = ctk.CTkLabel(
            event_block,
            text=event_text,
            font=FONTS['small'],
            text_color='white',
            anchor='nw'
        )
        event_label.pack(padx=4, pady=2, anchor='nw')
        
        # Click handler
        event_block.bind("<Button-1>", lambda e: self._on_event_click(event))
        event_label.bind("<Button-1>", lambda e: self._on_event_click(event))
    
    def _on_event_click(self, event):
        """Handle event block click"""
        if hasattr(self.controller, 'handle_event_clicked'):
            self.controller.handle_event_clicked(event.id)
    
    def _update_headers(self):
        """Update day headers for current week"""
        weekdays_vi = ['THỨ 2', 'THỨ 3', 'THỨ 4', 'THỨ 5', 'THỨ 6', 'THỨ 7', 'CHỦ NHẬT']
        
        for i, header_frame in enumerate(self.day_headers):
            day_date = self.week_start + timedelta(days=i)
            is_today = day_date == date.today()
            
            # Update background color
            header_frame.configure(
                fg_color=COLORS['primary_blue_light'] if is_today else 'transparent'
            )
            
            # Update labels
            for widget in header_frame.winfo_children():
                widget.destroy()
            
            # Weekday name
            weekday_label = ctk.CTkLabel(
                header_frame,
                text=weekdays_vi[i],
                font=FONTS['caption'],
                text_color=COLORS['text_secondary']
            )
            weekday_label.pack(pady=(SPACING['xs'], 0))
            
            # Date number
            date_label = ctk.CTkLabel(
                header_frame,
                text=str(day_date.day),
                font=FONTS['heading'] if is_today else FONTS['body_bold'],
                text_color=COLORS['primary_blue'] if is_today else COLORS['text_primary']
            )
            date_label.pack()
    
    def go_previous_week(self):
        """Navigate to previous week"""
        self.week_start -= timedelta(days=7)
        self.current_date = self.week_start
        self.update_week()
    
    def go_next_week(self):
        """Navigate to next week"""
        self.week_start += timedelta(days=7)
        self.current_date = self.week_start
        self.update_week()
    
    def go_today(self):
        """Navigate to current week"""
        today = date.today()
        self.week_start = self._get_week_start(today)
        self.current_date = today
        self.update_week()
    
    def refresh(self):
        """Refresh week view"""
        self.update_week()
    
    def get_current_period_text(self) -> str:
        """Get formatted period text"""
        week_num = self.week_start.isocalendar()[1]
        return f"Tuần {week_num}, {self.week_start.year}"
