"""
Calendar Model
Business logic for calendar operations and event management
"""
from datetime import date, datetime, timedelta
from typing import List, Optional, Dict
from functools import lru_cache
from app.models.event_model import Event
from app.models.calendar_state import CalendarState


class CalendarModel:
    """
    Manages calendar business logic and event operations
    """
    
    def __init__(self, db_manager):
        """
        Initialize calendar model with database manager
        
        Args:
            db_manager: DatabaseManager instance from database.db_manager
        """
        self.db = db_manager
        self.state = CalendarState()
        self._event_cache_version = 0  # Increment when events change
    
    # ==================== Event CRUD Operations ====================
    
    def create_event(self, event: Event) -> bool:
        """
        Create a new event
        
        Args:
            event: Event object to create
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            event_data = event.to_dict()
            
            # Remove None id for new events
            if event_data['id'] is None:
                del event_data['id']
            
            # Prepare event dict for database
            db_event = {
                'event_name': event_data['event_name'],
                'start_time': event_data['start_time'],
                'end_time': event_data.get('end_time'),
                'location': event_data.get('location', ''),
                'reminder_minutes': event_data.get('reminder_minutes', 0)
            }
            
            result = self.db.add_event(db_event)
            success = result.get('success', False)
            if success:
                self._invalidate_cache()  # Clear cache after create
            return success
        except Exception as e:
            print(f"Error creating event: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def update_event(self, event: Event) -> bool:
        """
        Update an existing event
        
        Args:
            event: Event object with updated data
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            event_data = event.to_dict()
            # Prepare event dict for database
            db_event = {
                'event_name': event_data['event_name'],
                'start_time': event_data['start_time'],
                'end_time': event_data.get('end_time'),
                'location': event_data.get('location', ''),
                'reminder_minutes': event_data.get('reminder_minutes', 0)
            }
            result = self.db.update_event(event_data['id'], db_event)
            success = result.get('success', False)
            if success:
                self._invalidate_cache()  # Clear cache after update
            return success
        except Exception as e:
            print(f"Error updating event: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def delete_event(self, event_id: int) -> bool:
        """
        Delete an event
        
        Args:
            event_id: ID of event to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.db.delete_event(event_id)
            self._invalidate_cache()  # Clear cache after delete
            return True
        except Exception as e:
            print(f"Error deleting event: {e}")
            return False
    
    def get_event_by_id(self, event_id: int) -> Optional[Event]:
        """
        Get a single event by ID
        
        Args:
            event_id: Event ID
            
        Returns:
            Event object or None if not found
        """
        try:
            event_dict = self.db.get_event_by_id(event_id)
            if event_dict:
                return Event.from_dict(event_dict)
            return None
        except Exception as e:
            print(f"Error getting event: {e}")
            return None
    
    def _invalidate_cache(self):
        """Invalidate cache when events are modified"""
        self._event_cache_version += 1
        # Clear any cached queries
        if hasattr(self, '_cached_events'):
            delattr(self, '_cached_events')
    
    # ==================== Event Queries ====================
    
    def get_events_for_date(self, target_date: date) -> List[Event]:
        """
        Get all events for a specific date
        
        Args:
            target_date: Date to get events for
            
        Returns:
            List of Event objects
        """
        try:
            results = self.db.get_events_by_date(target_date)
            events = [Event.from_dict(row) for row in results]
            return self._apply_filters(events)
        except Exception as e:
            print(f"Error getting events for date: {e}")
            return []
    
    def get_events_for_date_range(self, start_date: date, end_date: date) -> List[Event]:
        """
        Get all events within a date range (OPTIMIZED: Single SQL query)
        
        Args:
            start_date: Start date (inclusive)
            end_date: End date (inclusive)
            
        Returns:
            List of Event objects
        """
        try:
            # OPTIMIZATION: Use single batch query instead of looping through dates
            results = self.db.get_events_by_date_range(start_date, end_date)
            
            # Convert to Event objects
            events = [Event.from_dict(row) for row in results]
            
            # Apply filters
            filtered_events = self._apply_filters(events)
            
            return filtered_events
        except Exception as e:
            print(f"Error getting events for range: {e}")
            return []
    
    def get_events_for_current_view(self) -> List[Event]:
        """
        Get events for current calendar view period
        
        Returns:
            List of Event objects
        """
        if self.state.view_type == "day":
            return self.get_events_for_date(self.state.current_date)
        
        elif self.state.view_type == "week":
            start, end = self.state.get_week_start_end()
            return self.get_events_for_date_range(start, end)
        
        elif self.state.view_type == "month":
            start, end = self.state.get_month_start_end()
            return self.get_events_for_date_range(start, end)
        
        elif self.state.view_type == "year":
            start, end = self.state.get_year_start_end()
            return self.get_events_for_date_range(start, end)
        
        elif self.state.view_type == "schedule":
            # For schedule view, show next 30 days
            today = date.today()
            end = today + timedelta(days=30)
            return self.get_events_for_date_range(today, end)
        
        return []
    
    def search_events(self, query: str, field: str = "name") -> List[Event]:
        """
        Search events by field
        
        Args:
            query: Search query
            field: Field to search (name, location, date, id)
            
        Returns:
            List of Event objects
        """
        try:
            if field == "name":
                results = self.db.search_events_by_name(query)
            elif field == "location":
                results = self.db.search_events_by_location(query)
            elif field == "id":
                try:
                    event_id = int(query)
                    results = self.db.search_events_by_id(event_id)
                except ValueError:
                    results = []
            else:
                results = []
            events = [Event.from_dict(row) for row in results]
            return self._apply_filters(events)
        except Exception as e:
            print(f"Error searching events: {e}")
            return []
    
    def get_all_events(self) -> List[Event]:
        """
        Get all events from database
        
        Returns:
            List of Event objects
        """
        try:
            results = self.db.get_all_events()
            events = [Event.from_dict(row) for row in results]
            return self._apply_filters(events)
        except Exception as e:
            print(f"Error getting all events: {e}")
            return []
    
    # ==================== Filtering & Grouping ====================
    
    def _apply_filters(self, events: List[Event]) -> List[Event]:
        """
        Apply current filters to event list
        
        Args:
            events: List of events to filter
            
        Returns:
            Filtered list of events
        """
        filtered = events
        
        # Apply search query
        if self.state.search_query:
            query_lower = self.state.search_query.lower()
            filtered = [
                e for e in filtered
                if query_lower in e.event_name.lower() or
                   query_lower in e.location.lower()
            ]
        
        # Apply category filter
        if self.state.filter_category:
            filtered = [
                e for e in filtered
                if e.category == self.state.filter_category
            ]
        
        return filtered
    
    def group_events_by_date(self, events: List[Event]) -> Dict[date, List[Event]]:
        """
        Group events by date
        
        Args:
            events: List of events
            
        Returns:
            Dictionary mapping date to list of events
        """
        grouped = {}
        for event in events:
            if event.start_time:
                event_date = event.start_time.date()
                if event_date not in grouped:
                    grouped[event_date] = []
                grouped[event_date].append(event)
        
        # Sort events within each date
        for event_date in grouped:
            grouped[event_date].sort(key=lambda e: e.start_time)
        
        return grouped
    
    def group_events_by_category(self, events: List[Event]) -> Dict[str, List[Event]]:
        """
        Group events by category
        
        Args:
            events: List of events
            
        Returns:
            Dictionary mapping category to list of events
        """
        grouped = {}
        for event in events:
            category = event.category
            if category not in grouped:
                grouped[category] = []
            grouped[category].append(event)
        
        return grouped
    
    # ==================== Statistics ====================
    
    def get_event_count_for_date(self, target_date: date) -> int:
        """
        Get count of events for a specific date
        
        Args:
            target_date: Date to count events for
            
        Returns:
            Number of events
        """
        return len(self.get_events_for_date(target_date))
    
    def get_upcoming_events(self, days: int = 7) -> List[Event]:
        """
        Get upcoming events within specified days
        
        Args:
            days: Number of days to look ahead
            
        Returns:
            List of upcoming Event objects
        """
        today = date.today()
        end_date = today + timedelta(days=days)
        events = self.get_events_for_date_range(today, end_date)
        
        # Filter to only future events
        now = datetime.now()
        upcoming = [
            e for e in events
            if e.start_time and e.start_time >= now
        ]
        
        return sorted(upcoming, key=lambda e: e.start_time)
    
    def get_overdue_events(self) -> List[Event]:
        """
        Get past events that haven't been marked as completed
        
        Returns:
            List of overdue Event objects
        """
        try:
            all_events = self.get_all_events()
            now = datetime.now()
            
            overdue = [
                e for e in all_events
                if e.start_time and e.start_time < now and e.status == "pending"
            ]
            
            return sorted(overdue, key=lambda e: e.start_time, reverse=True)
        except Exception as e:
            print(f"Error getting overdue events: {e}")
            return []
    
    # ==================== Calendar State Management ====================
    
    def set_current_date(self, target_date: date):
        """Update current view date"""
        self.state.current_date = target_date
    
    def set_view_type(self, view_type: str):
        """Change calendar view type"""
        self.state.set_view_type(view_type)
    
    def navigate_previous(self):
        """Navigate to previous period"""
        self.state.go_previous()
    
    def navigate_next(self):
        """Navigate to next period"""
        self.state.go_next()
    
    def navigate_today(self):
        """Navigate to today"""
        self.state.go_to_today()
    
    def set_search_query(self, query: str):
        """Update search query"""
        self.state.set_search_query(query)
    
    def set_category_filter(self, category: Optional[str]):
        """Set category filter"""
        self.state.set_filter_category(category)
    
    def clear_filters(self):
        """Clear all filters"""
        self.state.clear_filters()
    
    def get_current_period_text(self) -> str:
        """Get formatted text for current period"""
        return self.state.get_view_period_text()
