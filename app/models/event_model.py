"""
Event Model
Data model for calendar events
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Event:
    """
    Event data model - Google Calendar style
    Represents a single calendar event with all its properties
    """
    id: Optional[int] = None
    event_name: str = ""
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: str = ""
    reminder_minutes: int = 0
    status: str = "pending"  # pending, notified, cancelled
    category: str = "other"  # họp, khám, ăn, học, thể thao, giải trí
    
    @property
    def category_color(self) -> str:
        """
        Get Google Calendar style color for event category
        
        Returns:
            Hex color string
        """
        colors = {
            'họp': '#1967D2',      # Blue - Meetings
            'khám': '#D50000',     # Red - Medical appointments
            'ăn': '#F4511E',       # Orange - Food/meals
            'học': '#0B8043',      # Green - Study/learning
            'thể thao': '#F09300', # Yellow-orange - Sports
            'giải trí': '#7B1FA2', # Purple - Entertainment
            'other': '#5F6368'     # Gray - Other
        }
        return colors.get(self.category, colors['other'])
    
    @property
    def is_all_day(self) -> bool:
        """Check if this is an all-day event"""
        if not self.start_time or not self.end_time:
            return True
        
        # Check if time is midnight to midnight
        return (
            self.start_time.hour == 0 and 
            self.start_time.minute == 0 and
            self.end_time.hour == 23 and 
            self.end_time.minute == 59
        )
    
    @property
    def duration_minutes(self) -> int:
        """Get event duration in minutes"""
        if not self.start_time or not self.end_time:
            return 0
        
        delta = self.end_time - self.start_time
        return int(delta.total_seconds() / 60)
    
    @property
    def is_past(self) -> bool:
        """Check if event is in the past"""
        if not self.start_time:
            return False
        return self.start_time < datetime.now()
    
    @property
    def is_upcoming(self) -> bool:
        """Check if event is in the future"""
        if not self.start_time:
            return False
        return self.start_time > datetime.now()
    
    @property
    def is_today(self) -> bool:
        """Check if event is today"""
        if not self.start_time:
            return False
        today = datetime.now().date()
        return self.start_time.date() == today
    
    def get_formatted_time(self) -> str:
        """
        Get formatted time string for display
        
        Returns:
            Formatted time string (e.g., "10:00 - 11:30")
        """
        if not self.start_time:
            return "Chưa xác định"
        
        if self.is_all_day:
            return "Cả ngày"
        
        start_str = self.start_time.strftime("%H:%M")
        
        if self.end_time:
            end_str = self.end_time.strftime("%H:%M")
            return f"{start_str} - {end_str}"
        
        return start_str
    
    def get_formatted_date(self) -> str:
        """
        Get formatted date string for display
        
        Returns:
            Formatted date string (e.g., "Thứ 2, 05/11/2024")
        """
        if not self.start_time:
            return "Chưa xác định"
        
        weekdays = [
            "Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5",
            "Thứ 6", "Thứ 7", "Chủ nhật"
        ]
        weekday = weekdays[self.start_time.weekday()]
        date_str = self.start_time.strftime("%d/%m/%Y")
        
        return f"{weekday}, {date_str}"
    
    def get_reminder_text(self) -> str:
        """
        Get human-readable reminder time
        
        Returns:
            Reminder text (e.g., "30 phút trước", "1 giờ trước")
        """
        if self.reminder_minutes == 0:
            return "Không nhắc nhở"
        elif self.reminder_minutes < 60:
            return f"{self.reminder_minutes} phút trước"
        else:
            hours = self.reminder_minutes // 60
            if hours == 1:
                return "1 giờ trước"
            elif hours == 24:
                return "1 ngày trước"
            elif hours % 24 == 0:
                days = hours // 24
                return f"{days} ngày trước"
            else:
                return f"{hours} giờ trước"
    
    def to_dict(self) -> dict:
        """
        Convert Event to dictionary for database storage
        
        Returns:
            Dictionary representation
        """
        return {
            'id': self.id,
            'event_name': self.event_name,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'location': self.location,
            'reminder_minutes': self.reminder_minutes,
            'status': self.status
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Event':
        """
        Create Event from database row dictionary
        
        Args:
            data: Dictionary containing event data
            
        Returns:
            Event object
        """
        event = cls()
        event.id = data.get('id')
        event.event_name = data.get('event_name', '')
        
        # Parse datetime strings from database
        if data.get('start_time'):
            try:
                event.start_time = datetime.fromisoformat(data['start_time'])
            except (ValueError, TypeError):
                # Try parsing from Vietnamese format (dd/mm/yyyy HH:MM)
                try:
                    event.start_time = datetime.strptime(data['start_time'], "%d/%m/%Y %H:%M")
                except (ValueError, TypeError):
                    event.start_time = None
        
        if data.get('end_time'):
            try:
                event.end_time = datetime.fromisoformat(data['end_time'])
            except (ValueError, TypeError):
                try:
                    event.end_time = datetime.strptime(data['end_time'], "%d/%m/%Y %H:%M")
                except (ValueError, TypeError):
                    event.end_time = None
        
        event.location = data.get('location', '')
        event.reminder_minutes = data.get('reminder_minutes', 0)
        event.status = data.get('status', 'pending')
        
        # Auto-detect category from event name
        event.category = event._detect_category()
        
        return event
    
    def _detect_category(self) -> str:
        """
        Auto-detect event category from event name using keywords
        
        Returns:
            Category string
        """
        keywords = {
            'họp': ['họp', 'meeting', 'gặp', 'phỏng vấn', 'cuộc họp', 'hội nghị'],
            'khám': ['khám', 'bác sĩ', 'nha khoa', 'bệnh viện', 'phòng khám', 'y tế'],
            'ăn': ['ăn', 'cơm', 'trưa', 'tối', 'nhà hàng', 'quán', 'bữa', 'tiệc'],
            'học': ['học', 'lớp', 'bài', 'thi', 'kiểm tra', 'giảng', 'khóa học'],
            'thể thao': ['gym', 'chạy', 'bơi', 'thể thao', 'yoga', 'tập', 'fitness'],
            'giải trí': ['phim', 'xem', 'chơi', 'du lịch', 'concert', 'show']
        }
        
        name_lower = self.event_name.lower()
        for category, words in keywords.items():
            if any(word in name_lower for word in words):
                return category
        return 'other'
    
    def update_from_dict(self, data: dict):
        """
        Update event fields from dictionary
        
        Args:
            data: Dictionary with fields to update
        """
        if 'event_name' in data:
            self.event_name = data['event_name']
        
        if 'start_time' in data:
            if isinstance(data['start_time'], datetime):
                self.start_time = data['start_time']
            elif isinstance(data['start_time'], str):
                try:
                    self.start_time = datetime.fromisoformat(data['start_time'])
                except ValueError:
                    pass
        
        if 'end_time' in data:
            if isinstance(data['end_time'], datetime):
                self.end_time = data['end_time']
            elif isinstance(data['end_time'], str):
                try:
                    self.end_time = datetime.fromisoformat(data['end_time'])
                except ValueError:
                    pass
        
        if 'location' in data:
            self.location = data['location']
        
        if 'reminder_minutes' in data:
            self.reminder_minutes = data['reminder_minutes']
        
        if 'status' in data:
            self.status = data['status']
        
        if 'category' in data:
            self.category = data['category']
        else:
            # Re-detect category if name changed
            self.category = self._detect_category()
    
    def __str__(self) -> str:
        """String representation of Event"""
        return f"Event({self.event_name}, {self.get_formatted_date()}, {self.get_formatted_time()})"
    
    def __repr__(self) -> str:
        """Debug representation of Event"""
        return (
            f"Event(id={self.id}, name='{self.event_name}', "
            f"start={self.start_time}, category='{self.category}')"
        )
