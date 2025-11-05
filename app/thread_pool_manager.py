"""
Thread Pool Manager
Manages multithreading for performance optimization
"""
import threading
import queue
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Callable, Any, Optional, Dict
import time


class ThreadPoolManager:
    """
    Singleton thread pool manager for handling async operations
    Optimizes performance by running heavy tasks in background threads
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Ensure singleton pattern"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize thread pool with optimal worker count"""
        if hasattr(self, '_initialized'):
            return
        
        # Optimal thread count: 2x CPU cores for I/O-bound tasks
        import os
        cpu_count = os.cpu_count() or 4
        self.max_workers = min(cpu_count * 2, 16)  # Cap at 16 threads
        
        # Thread pools for different task types
        self.io_pool = ThreadPoolExecutor(
            max_workers=self.max_workers,
            thread_name_prefix="IO-Worker"
        )
        
        self.compute_pool = ThreadPoolExecutor(
            max_workers=cpu_count,
            thread_name_prefix="Compute-Worker"
        )
        
        # Task tracking
        self.active_tasks: Dict[str, Future] = {}
        self.task_lock = threading.Lock()
        
        # Performance metrics
        self.metrics = {
            'total_tasks': 0,
            'completed_tasks': 0,
            'failed_tasks': 0,
            'avg_execution_time': 0.0
        }
        self.metrics_lock = threading.Lock()
        
        self._initialized = True
        print(f"🚀 ThreadPool initialized: {self.max_workers} I/O workers, {cpu_count} compute workers")
    
    def submit_io_task(
        self,
        task_id: str,
        func: Callable,
        *args,
        callback: Optional[Callable[[Any], None]] = None,
        error_callback: Optional[Callable[[Exception], None]] = None,
        **kwargs
    ) -> Future:
        """
        Submit I/O-bound task (database, file operations, network)
        
        Args:
            task_id: Unique task identifier
            func: Function to execute
            *args: Positional arguments for func
            callback: Function to call with result on success
            error_callback: Function to call with exception on error
            **kwargs: Keyword arguments for func
            
        Returns:
            Future object for tracking task
        """
        return self._submit_task(
            self.io_pool,
            task_id,
            func,
            *args,
            callback=callback,
            error_callback=error_callback,
            **kwargs
        )
    
    def submit_compute_task(
        self,
        task_id: str,
        func: Callable,
        *args,
        callback: Optional[Callable[[Any], None]] = None,
        error_callback: Optional[Callable[[Exception], None]] = None,
        **kwargs
    ) -> Future:
        """
        Submit CPU-bound task (NLP parsing, data processing)
        
        Args:
            task_id: Unique task identifier
            func: Function to execute
            *args: Positional arguments for func
            callback: Function to call with result on success
            error_callback: Function to call with exception on error
            **kwargs: Keyword arguments for func
            
        Returns:
            Future object for tracking task
        """
        return self._submit_task(
            self.compute_pool,
            task_id,
            func,
            *args,
            callback=callback,
            error_callback=error_callback,
            **kwargs
        )
    
    def _submit_task(
        self,
        pool: ThreadPoolExecutor,
        task_id: str,
        func: Callable,
        *args,
        callback: Optional[Callable] = None,
        error_callback: Optional[Callable] = None,
        **kwargs
    ) -> Future:
        """Internal method to submit task to pool"""
        start_time = time.time()
        
        # Cancel existing task with same ID if exists
        with self.task_lock:
            if task_id in self.active_tasks:
                self.active_tasks[task_id].cancel()
        
        # Wrapper function to track metrics and call callbacks
        def wrapped_func():
            try:
                # Execute actual function
                result = func(*args, **kwargs)
                
                # Update metrics
                execution_time = time.time() - start_time
                self._update_metrics(success=True, execution_time=execution_time)
                
                # Call success callback if provided
                if callback:
                    callback(result)
                
                return result
            except Exception as e:
                # Update metrics
                execution_time = time.time() - start_time
                self._update_metrics(success=False, execution_time=execution_time)
                
                # Call error callback if provided
                if error_callback:
                    error_callback(e)
                else:
                    print(f"❌ Task {task_id} failed: {e}")
                
                raise
            finally:
                # Remove from active tasks
                with self.task_lock:
                    self.active_tasks.pop(task_id, None)
        
        # Submit to thread pool
        future = pool.submit(wrapped_func)
        
        # Track active task
        with self.task_lock:
            self.active_tasks[task_id] = future
        
        return future
    
    def cancel_task(self, task_id: str) -> bool:
        """
        Cancel a running task
        
        Args:
            task_id: Task identifier to cancel
            
        Returns:
            True if task was cancelled, False if not found or already done
        """
        with self.task_lock:
            if task_id in self.active_tasks:
                return self.active_tasks[task_id].cancel()
        return False
    
    def wait_for_task(self, task_id: str, timeout: Optional[float] = None) -> Any:
        """
        Wait for task to complete and return result
        
        Args:
            task_id: Task identifier
            timeout: Maximum seconds to wait (None = wait forever)
            
        Returns:
            Task result
            
        Raises:
            TimeoutError: If timeout exceeded
            Exception: If task raised an exception
        """
        with self.task_lock:
            if task_id not in self.active_tasks:
                raise ValueError(f"Task {task_id} not found")
            future = self.active_tasks[task_id]
        
        return future.result(timeout=timeout)
    
    def get_active_tasks(self) -> int:
        """Get number of currently running tasks"""
        with self.task_lock:
            return len(self.active_tasks)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        with self.metrics_lock:
            return self.metrics.copy()
    
    def _update_metrics(self, success: bool, execution_time: float):
        """Update performance metrics"""
        with self.metrics_lock:
            self.metrics['total_tasks'] += 1
            if success:
                self.metrics['completed_tasks'] += 1
            else:
                self.metrics['failed_tasks'] += 1
            
            # Update average execution time (rolling average)
            total = self.metrics['total_tasks']
            old_avg = self.metrics['avg_execution_time']
            self.metrics['avg_execution_time'] = (old_avg * (total - 1) + execution_time) / total
    
    def shutdown(self, wait: bool = True):
        """
        Shutdown thread pools
        
        Args:
            wait: If True, wait for all tasks to complete
        """
        print(f"🛑 Shutting down thread pools (wait={wait})...")
        self.io_pool.shutdown(wait=wait)
        self.compute_pool.shutdown(wait=wait)
        
        # Print final metrics
        metrics = self.get_metrics()
        print(f"📊 Final metrics:")
        print(f"   - Total tasks: {metrics['total_tasks']}")
        print(f"   - Completed: {metrics['completed_tasks']}")
        print(f"   - Failed: {metrics['failed_tasks']}")
        print(f"   - Avg execution time: {metrics['avg_execution_time']:.3f}s")


# Global singleton instance
_thread_pool = None


def get_thread_pool() -> ThreadPoolManager:
    """Get or create global thread pool instance"""
    global _thread_pool
    if _thread_pool is None:
        _thread_pool = ThreadPoolManager()
    return _thread_pool


def shutdown_thread_pool(wait: bool = True):
    """Shutdown global thread pool"""
    global _thread_pool
    if _thread_pool is not None:
        _thread_pool.shutdown(wait=wait)
        _thread_pool = None
