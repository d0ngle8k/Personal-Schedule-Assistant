"""
Phase 1 Integration Test
Tests the MVC architecture with existing database
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.models import Event, CalendarModel
from database.db_manager import DatabaseManager
from datetime import datetime, date


def test_event_model():
    """Test Event model"""
    print("\n" + "="*50)
    print("Testing Event Model")
    print("="*50)
    
    # Create event
    event = Event(
        id=1,
        event_name="Họp nhóm dự án",
        start_time=datetime(2024, 11, 5, 14, 0),
        end_time=datetime(2024, 11, 5, 15, 30),
        location="Phòng họp A",
        reminder_minutes=30,
        status="pending"
    )
    
    print(f"Event: {event}")
    print(f"Category: {event.category}")
    print(f"Color: {event.category_color}")
    print(f"Formatted time: {event.get_formatted_time()}")
    print(f"Formatted date: {event.get_formatted_date()}")
    print(f"Duration: {event.duration_minutes} minutes")
    print(f"Is today: {event.is_today}")
    print(f"Reminder: {event.get_reminder_text()}")
    
    # Test to_dict and from_dict
    event_dict = event.to_dict()
    print(f"\nDict: {event_dict}")
    
    event2 = Event.from_dict(event_dict)
    print(f"Reconstructed: {event2}")
    
    print("✅ Event model test passed!")


def test_calendar_model():
    """Test CalendarModel"""
    print("\n" + "="*50)
    print("Testing Calendar Model")
    print("="*50)
    
    # Initialize database
    db = DatabaseManager("database/events.db")
    model = CalendarModel(db)
    
    print(f"Current date: {model.state.current_date}")
    print(f"View type: {model.state.view_type}")
    print(f"Period text: {model.get_current_period_text()}")
    
    # Test navigation
    print("\n--- Testing Navigation ---")
    model.navigate_today()
    print(f"Today: {model.get_current_period_text()}")
    
    model.navigate_next()
    print(f"Next: {model.get_current_period_text()}")
    
    model.navigate_previous()
    print(f"Previous: {model.get_current_period_text()}")
    
    model.navigate_today()
    print(f"Back to today: {model.get_current_period_text()}")
    
    # Test view types
    print("\n--- Testing View Types ---")
    for view in ["day", "week", "month", "year", "schedule"]:
        model.set_view_type(view)
        print(f"{view.capitalize()} view: {model.get_current_period_text()}")
    
    # Test event queries
    print("\n--- Testing Event Queries ---")
    model.set_view_type("month")
    model.navigate_today()
    
    events = model.get_events_for_current_view()
    print(f"Events this month: {len(events)}")
    
    if events:
        print("\nFirst 5 events:")
        for event in events[:5]:
            print(f"  - {event.event_name} ({event.get_formatted_date()})")
    
    # Test upcoming events
    upcoming = model.get_upcoming_events(7)
    print(f"\nUpcoming events (next 7 days): {len(upcoming)}")
    
    if upcoming:
        print("Next 3 upcoming:")
        for event in upcoming[:3]:
            print(f"  - {event.event_name} ({event.get_formatted_date()} at {event.get_formatted_time()})")
    
    # Test statistics
    print("\n--- Testing Statistics ---")
    today = date.today()
    count_today = model.get_event_count_for_date(today)
    print(f"Events today: {count_today}")
    
    all_events = model.get_all_events()
    print(f"Total events in database: {len(all_events)}")
    
    # Group by category
    by_category = model.group_events_by_category(all_events)
    print("\nEvents by category:")
    for category, events_list in by_category.items():
        print(f"  {category}: {len(events_list)} events")
    
    print("\n✅ Calendar model test passed!")


def test_database_integration():
    """Test integration with existing database"""
    print("\n" + "="*50)
    print("Testing Database Integration")
    print("="*50)
    
    db = DatabaseManager("database/events.db")
    
    # Get all events
    all_events = db.get_all_events()
    print(f"Total events in database: {len(all_events)}")
    
    if all_events:
        print("\nSample events:")
        for row in all_events[:3]:
            event = Event.from_dict(row)
            print(f"  - ID: {event.id}")
            print(f"    Name: {event.event_name}")
            print(f"    Time: {event.get_formatted_time()}")
            print(f"    Category: {event.category} ({event.category_color})")
            print()
    
    # Search events
    print("--- Testing Search ---")
    search_results = db.search_events_by_name("họp")
    print(f"Events containing 'họp': {len(search_results)}")
    
    print("✅ Database integration test passed!")


def main():
    """Run all tests"""
    print("="*50)
    print("Phase 1 Integration Test")
    print("Testing MVC Architecture with Existing Database")
    print("="*50)
    
    try:
        # Test each component
        test_event_model()
        test_calendar_model()
        test_database_integration()
        
        print("\n" + "="*50)
        print("✅ ALL TESTS PASSED!")
        print("Phase 1 MVC Architecture is working correctly")
        print("="*50)
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
