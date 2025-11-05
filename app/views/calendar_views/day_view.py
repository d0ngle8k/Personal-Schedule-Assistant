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
        
        # PERFORMANCE: Cache for instant view switching
        self._events_cache = []
        self._last_cache_key = None
        
        # WIDGET POOLING: Store event blocks for reuse
        self._event_blocks = []
        self._event_blocks_in_use = []
        
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
        """OPTIMIZED: Hide event blocks for reuse (no destroy!)"""
        for event_block in self._event_blocks_in_use:
            event_block['frame'].place_forget()  # Hide
            self._event_blocks.append(event_block)  # Return to pool
        self._event_blocks_in_use = []  # Clear in-use list
    
    def _get_events_for_day(self) -> List:
        """
        ULTRA OPTIMIZED: Get events with smart caching
        
        Returns:
            List of Event objects
        """
        if not hasattr(self.controller, 'model'):
            return []
        
        try:
            # Generate cache key
            cache_key = self.current_date.isoformat()
            
            # OPTIMIZATION: Return cached data if same day (instant!)
            if cache_key == self._last_cache_key and self._events_cache:
                return self._events_cache
            
            events = self.controller.model.get_events_for_date_range(
                self.current_date,
                self.current_date
            )
            # Sort by start time
            sorted_events = sorted(events, key=lambda e: e.start_time if e.start_time else time(0, 0))
            
            # CACHE the result
            self._events_cache = sorted_events
            self._last_cache_key = cache_key
            
            return sorted_events
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
        OPTIMIZED: Reuse event block from pool or create new
        
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
        y_offset = int((start_minute / 60) * 80)
        block_height = max(60, int(duration_hours * 80))
        
        # Get container width
        container.update_idletasks()
        block_width = max(300, container.winfo_width() - 8)
        
        # WIDGET POOLING: Reuse from pool or create new
        if self._event_blocks:
            # Reuse existing block
            block_data = self._event_blocks.pop()
            event_block = block_data['frame']
            content_frame = block_data['content']
            event_label = block_data['title']
            time_label = block_data['time']
            category_label = block_data['category']
            
            # Update properties
            event_block.configure(
                width=block_width,
                height=block_height,
                fg_color=event.category_color
            )
            event_label.configure(text=event.event_name)
            
            # Update time
            if event.start_time and event.end_time:
                time_text = f"{event.start_time.strftime('%H:%M')} - {event.end_time.strftime('%H:%M')}"
                time_label.configure(text=time_text)
                time_label.pack(anchor='nw', pady=(0, SPACING['xs']))
            else:
                time_label.pack_forget()
            
            # Update category
            if block_height > 80:
                category_label.configure(text=f"📁 {event.category}")
                category_label.pack(anchor='nw')
            else:
                category_label.pack_forget()
            
            # Update click handler
            try:
                event_block.unbind("<Button-1>")
                event_label.unbind("<Button-1>")
            except:
                pass
            event_block.bind("<Button-1>", lambda e: self._on_event_click(event))
            event_label.bind("<Button-1>", lambda e: self._on_event_click(event))
            
            # CRITICAL: Place widget in new container
            event_block.place(x=4, y=y_offset, in_=container)
            event_block.lift()
            
        else:
            # Create new block with THIS VIEW as parent (allows flexible placement)
            event_block = ctk.CTkFrame(
                self,  # Parent is view itself, not container
                width=block_width,
                height=block_height,
                fg_color=event.category_color,
                corner_radius=8
            )
            
            # Content container
            content_frame = ctk.CTkFrame(
                event_block,
                fg_color='transparent'
            )
            content_frame.pack(fill='both', expand=True, padx=SPACING['sm'], pady=SPACING['sm'])
            
            # Title label
            event_label = ctk.CTkLabel(
                content_frame,
                text=event.event_name,
                font=FONTS['body_bold'],
                text_color='white',
                anchor='nw',
                justify='left'
            )
            event_label.pack(anchor='nw', pady=(0, SPACING['xs']))
            
            # Time label
            time_label = ctk.CTkLabel(
                content_frame,
                text="",
                font=FONTS['small'],
                text_color='white',
                anchor='nw'
            )
            if event.start_time and event.end_time:
                time_text = f"{event.start_time.strftime('%H:%M')} - {event.end_time.strftime('%H:%M')}"
                time_label.configure(text=time_text)
                time_label.pack(anchor='nw', pady=(0, SPACING['xs']))
            
            # Category label
            category_label = ctk.CTkLabel(
                content_frame,
                text=f"📁 {event.category}",
                font=FONTS['small'],
                text_color='white',
                anchor='nw'
            )
            if block_height > 80:
                category_label.pack(anchor='nw')
            
            # Click handler
            event_block.bind("<Button-1>", lambda e: self._on_event_click(event))
            event_label.bind("<Button-1>", lambda e: self._on_event_click(event))
            
            # Store widget references
            block_data = {
                'frame': event_block,
                'content': content_frame,
                'title': event_label,
                'time': time_label,
                'category': category_label
            }
            
            # Position block
            event_block.place(x=4, y=y_offset, in_=container)
        
        # Track as in-use
        self._event_blocks_in_use.append(block_data)
    
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
    
    def clear_cache(self):
        """Clear events cache when data changes"""
        self._events_cache = []
        self._last_cache_key = None
    
    def refresh(self):
        """Refresh day view (uses cached data if available)"""
        self.update_day()
    
    def get_current_period_text(self) -> str:
        """Get formatted period text"""
        return self.current_date.strftime("%d/%m/%Y")
