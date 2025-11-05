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
        
        # WIDGET POOLING: Store widgets for reuse
        self._date_headers = []  # Pool of date header widgets
        self._event_cards = []   # Pool of event card widgets
        self._widgets_in_use = [] # Track what's currently displayed
        
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
        """OPTIMIZED: Update schedule view with widget pooling (no destroy!)"""
        # Hide all widgets currently in use (return to pool)
        for widget_data in self._widgets_in_use:
            widget_data['widget'].pack_forget()
            if widget_data['type'] == 'header':
                self._date_headers.append(widget_data)
            else:
                self._event_cards.append(widget_data)
        self._widgets_in_use = []
        
        # Get events for next 30 days
        events_by_date = self._get_upcoming_events()
        
        if not events_by_date:
            # Show empty state (reuse or create)
            empty_label = self._get_or_create_date_header()
            empty_label['widget'].configure(
                text="📭 Không có sự kiện nào sắp tới",
                text_color=COLORS['text_secondary']
            )
            empty_label['widget'].pack(pady=SPACING['xxl'])
            self._widgets_in_use.append(empty_label)
            return
        
        # Create date sections (reuse widgets)
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
    
    def _get_or_create_date_header(self):
        """WIDGET POOLING: Get date header from pool or create new"""
        if self._date_headers:
            return self._date_headers.pop()
        
        # Create new date header
        date_header = ctk.CTkFrame(
            self.scroll_frame,
            fg_color='transparent',
            corner_radius=6
        )
        date_label = ctk.CTkLabel(
            date_header,
            text="",
            font=FONTS['subheading'],
            anchor='w'
        )
        date_label.pack(side='left', padx=SPACING['sm'], pady=SPACING['xs'])
        
        count_label = ctk.CTkLabel(
            date_header,
            text="",
            font=FONTS['caption'],
            text_color=COLORS['text_secondary']
        )
        count_label.pack(side='right', padx=SPACING['sm'], pady=SPACING['xs'])
        
        return {
            'type': 'header',
            'widget': date_header,
            'date_label': date_label,
            'count_label': count_label
        }
    
    def _get_or_create_event_card(self):
        """WIDGET POOLING: Get event card from pool or create new"""
        if self._event_cards:
            return self._event_cards.pop()
        
        # Create new event card
        card = ctk.CTkFrame(
            self.scroll_frame,
            fg_color=COLORS['bg_white'],
            border_width=1,
            border_color=COLORS['border_light'],
            corner_radius=8
        )
        
        inner_frame = ctk.CTkFrame(card, fg_color='transparent')
        inner_frame.pack(fill='both', expand=True, padx=SPACING['sm'], pady=SPACING['sm'])
        
        color_bar = ctk.CTkFrame(
            inner_frame,
            width=4,
            corner_radius=2
        )
        color_bar.pack(side='left', fill='y', padx=(0, SPACING['sm']))
        
        content_frame = ctk.CTkFrame(inner_frame, fg_color='transparent')
        content_frame.pack(side='left', fill='both', expand=True)
        
        name_label = ctk.CTkLabel(
            content_frame,
            text="",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary'],
            anchor='w'
        )
        name_label.pack(fill='x', anchor='w')
        
        info_label = ctk.CTkLabel(
            content_frame,
            text="",
            font=FONTS['caption'],
            text_color=COLORS['text_secondary'],
            anchor='w'
        )
        info_label.pack(fill='x', anchor='w', pady=(SPACING['xs'], 0))
        
        return {
            'type': 'card',
            'widget': card,
            'color_bar': color_bar,
            'name_label': name_label,
            'info_label': info_label
        }
    
    def _create_date_section(self, event_date: date, events: List):
        """
        OPTIMIZED: Reuse date header and event cards from pool
        
        Args:
            event_date: Date for this section
            events: List of Event objects for this date
        """
        # Date header text
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
        
        # WIDGET POOLING: Reuse date header
        header_data = self._get_or_create_date_header()
        header_data['widget'].configure(
            fg_color=COLORS['bg_gray'] if is_today else 'transparent'
        )
        header_data['date_label'].configure(
            text=date_text,
            text_color=COLORS['primary_blue'] if is_today else COLORS['text_primary']
        )
        header_data['count_label'].configure(text=f"{len(events)} sự kiện")
        header_data['widget'].pack(fill='x', pady=(SPACING['md'], SPACING['xs']), padx=SPACING['sm'])
        self._widgets_in_use.append(header_data)
        
        # Event list
        for event in sorted(events, key=lambda e: e.start_time if e.start_time else datetime.min):
            self._create_event_card(event)
    
    def _create_event_card(self, event):
        """
        OPTIMIZED: Reuse event card from pool
        
        Args:
            event: Event object
        """
        # WIDGET POOLING: Reuse event card
        card_data = self._get_or_create_event_card()
        
        # Update properties
        card_data['color_bar'].configure(fg_color=event.category_color)
        card_data['name_label'].configure(text=event.event_name)
        
        # Update time info
        if event.start_time:
            time_str = event.start_time.strftime("%H:%M")
            if event.end_time:
                time_str += f" - {event.end_time.strftime('%H:%M')}"
            info_text = f"⏰ {time_str}  •  📂 {event.category}"
            card_data['info_label'].configure(text=info_text)
        else:
            card_data['info_label'].configure(text=f"📂 {event.category}")
        
        # Update click handler
        try:
            card_data['widget'].unbind("<Button-1>")
        except:
            pass
        card_data['widget'].bind("<Button-1>", lambda e: self._on_event_click(event))
        
        # Show card
        card_data['widget'].pack(fill='x', pady=SPACING['xs'], padx=SPACING['md'])
        self._widgets_in_use.append(card_data)
    
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
