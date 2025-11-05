"""
Schedule/Agenda View Component
List of upcoming events in chronological order (Google Calendar style)
"""
import customtkinter as ctk
from datetime import date, datetime, timedelta
from typing import List
from app.config import COLORS, FONTS, SPACING


class ScheduleView(ctk.CTkFrame):
    """
    Schedule/Agenda view showing upcoming events in list format
    Groups events by date with clear sections
    """
    
    def __init__(self, parent, controller):
        """
        Initialize schedule view
        
        Args:
            parent: Parent widget
            controller: MainController instance
        """
        super().__init__(parent, fg_color=COLORS['bg_white'])
        
        self.controller = controller
        self.current_date = date.today()
        self.days_ahead = 30  # Show next 30 days
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup schedule view UI"""
        # Scrollable container
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=COLORS['bg_white']
        )
        self.scroll_frame.pack(fill='both', expand=True, padx=SPACING['lg'], pady=SPACING['md'])
        
        # Empty state label (will be replaced with events)
        self.empty_label = ctk.CTkLabel(
            self.scroll_frame,
            text="📅 Đang tải sự kiện...",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        self.empty_label.pack(pady=SPACING['xl'])
    
    def update_schedule(self):
        """Update schedule view with events"""
        # Clear existing widgets
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        # Get events for next 30 days
        events_by_date = self._get_upcoming_events()
        
        if not events_by_date:
            # Show empty state
            empty_label = ctk.CTkLabel(
                self.scroll_frame,
                text="📭 Không có sự kiện nào sắp tới",
                font=FONTS['heading'],
                text_color=COLORS['text_secondary']
            )
            empty_label.pack(pady=SPACING['xxl'])
            return
        
        # Create date sections
        for event_date in sorted(events_by_date.keys()):
            self._create_date_section(event_date, events_by_date[event_date])
    
    def _get_upcoming_events(self) -> dict:
        """
        Get events for next 30 days grouped by date
        
        Returns:
            Dictionary mapping date to list of events
        """
        if not hasattr(self.controller, 'model'):
            return {}
        
        try:
            end_date = self.current_date + timedelta(days=self.days_ahead)
            events = self.controller.model.get_events_for_date_range(self.current_date, end_date)
            return self.controller.model.group_events_by_date(events)
        except Exception as e:
            print(f"Error getting upcoming events: {e}")
            return {}
    
    def _create_date_section(self, event_date: date, events: List):
        """
        Create a section for one date with its events
        
        Args:
            event_date: Date for this section
            events: List of Event objects for this date
        """
        # Date header
        is_today = event_date == date.today()
        is_tomorrow = event_date == date.today() + timedelta(days=1)
        
        if is_today:
            date_text = f"Hôm nay - {event_date.strftime('%d/%m/%Y')}"
        elif is_tomorrow:
            date_text = f"Ngày mai - {event_date.strftime('%d/%m/%Y')}"
        else:
            weekday_names = ['Thứ hai', 'Thứ ba', 'Thứ tư', 'Thứ năm', 'Thứ sáu', 'Thứ bảy', 'Chủ nhật']
            weekday = weekday_names[event_date.weekday()]
            date_text = f"{weekday}, {event_date.strftime('%d/%m/%Y')}"
        
        date_header = ctk.CTkFrame(
            self.scroll_frame,
            fg_color=COLORS['bg_gray'] if is_today else 'transparent',
            corner_radius=6
        )
        date_header.pack(fill='x', pady=(SPACING['md'], SPACING['xs']), padx=SPACING['sm'])
        
        date_label = ctk.CTkLabel(
            date_header,
            text=date_text,
            font=FONTS['subheading'],
            text_color=COLORS['primary_blue'] if is_today else COLORS['text_primary'],
            anchor='w'
        )
        date_label.pack(side='left', padx=SPACING['sm'], pady=SPACING['xs'])
        
        # Event count
        count_label = ctk.CTkLabel(
            date_header,
            text=f"{len(events)} sự kiện",
            font=FONTS['caption'],
            text_color=COLORS['text_secondary']
        )
        count_label.pack(side='right', padx=SPACING['sm'], pady=SPACING['xs'])
        
        # Event list
        for event in sorted(events, key=lambda e: e.start_time if e.start_time else datetime.min):
            self._create_event_card(event)
    
    def _create_event_card(self, event):
        """
        Create event card in list
        
        Args:
            event: Event object
        """
        # Event card
        card = ctk.CTkFrame(
            self.scroll_frame,
            fg_color=COLORS['bg_white'],
            border_width=1,
            border_color=COLORS['border_light'],
            corner_radius=8
        )
        card.pack(fill='x', pady=SPACING['xs'], padx=SPACING['md'])
        
        # Add click handler
        card.bind("<Button-1>", lambda e: self._on_event_click(event))
        
        # Inner padding frame
        inner_frame = ctk.CTkFrame(card, fg_color='transparent')
        inner_frame.pack(fill='both', expand=True, padx=SPACING['sm'], pady=SPACING['sm'])
        
        # Left side - Color indicator
        color_bar = ctk.CTkFrame(
            inner_frame,
            width=4,
            fg_color=event.category_color,
            corner_radius=2
        )
        color_bar.pack(side='left', fill='y', padx=(0, SPACING['sm']))
        
        # Content frame
        content_frame = ctk.CTkFrame(inner_frame, fg_color='transparent')
        content_frame.pack(side='left', fill='both', expand=True)
        
        # Event name
        name_label = ctk.CTkLabel(
            content_frame,
            text=event.event_name,
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary'],
            anchor='w'
        )
        name_label.pack(fill='x', anchor='w')
        
        # Time and category
        if event.start_time:
            time_str = event.start_time.strftime("%H:%M")
            if event.end_time:
                time_str += f" - {event.end_time.strftime('%H:%M')}"
            
            info_text = f"⏰ {time_str}  •  📂 {event.category}"
            
            info_label = ctk.CTkLabel(
                content_frame,
                text=info_text,
                font=FONTS['caption'],
                text_color=COLORS['text_secondary'],
                anchor='w'
            )
            info_label.pack(fill='x', anchor='w', pady=(SPACING['xs'], 0))
    
    def _on_event_click(self, event):
        """Handle event click"""
        if hasattr(self.controller, 'handle_event_clicked'):
            self.controller.handle_event_clicked(event.id)
    
    def go_today(self):
        """Reset to show from today"""
        self.current_date = date.today()
        self.update_schedule()
    
    def refresh(self):
        """Refresh schedule view"""
        self.update_schedule()
    
    def get_current_period_text(self) -> str:
        """Get formatted period text"""
        end_date = self.current_date + timedelta(days=self.days_ahead)
        return f"Lịch trình: {self.current_date.strftime('%d/%m')} - {end_date.strftime('%d/%m/%Y')}"
