"""
Calendar State Model
Manages the current calendar view state (date, view type, filters)
"""
from datetime import date, datetime, timedelta
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class CalendarState:
    """
    Represents the current state of the calendar view
    """
    current_date: date = field(default_factory=date.today)
    view_type: str = "month"  # day, week, month, year, schedule
    selected_calendars: List[str] = field(default_factory=lambda: ["work", "health", "study"])
    search_query: str = ""
    filter_category: Optional[str] = None
    
    def get_view_period_text(self) -> str:
        """Get formatted text for current period"""
        if self.view_type == "day":
            return self.current_date.strftime("%d/%m/%Y")
        elif self.view_type == "week":
            week_num = self.current_date.isocalendar()[1]
            return f"Tuần {week_num}, {self.current_date.year}"
        elif self.view_type == "month":
            months_vi = [
                "Tháng 1", "Tháng 2", "Tháng 3", "Tháng 4",
                "Tháng 5", "Tháng 6", "Tháng 7", "Tháng 8",
                "Tháng 9", "Tháng 10", "Tháng 11", "Tháng 12"
            ]
            return f"{months_vi[self.current_date.month - 1]}, {self.current_date.year}"
        elif self.view_type == "year":
            return f"Năm {self.current_date.year}"
        return self.current_date.strftime("%d/%m/%Y")
    
    def go_to_today(self):
        """Reset to today's date"""
        self.current_date = date.today()
    
    def go_previous(self):
        """Navigate to previous period based on view type"""
        if self.view_type == "day":
            self.current_date -= timedelta(days=1)
        elif self.view_type == "week":
            self.current_date -= timedelta(weeks=1)
        elif self.view_type == "month":
            # Go to previous month
            if self.current_date.month == 1:
                self.current_date = self.current_date.replace(year=self.current_date.year - 1, month=12)
            else:
                self.current_date = self.current_date.replace(month=self.current_date.month - 1)
        elif self.view_type == "year":
            self.current_date = self.current_date.replace(year=self.current_date.year - 1)
    
    def go_next(self):
        """Navigate to next period based on view type"""
        if self.view_type == "day":
            self.current_date += timedelta(days=1)
        elif self.view_type == "week":
            self.current_date += timedelta(weeks=1)
        elif self.view_type == "month":
            # Go to next month
            if self.current_date.month == 12:
                self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=1)
            else:
                self.current_date = self.current_date.replace(month=self.current_date.month + 1)
        elif self.view_type == "year":
            self.current_date = self.current_date.replace(year=self.current_date.year + 1)
    
    def set_view_type(self, view_type: str):
        """Change view type"""
        valid_views = ["day", "week", "month", "year", "schedule"]
        if view_type in valid_views:
            self.view_type = view_type
    
    def toggle_calendar(self, calendar_name: str):
        """Toggle calendar visibility"""
        if calendar_name in self.selected_calendars:
            self.selected_calendars.remove(calendar_name)
        else:
            self.selected_calendars.append(calendar_name)
    
    def set_search_query(self, query: str):
        """Update search query"""
        self.search_query = query
    
    def set_filter_category(self, category: Optional[str]):
        """Set event category filter"""
        self.filter_category = category
    
    def clear_filters(self):
        """Clear all filters"""
        self.search_query = ""
        self.filter_category = None
    
    def get_week_start_end(self) -> tuple[date, date]:
        """Get start and end dates of current week"""
        # Monday as first day of week
        start = self.current_date - timedelta(days=self.current_date.weekday())
        end = start + timedelta(days=6)
        return start, end
    
    def get_month_start_end(self) -> tuple[date, date]:
        """Get start and end dates of current month"""
        start = self.current_date.replace(day=1)
        # Last day of month
        if start.month == 12:
            end = start.replace(year=start.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            end = start.replace(month=start.month + 1, day=1) - timedelta(days=1)
        return start, end
    
    def get_year_start_end(self) -> tuple[date, date]:
        """Get start and end dates of current year"""
        start = self.current_date.replace(month=1, day=1)
        end = self.current_date.replace(month=12, day=31)
        return start, end
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            "current_date": self.current_date.isoformat(),
            "view_type": self.view_type,
            "selected_calendars": self.selected_calendars,
            "search_query": self.search_query,
            "filter_category": self.filter_category,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'CalendarState':
        """Create from dictionary"""
        return cls(
            current_date=datetime.fromisoformat(data["current_date"]).date(),
            view_type=data["view_type"],
            selected_calendars=data["selected_calendars"],
            search_query=data.get("search_query", ""),
            filter_category=data.get("filter_category"),
        )
