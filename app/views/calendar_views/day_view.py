"""
Day View Component
Detailed hourly timeline for a single day
"""
import customtkinter as ctk
from datetime import date, datetime, timedelta, time
from typing import Dict, List
from app.config import COLORS, FONTS, SPACING


class DayView(ctk.CTkFrame):
    """
    Day view with detailed hourly timeline (Google Calendar style)
    Shows one day with hourly slots and detailed event information
    """
    
    def __init__(self, parent, controller):
        """
        Initialize day view
        
        Args:
            parent: Parent widget
            controller: MainController instance
        """
        super().__init__(parent, fg_color=COLORS['bg_white'])
        
        self.controller = controller
        self.current_date = date.today()
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup day view UI"""
        # Main container
        self.container = ctk.CTkFrame(self, fg_color='transparent')
        self.container.pack(fill='both', expand=True, padx=SPACING['md'], pady=SPACING['md'])
        
        # Create header with date
        self._create_day_header()
        
        # Create scrollable timeline area
        self._create_timeline()
    
    def _create_day_header(self):
        """Create header row with day name and date"""
        header_frame = ctk.CTkFrame(
            self.container,
            fg_color='transparent',
            height=80
        )
        header_frame.pack(fill='x', pady=(0, SPACING['sm']))
        header_frame.pack_propagate(False)
        
        # Date information
        weekdays_vi = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'Chủ nhật']
        weekday = weekdays_vi[self.current_date.weekday()]
        
        # Day name
        self.weekday_label = ctk.CTkLabel(
            header_frame,
            text=weekday,
            font=FONTS['heading'],
            text_color=COLORS['text_secondary']
        )
        self.weekday_label.pack(pady=(SPACING['sm'], 0))
        
        # Date
        date_text = self.current_date.strftime("%d tháng %m, %Y")
        self.date_label = ctk.CTkLabel(
            header_frame,
            text=date_text,
            font=FONTS['title'],
            text_color=COLORS['primary_blue']
        )
        self.date_label.pack()
    
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
            height=80  # Taller than week view for more details
        )
        row_frame.pack(fill='x', pady=1)
        row_frame.pack_propagate(False)
        
        # Time label (left side)
        time_text = f"{hour:02d}:00"
        time_label = ctk.CTkLabel(
            row_frame,
            text=time_text,
            font=FONTS['body'],
            text_color=COLORS['text_secondary'],
            width=80,
            anchor='ne'
        )
        time_label.pack(side='left', padx=(0, SPACING['md']))
        
        # Event container (wider for detailed view)
        event_container = ctk.CTkFrame(
            row_frame,
            fg_color=COLORS['bg_white'],
            border_width=1,
            border_color=COLORS['border_light']
        )
        event_container.pack(side='left', fill='both', expand=True)
        
        self.hour_rows.append({
            'hour': hour,
            'frame': row_frame,
            'container': event_container
        })
    
    def update_day(self, target_date: date = None):
        """
        Update day view with events
        
        Args:
            target_date: Date to display
        """
        if target_date is not None:
            self.current_date = target_date
        
        # Update header
        self._update_header()
        
        # Clear existing events
        self._clear_event_blocks()
        
        # Get events for this day
        events = self._get_events_for_day()
        
        # Place event blocks in timeline
        self._place_event_blocks(events)
    
    def _update_header(self):
        """Update header with current date"""
        weekdays_vi = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'Chủ nhật']
        weekday = weekdays_vi[self.current_date.weekday()]
        date_text = self.current_date.strftime("%d tháng %m, %Y")
        
        self.weekday_label.configure(text=weekday)
        self.date_label.configure(text=date_text)
    
    def _clear_event_blocks(self):
        """Clear all event blocks from timeline"""
        for row_data in self.hour_rows:
            container = row_data['container']
            for widget in container.winfo_children():
                widget.destroy()
    
    def _get_events_for_day(self) -> List:
        """
        Get events for current day
        
        Returns:
            List of Event objects
        """
        if not hasattr(self.controller, 'model'):
            return []
        
        try:
            events = self.controller.model.get_events_for_date_range(
                self.current_date,
                self.current_date
            )
            # Sort by start time
            return sorted(events, key=lambda e: e.start_time if e.start_time else time(0, 0))
        except Exception as e:
            print(f"Error getting events for day: {e}")
            return []
    
    def _place_event_blocks(self, events: List):
        """
        Place event blocks in timeline containers
        
        Args:
            events: List of Event objects
        """
        for event in events:
            if not event.start_time:
                continue
            
            # Calculate which hour container this event belongs to
            start_hour = event.start_time.hour
            start_minute = event.start_time.minute
            
            # Calculate duration in hours
            if event.end_time:
                duration_hours = (event.end_time - event.start_time).total_seconds() / 3600
            else:
                duration_hours = 1  # Default 1 hour
            
            # Create event block
            self._create_event_block(start_hour, start_minute, duration_hours, event)
    
    def _create_event_block(self, start_hour: int, start_minute: int, 
                           duration_hours: float, event):
        """
        Create a detailed event block in the timeline
        
        Args:
            start_hour: Starting hour (0-23)
            start_minute: Starting minute (0-59)
            duration_hours: Duration in hours
            event: Event object
        """
        if start_hour >= 24:
            return
        
        # Find the container
        container = self.hour_rows[start_hour]['container']
        
        # Calculate vertical position and height
        # Each hour container is 80px, position based on minutes
        y_offset = int((start_minute / 60) * 80)
        block_height = max(60, int(duration_hours * 80))  # Min 60px for readability
        
        # Get container width for block width calculation
        container.update_idletasks()
        block_width = max(300, container.winfo_width() - 8)  # Leave 8px padding
        
        # Create event block
        event_block = ctk.CTkFrame(
            container,
            width=block_width,
            height=block_height,
            fg_color=event.category_color,
            corner_radius=8
        )
        
        event_block.place(x=4, y=y_offset)
        
        # Event content container
        content_frame = ctk.CTkFrame(
            event_block,
            fg_color='transparent'
        )
        content_frame.pack(fill='both', expand=True, padx=SPACING['sm'], pady=SPACING['sm'])
        
        # Event title
        event_label = ctk.CTkLabel(
            content_frame,
            text=event.event_name,
            font=FONTS['body_bold'],
            text_color='white',
            anchor='nw',
            justify='left'
        )
        event_label.pack(anchor='nw', pady=(0, SPACING['xs']))
        
        # Time display
        if event.start_time and event.end_time:
            time_text = f"{event.start_time.strftime('%H:%M')} - {event.end_time.strftime('%H:%M')}"
            time_label = ctk.CTkLabel(
                content_frame,
                text=time_text,
                font=FONTS['small'],
                text_color='white',
                anchor='nw'
            )
            time_label.pack(anchor='nw', pady=(0, SPACING['xs']))
        
        # Category (if height allows)
        if block_height > 80:
            category_label = ctk.CTkLabel(
                content_frame,
                text=f"📁 {event.category}",
                font=FONTS['small'],
                text_color='white',
                anchor='nw'
            )
            category_label.pack(anchor='nw')
        
        # Click handler
        event_block.bind("<Button-1>", lambda e: self._on_event_click(event))
        event_label.bind("<Button-1>", lambda e: self._on_event_click(event))
    
    def _on_event_click(self, event):
        """Handle event block click"""
        if hasattr(self.controller, 'handle_event_clicked'):
            self.controller.handle_event_clicked(event.id)
    
    def go_previous_day(self):
        """Navigate to previous day"""
        self.current_date -= timedelta(days=1)
        self.update_day()
    
    def go_next_day(self):
        """Navigate to next day"""
        self.current_date += timedelta(days=1)
        self.update_day()
    
    def go_today(self):
        """Navigate to today"""
        self.current_date = date.today()
        self.update_day()
    
    def refresh(self):
        """Refresh day view"""
        self.update_day()
    
    def get_current_period_text(self) -> str:
        """Get formatted period text"""
        return self.current_date.strftime("%d/%m/%Y")
