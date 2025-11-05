"""
Performance Profiler for Calendar App
Measure actual performance of each view
"""
import time
import sys
import os

# Prevent GUI from starting
os.environ['DISPLAY'] = ''

sys.path.insert(0, '.')

from datetime import date
from app.models.calendar_model import CalendarModel
from database.db_manager import DatabaseManager

def measure_view_performance():
    """Measure performance of different operations"""
    print("=" * 60)
    print("PERFORMANCE PROFILING")
    print("=" * 60)
    
    # Setup
    db = DatabaseManager()
    model = CalendarModel(db)
    
    # Test 1: Load events for month
    start = time.perf_counter()
    start_date = date(2025, 11, 1)
    end_date = date(2025, 11, 30)
    events = model.get_events_for_date_range(start_date, end_date)
    end = time.perf_counter()
    print(f"✅ Load Month Events: {len(events)} events in {(end-start)*1000:.2f}ms")
    
    # Test 2: Load events for week
    start = time.perf_counter()
    start_date = date(2025, 11, 4)
    end_date = date(2025, 11, 10)
    events = model.get_events_for_date_range(start_date, end_date)
    end = time.perf_counter()
    print(f"✅ Load Week Events: {len(events)} events in {(end-start)*1000:.2f}ms")
    
    # Test 3: Load events for day
    start = time.perf_counter()
    events = model.get_events_for_date(start_date)
    end = time.perf_counter()
    print(f"✅ Load Day Events: {len(events)} events in {(end-start)*1000:.2f}ms")
    
    # Test 4: Load events for year (12 months)
    start = time.perf_counter()
    start_date = date(2025, 1, 1)
    end_date = date(2025, 12, 31)
    events = model.get_events_for_date_range(start_date, end_date)
    end = time.perf_counter()
    print(f"✅ Load Year Events (1 query): {len(events)} events in {(end-start)*1000:.2f}ms")
    
    # Test 5: Load schedule (30 days)
    start = time.perf_counter()
    from datetime import timedelta
    end_date = start_date + timedelta(days=30)
    events = model.get_events_for_date_range(start_date, end_date)
    end = time.perf_counter()
    print(f"✅ Load Schedule (30 days): {len(events)} events in {(end-start)*1000:.2f}ms")
    
    # Test 6: Database query performance
    start = time.perf_counter()
    db.get_all_events()
    end = time.perf_counter()
    print(f"✅ Get All Events: {(end-start)*1000:.2f}ms")
    
    print("=" * 60)
    print("PERFORMANCE ANALYSIS:")
    print("- If Month/Week/Day < 50ms: ✅ Good")
    print("- If 50-100ms: ⚠️ Acceptable")
    print("- If > 100ms: ❌ Needs optimization")
    print("=" * 60)

if __name__ == "__main__":
    measure_view_performance()
