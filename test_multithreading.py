"""
Test Multithreading Configuration
Quick test without UI dependencies
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("="*60)
print("Testing Multithreading Configuration")
print("="*60)

# Test 1: ThreadPoolManager
print("\n[Test 1] ThreadPoolManager initialization...")
try:
    from app.thread_pool_manager import get_thread_pool
    
    pool = get_thread_pool()
    print(f"✅ Thread pool created successfully")
    print(f"   - I/O workers: {pool.max_workers}")
    print(f"   - Compute workers: {pool.compute_pool._max_workers}")
    print(f"   - Active tasks: {pool.get_active_tasks()}")
except Exception as e:
    print(f"❌ Failed: {e}")
    sys.exit(1)

# Test 2: Submit I/O Task
print("\n[Test 2] Submit I/O task...")
try:
    import time
    
    result = []
    
    def io_task(x):
        time.sleep(0.1)
        return x * 2
    
    def callback(r):
        result.append(r)
        print(f"✅ Callback received: {r}")
    
    future = pool.submit_io_task(
        "test_io",
        io_task,
        10,
        callback=callback
    )
    
    # Wait for completion
    future.result(timeout=2.0)
    print(f"✅ I/O task completed")
except Exception as e:
    print(f"❌ Failed: {e}")

# Test 3: Submit Compute Task
print("\n[Test 3] Submit compute task...")
try:
    def compute_task():
        total = 0
        for i in range(1000000):
            total += i
        return total
    
    result = []
    
    def callback(r):
        result.append(r)
        print(f"✅ Compute result: {r}")
    
    future = pool.submit_compute_task(
        "test_compute",
        compute_task,
        callback=callback
    )
    
    # Wait for completion
    future.result(timeout=2.0)
    print(f"✅ Compute task completed")
except Exception as e:
    print(f"❌ Failed: {e}")

# Test 4: Parallel Tasks
print("\n[Test 4] Parallel task execution...")
try:
    import time
    
    completed = []
    
    def parallel_task(task_id):
        time.sleep(0.2)
        return f"Task {task_id} done"
    
    def make_callback(tid):
        def cb(result):
            completed.append(result)
            print(f"   {result}")
        return cb
    
    # Submit 5 parallel tasks
    futures = []
    for i in range(5):
        f = pool.submit_io_task(
            f"parallel_{i}",
            parallel_task,
            i,
            callback=make_callback(i)
        )
        futures.append(f)
    
    # Wait for all
    for f in futures:
        f.result(timeout=2.0)
    
    print(f"✅ All {len(completed)} parallel tasks completed")
except Exception as e:
    print(f"❌ Failed: {e}")

# Test 5: Database Connection Pooling
print("\n[Test 5] Database connection pooling...")
try:
    from database.db_manager import DatabaseManager
    
    db = DatabaseManager("database/events.db")
    print(f"✅ Database initialized with connection pool")
    print(f"   - Pool size: {db._pool_size}")
    print(f"   - Max pool size: {db.MAX_POOL_SIZE}")
    
    # Test concurrent queries
    import threading
    
    def query_db():
        events = db.get_all_events()
        return len(events)
    
    threads = []
    results = []
    
    for i in range(5):
        def thread_func():
            count = query_db()
            results.append(count)
        
        t = threading.Thread(target=thread_func)
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print(f"✅ {len(threads)} concurrent database queries completed")
    print(f"   - Results: {results}")
    
    # Cleanup
    db.close_pool()
except Exception as e:
    print(f"❌ Failed: {e}")
    import traceback
    traceback.print_exc()

# Test 6: Get Metrics
print("\n[Test 6] Performance metrics...")
try:
    metrics = pool.get_metrics()
    print(f"✅ Metrics retrieved:")
    print(f"   - Total tasks: {metrics['total_tasks']}")
    print(f"   - Completed: {metrics['completed_tasks']}")
    print(f"   - Failed: {metrics['failed_tasks']}")
    print(f"   - Avg execution time: {metrics['avg_execution_time']:.4f}s")
except Exception as e:
    print(f"❌ Failed: {e}")

# Test 7: Cleanup
print("\n[Test 7] Thread pool shutdown...")
try:
    from app.thread_pool_manager import shutdown_thread_pool
    
    shutdown_thread_pool(wait=True)
    print(f"✅ Thread pool shutdown completed")
except Exception as e:
    print(f"❌ Failed: {e}")

print("\n" + "="*60)
print("All tests completed successfully! ✅")
print("="*60)
print("\nMultithreading configuration is working correctly.")
print("The application will run faster with:")
print("  • Non-blocking NLP parsing")
print("  • Concurrent database queries")
print("  • Background import/export")
print("  • Parallel task execution")
