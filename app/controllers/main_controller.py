"""
Main Controller
Coordinates between View (UI) and Model (Data/Business Logic)
"""
from datetime import datetime, date
from typing import Optional, List
import threading
from app.models import Event, CalendarModel
from database.db_manager import DatabaseManager
from app.animation_helper import AnimationHelper
from app.config import ANIMATIONS
from app.thread_pool_manager import get_thread_pool


class MainController:
    """
    Main application controller following MVC pattern
    Handles user interactions and coordinates between view and model
    """
    
    def __init__(self, view, db_path: str = "database/events.db"):
        """
        Initialize controller
        
        Args:
            view: MainWindow instance
            db_path: Path to SQLite database
        """
        self.view = view
        self.db = DatabaseManager(db_path)
        self.model = CalendarModel(self.db)
        
        # Performance optimization: Thread pool for async operations
        self.thread_pool = get_thread_pool()
        
        # Performance optimization: Debounce refresh
        self._refresh_timer = None
        self._refresh_pending = False
        
        # Bind event handlers
        self._bind_events()
        
        # Load initial data
        self._load_initial_data()
    
    def _bind_events(self):
        """Bind UI events to controller methods"""
        # This will be implemented when we add event handlers to the view
        pass
    
    def _load_initial_data(self):
        """OPTIMIZED: Load initial data with lazy view initialization"""
        # Navigate to today
        self.model.navigate_today()
        
        # PERFORMANCE: Only initialize Month view (default view)
        # Other views will be initialized on-demand when user switches to them
        if hasattr(self.view, 'initialize_month_view'):
            self.view.initialize_month_view(self)
        
        # Mark other views as not initialized yet
        self._view_initialized = {
            'month': True,
            'week': False,
            'day': False,
            'year': False,
            'schedule': False
        }
        
        # Load events for current view
        self.refresh_events()
    
    # ==================== Event Management ====================
    
    def handle_create_event(self, event_data: dict) -> bool:
        """
        Handle create event action
        
        Args:
            event_data: Dictionary with event fields
            
        Returns:
            bool: True if successful
        """
        try:
            # Create Event object
            event = Event()
            event.update_from_dict(event_data)
            
            # Save to database
            success = self.model.create_event(event)
            
            if success:
                # Refresh view
                self.refresh_events()
                self.show_notification("Đã tạo sự kiện thành công", "success")
            else:
                self.show_notification("Lỗi khi tạo sự kiện", "error")
            
            return success
        except Exception as e:
            print(f"Error in handle_create_event: {e}")
            self.show_notification(f"Lỗi: {str(e)}", "error")
            return False
    
    def handle_create_event_from_nlp(self, text: str) -> bool:
        """
        Handle create event from natural language input (MULTITHREADED)
        
        Args:
            text: Natural language event description
            
        Returns:
            bool: True if successful
        """
        try:
            # Import NLP pipeline
            from core_nlp.pipeline import NLPPipeline
            
            # Parse text in background thread (CPU-intensive)
            def parse_in_background():
                nlp = NLPPipeline()
                return nlp.parse_event(text)
            
            def on_success(parsed):
                if not parsed:
                    self.show_notification("Không thể hiểu câu lệnh", "error")
                    return
                # Create event from parsed data
                self.handle_create_event(parsed)
            
            def on_error(error):
                print(f"Error in NLP parsing: {error}")
                self.show_notification(f"Lỗi NLP: {str(error)}", "error")
            
            # Submit to thread pool
            self.thread_pool.submit_compute_task(
                task_id=f"nlp_parse_{hash(text)}",
                func=parse_in_background,
                callback=on_success,
                error_callback=on_error
            )
            
            return True
        except Exception as e:
            print(f"Error in handle_create_event_from_nlp: {e}")
            self.show_notification(f"Lỗi: {str(e)}", "error")
            return False
    
    def handle_edit_event(self, event_id: int, updated_data: dict) -> bool:
        """
        Handle edit event action
        
        Args:
            event_id: ID of event to edit
            updated_data: Dictionary with updated fields
            
        Returns:
            bool: True if successful
        """
        try:
            # Get existing event
            event = self.model.get_event_by_id(event_id)
            if not event:
                self.show_notification("Không tìm thấy sự kiện", "error")
                return False
            
            # Update fields
            event.update_from_dict(updated_data)
            
            # Save to database
            success = self.model.update_event(event)
            
            if success:
                self.refresh_events()
                self.show_notification("Đã cập nhật sự kiện", "success")
            else:
                self.show_notification("Lỗi khi cập nhật sự kiện", "error")
            
            return success
        except Exception as e:
            print(f"Error in handle_edit_event: {e}")
            self.show_notification(f"Lỗi: {str(e)}", "error")
            return False
    
    def handle_delete_event(self, event_id: int) -> bool:
        """
        Handle delete event action (called from delete confirm dialog)
        
        Args:
            event_id: ID of event to delete
            
        Returns:
            bool: True if successful
        """
        try:
            # Delete from database (confirmation already done in dialog)
            success = self.model.delete_event(event_id)
            
            if success:
                self.refresh_events()
                print(f"✅ Event {event_id} deleted successfully")
            else:
                print(f"❌ Failed to delete event {event_id}")
            
            return success
        except Exception as e:
            print(f"[ERROR] handle_delete_event: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def handle_event_clicked(self, event_id: int):
        """
        Handle event click action
        
        Args:
            event_id: ID of clicked event
        """
        try:
            # Get event details
            event = self.model.get_event_by_id(event_id)
            if not event:
                return
            
            # Show edit dialog
            self.show_edit_dialog(event_id)
        except Exception as e:
            print(f"Error in handle_event_clicked: {e}")
    
    # ==================== Dialog Methods ====================
    
    def show_create_dialog(self, initial_date=None):
        """
        Show create event dialog
        
        Args:
            initial_date: Pre-selected date for new event
        """
        try:
            from app.views.dialogs import EventDialog
            dialog = EventDialog(self.view, self, initial_date=initial_date)
            dialog.wait_window()
            print("✅ Create dialog closed")
        except Exception as e:
            print(f"Error showing create dialog: {e}")
            self.show_notification(f"Lỗi: {str(e)}", "error")
    
    def show_edit_dialog(self, event_id: int):
        """
        Show edit event dialog
        
        Args:
            event_id: ID of event to edit
        """
        try:
            event = self.model.get_event_by_id(event_id)
            if not event:
                self.show_notification("Không tìm thấy sự kiện", "error")
                return
            
            from app.views.dialogs import EventDialog
            dialog = EventDialog(self.view, self, event=event)
            dialog.wait_window()
            print("✅ Edit dialog closed")
        except Exception as e:
            print(f"Error showing edit dialog: {e}")
            self.show_notification(f"Lỗi: {str(e)}", "error")
    
    def show_delete_confirm_dialog(self, event_id: int):
        """
        Show delete confirmation dialog
        
        Args:
            event_id: ID of event to delete
        """
        try:
            event = self.model.get_event_by_id(event_id)
            if not event:
                self.show_notification("Không tìm thấy sự kiện", "error")
                return
            
            from app.views.dialogs import DeleteConfirmDialog
            
            def on_confirm():
                success = self.handle_delete_event(event_id)
                if success:
                    self.show_notification("Đã xóa sự kiện thành công", "success")
                else:
                    self.show_notification("Lỗi khi xóa sự kiện", "error")
            
            dialog = DeleteConfirmDialog(self.view, event.event_name, on_confirm)
            dialog.wait_window()
            print("✅ Delete confirm dialog closed")
        except Exception as e:
            print(f"Error showing delete dialog: {e}")
            self.show_notification(f"Lỗi: {str(e)}", "error")
    
    def handle_update_event(self, event_id: int, event_data: dict) -> bool:
        """
        Wrapper for handle_edit_event (for compatibility with EventDialog)
        
        Args:
            event_id: ID of event to update
            event_data: Updated event data
            
        Returns:
            bool: True if successful
        """
        return self.handle_edit_event(event_id, event_data)
    
    # ==================== Calendar Navigation ====================
    
    def handle_date_selected(self, selected_date: date):
        """
        Handle date selection in calendar (single click)
        
        Args:
            selected_date: Selected date
        """
        try:
            # Update model
            self.model.set_current_date(selected_date)
            
            # Refresh view
            self.refresh_events()
            self.update_calendar_title()
        except Exception as e:
            print(f"Error in handle_date_selected: {e}")
    
    def handle_day_cell_double_click(self, selected_date: date):
        """
        Handle day cell double-click - create event for that date
        
        Args:
            selected_date: Date to create event for
        """
        try:
            print(f"📅 Double-click on {selected_date.strftime('%d/%m/%Y')} - Opening create dialog")
            self.show_create_dialog(initial_date=selected_date)
        except Exception as e:
            print(f"Error in handle_day_cell_double_click: {e}")
    
    def search_events(self, keyword: str, callback=None):
        """
        Search events by keyword (MULTITHREADED)
        
        Args:
            keyword: Search keyword
            callback: Optional callback function(results) to call with results
            
        Returns:
            List of matching Event objects (if synchronous)
        """
        try:
            # If no callback, execute synchronously
            if callback is None:
                return self.model.search_events(keyword)
            
            # Execute search in background (I/O-bound database operation)
            def search_in_background():
                return self.model.search_events(keyword)
            
            def on_error(error):
                print(f"Error in search: {error}")
                callback([])
            
            # Submit to thread pool
            self.thread_pool.submit_io_task(
                task_id=f"search_{hash(keyword)}",
                func=search_in_background,
                callback=callback,
                error_callback=on_error
            )
            
            return []  # Results will be provided via callback
        except Exception as e:
            print(f"Error in search_events: {e}")
            return []
    
    def show_search_dialog(self):
        """Show search dialog"""
        try:
            from app.views.dialogs import SearchDialog
            dialog = SearchDialog(self.view, self)
            dialog.wait_window()
            print("✅ Search dialog closed")
        except Exception as e:
            print(f"Error showing search dialog: {e}")
            self.show_notification(f"Lỗi: {str(e)}", "error")
    
    def show_settings_dialog(self):
        """Show settings dialog"""
        try:
            from app.views.dialogs import SettingsDialog
            dialog = SettingsDialog(self.view, self)
            dialog.wait_window()
            print("✅ Settings dialog closed")
        except Exception as e:
            print(f"Error showing settings dialog: {e}")
            self.show_notification(f"Lỗi: {str(e)}", "error")
    
    def show_statistics_dialog(self):
        """Show statistics dialog"""
        try:
            from app.views.dialogs import StatisticsDialog
            dialog = StatisticsDialog(self.view, self)
            dialog.wait_window()
            print("✅ Statistics dialog closed")
        except Exception as e:
            print(f"Error showing statistics dialog: {e}")
            self.show_notification(f"Lỗi: {str(e)}", "error")
    
    def handle_view_changed(self, view_type: str):
        """
        Handle calendar view type change
        
        Args:
            view_type: New view type (day, week, month, year, schedule)
        """
        try:
            # Update model
            self.model.set_view_type(view_type)
            
            # Refresh view
            self.refresh_events()
            self.update_calendar_title()
        except Exception as e:
            print(f"Error in handle_view_changed: {e}")
    
    def handle_navigate_previous(self):
        """OPTIMIZED: Instant navigation (no animation lag)"""
        try:
            # Navigate immediately for instant feel
            self.model.navigate_previous()
            
            # Refresh immediately (no delay for responsiveness)
            self._complete_navigation_instant()
        except Exception as e:
            print(f"Error in handle_navigate_previous: {e}")
    
    def handle_navigate_next(self):
        """OPTIMIZED: Instant navigation (no animation lag)"""
        try:
            # Navigate immediately for instant feel
            self.model.navigate_next()
            
            # Refresh immediately (no delay for responsiveness)
            self._complete_navigation_instant()
        except Exception as e:
            print(f"Error in handle_navigate_next: {e}")
    
    def handle_navigate_today(self):
        """OPTIMIZED: Instant navigation (no animation lag)"""
        try:
            # Navigate immediately for instant feel
            self.model.navigate_today()
            
            # Refresh immediately (no delay for responsiveness)
            self._complete_navigation_instant()
        except Exception as e:
            print(f"Error in handle_navigate_today: {e}")
    
    def _complete_navigation_instant(self):
        """Complete navigation without animation for instant feel"""
        try:
            # Refresh views (already optimized with debouncing)
            self.refresh_events(debounce_ms=0)
            
            # Update title
            self.update_calendar_title()
        except Exception as e:
            print(f"Error completing navigation: {e}")
    
    def _get_current_view_widget(self):
        """Get the current active view widget for animation"""
        try:
            if hasattr(self.view, 'month_view') and self.view.month_view and self.view.month_view.winfo_exists():
                return self.view.month_view
            elif hasattr(self.view, 'week_view') and self.view.week_view and self.view.week_view.winfo_exists():
                return self.view.week_view
            elif hasattr(self.view, 'day_view') and self.view.day_view and self.view.day_view.winfo_exists():
                return self.view.day_view
            elif hasattr(self.view, 'year_view') and self.view.year_view and self.view.year_view.winfo_exists():
                return self.view.year_view
            elif hasattr(self.view, 'schedule_view') and self.view.schedule_view and self.view.schedule_view.winfo_exists():
                return self.view.schedule_view
        except Exception:
            pass
        return None
    
    def _complete_navigation(self, direction: str):
        """Complete navigation after fade out animation"""
        try:
            # Navigate based on direction
            if direction == 'previous':
                self.model.navigate_previous()
            elif direction == 'next':
                self.model.navigate_next()
            elif direction == 'today':
                self.model.navigate_today()
            
            # Refresh and update
            self.refresh_events(debounce_ms=0)
            self.update_calendar_title()
            
            # Fade in new view
            current_widget = self._get_current_view_widget()
            if current_widget:
                AnimationHelper.fade_in(
                    current_widget,
                    duration_ms=ANIMATIONS['fade_duration'] // 2
                )
        except Exception as e:
            print(f"Error completing navigation: {e}")
    
    def handle_theme_change(self):
        """Handle theme change - refresh all views with new colors"""
        try:
            # Force immediate refresh to apply new colors
            self.refresh_events(debounce_ms=0)
            
            # Update calendar title with new colors
            self.update_calendar_title()
            
            print("🎨 Theme applied to all views")
        except Exception as e:
            print(f"Error in handle_theme_change: {e}")
    
    # ==================== Search & Filter ====================
    
    def handle_search(self, query: str):
        """
        Handle search query
        
        Args:
            query: Search query string
        """
        try:
            self.model.set_search_query(query)
            self.refresh_events()
        except Exception as e:
            print(f"Error in handle_search: {e}")
    
    def handle_filter_category(self, category: Optional[str]):
        """
        Handle category filter
        
        Args:
            category: Category to filter by (None = show all)
        """
        try:
            self.model.set_category_filter(category)
            self.refresh_events()
        except Exception as e:
            print(f"Error in handle_filter_category: {e}")
    
    def handle_clear_filters(self):
        """Handle clear all filters"""
        try:
            self.model.clear_filters()
            self.refresh_events()
        except Exception as e:
            print(f"Error in handle_clear_filters: {e}")
    
    # ==================== View Updates ====================
    
    def refresh_events(self, debounce_ms: int = 100):
        """
        Refresh events display in view (OPTIMIZED: with debouncing)
        
        Args:
            debounce_ms: Milliseconds to wait before refreshing (default 100ms)
        """
        # Cancel previous timer if exists
        if self._refresh_timer is not None:
            self._refresh_timer.cancel()
        
        # Mark refresh as pending
        self._refresh_pending = True
        
        # Schedule refresh after debounce period
        self._refresh_timer = threading.Timer(
            debounce_ms / 1000.0,
            self._do_refresh
        )
        self._refresh_timer.start()
    
    def _do_refresh(self):
        """OPTIMIZED: Perform refresh in main thread (avoid blocking)"""
        try:
            if not self._refresh_pending:
                return
            
            self._refresh_pending = False
            
            # Check if view still exists
            if not hasattr(self, 'view') or not self.view.winfo_exists():
                return
            
            # OPTIMIZATION: Get events in background, update UI in main thread
            # This prevents blocking the UI thread
            events = self.model.get_events_for_current_view()
            
            # Schedule UI update in main thread with after_idle for smooth update
            if hasattr(self.view, 'after_idle'):
                self.view.after_idle(lambda: self._update_ui_with_events(events))
            else:
                # Fallback to immediate update
                self._update_ui_with_events(events)
        except Exception as e:
            # Silently ignore errors during shutdown/widget destruction
            if "invalid command name" not in str(e):
                print(f"Error in refresh_events: {e}")
    
    def _update_ui_with_events(self, events):
        """Update UI with events in main thread"""
        try:
            # Update calendar title
            self.update_calendar_title()
            
            # Update view
            if hasattr(self.view, 'update_events'):
                self.view.update_events(events)
        except Exception as e:
            # Silently ignore widget destruction errors
            if "invalid command name" not in str(e):
                print(f"Error updating UI: {e}")
    
    def update_calendar_title(self):
        """Update calendar title with current period"""
        try:
            period_text = self.model.get_current_period_text()
            
            # Update view (to be implemented in view)
            if hasattr(self.view, 'update_period_title'):
                self.view.update_period_title(period_text)
        except Exception as e:
            print(f"Error in update_calendar_title: {e}")
    
    def show_event_details(self, event: Event):
        """
        Show event details dialog
        
        Args:
            event: Event to show
        """
        try:
            # To be implemented in view
            if hasattr(self.view, 'show_event_details_dialog'):
                self.view.show_event_details_dialog(event)
        except Exception as e:
            print(f"Error in show_event_details: {e}")
    
    def show_notification(self, message: str, type: str = "info"):
        """
        Show notification message
        
        Args:
            message: Message text
            type: Notification type (success, error, warning, info)
        """
        try:
            # To be implemented in view
            if hasattr(self.view, 'show_notification'):
                self.view.show_notification(message, type)
            else:
                # Fallback to print
                print(f"[{type.upper()}] {message}")
        except Exception as e:
            print(f"Error in show_notification: {e}")
    
    def show_confirmation(self, title: str, message: str) -> bool:
        """
        Show confirmation dialog
        
        Args:
            title: Dialog title
            message: Confirmation message
            
        Returns:
            bool: True if confirmed, False otherwise
        """
        try:
            # To be implemented in view
            if hasattr(self.view, 'show_confirmation_dialog'):
                return self.view.show_confirmation_dialog(title, message)
            else:
                # Fallback to console
                response = input(f"{title}: {message} (y/n): ")
                return response.lower() in ['y', 'yes']
        except Exception as e:
            print(f"Error in show_confirmation: {e}")
            return False
    
    # ==================== Statistics & Reports ====================
    
    def get_upcoming_events(self, days: int = 7) -> List[Event]:
        """
        Get upcoming events
        
        Args:
            days: Number of days to look ahead
            
        Returns:
            List of upcoming events
        """
        return self.model.get_upcoming_events(days)
    
    def get_event_statistics(self) -> dict:
        """
        Get event statistics
        
        Returns:
            Dictionary with statistics
        """
        try:
            all_events = self.model.get_all_events()
            upcoming = self.model.get_upcoming_events(7)
            overdue = self.model.get_overdue_events()
            
            # Group by category
            by_category = self.model.group_events_by_category(all_events)
            
            return {
                'total': len(all_events),
                'upcoming_week': len(upcoming),
                'overdue': len(overdue),
                'by_category': {k: len(v) for k, v in by_category.items()}
            }
        except Exception as e:
            print(f"Error in get_event_statistics: {e}")
            return {}
    
    # ==================== Import/Export ====================
    
    def handle_export_events(self, format: str, file_path: str) -> bool:
        """
        Handle export events (MULTITHREADED)
        
        Args:
            format: Export format (json, ics)
            file_path: Output file path
            
        Returns:
            bool: True if task submitted successfully
        """
        try:
            from services.export_service import export_to_json, export_to_ics
            
            # Export in background thread (I/O-bound operation)
            def export_in_background():
                if format == 'json':
                    export_to_json(self.db, file_path)
                    return True
                elif format == 'ics':
                    export_to_ics(self.db, file_path)
                    return True
                else:
                    return False
            
            def on_success(result):
                if result:
                    self.show_notification(f"✅ Đã xuất dữ liệu ra {file_path}", "success")
                else:
                    self.show_notification("❌ Định dạng không hợp lệ", "error")
            
            def on_error(error):
                print(f"Error in export: {error}")
                self.show_notification(f"❌ Lỗi: {str(error)}", "error")
            
            # Show progress notification
            self.show_notification("⏳ Đang xuất dữ liệu...", "info")
            
            # Submit to thread pool
            self.thread_pool.submit_io_task(
                task_id=f"export_{format}_{hash(file_path)}",
                func=export_in_background,
                callback=on_success,
                error_callback=on_error
            )
            
            return True
        except Exception as e:
            print(f"Error in handle_export_events: {e}")
            self.show_notification(f"❌ Lỗi: {str(e)}", "error")
            return False
    
    def handle_import_events(self, format: str, file_path: str) -> bool:
        """
        Handle import events (MULTITHREADED)
        
        Args:
            format: Import format (json, ics)
            file_path: Input file path
            
        Returns:
            bool: True if task submitted successfully
        """
        try:
            from services.import_service import import_from_json, import_from_ics
            
            # Import in background thread (I/O-bound operation)
            def import_in_background():
                if format == 'json':
                    return import_from_json(self.db, file_path, nlp_pipeline=None)
                elif format == 'ics':
                    return import_from_ics(self.db, file_path)
                else:
                    return 0
            
            def on_success(count):
                if count > 0:
                    self.refresh_events()
                    self.show_notification(f"✅ Đã nhập {count} sự kiện từ {file_path}", "success")
                else:
                    self.show_notification("⚠️ Không tìm thấy sự kiện hợp lệ", "warning")
            
            def on_error(error):
                print(f"Error in import: {error}")
                self.show_notification(f"❌ Lỗi: {str(error)}", "error")
            
            # Show progress notification
            self.show_notification("⏳ Đang nhập dữ liệu...", "info")
            
            # Submit to thread pool
            self.thread_pool.submit_io_task(
                task_id=f"import_{format}_{hash(file_path)}",
                func=import_in_background,
                callback=on_success,
                error_callback=on_error
            )
            
            return True
        except Exception as e:
            print(f"Error in handle_import_events: {e}")
            self.show_notification(f"❌ Lỗi: {str(e)}", "error")
            return False
    
    # ==================== App Lifecycle ====================
    
    def on_app_close(self):
        """Handle app closing (CLEANUP THREADS)"""
        try:
            # Shutdown thread pool gracefully
            print("🛑 Shutting down thread pool...")
            from app.thread_pool_manager import shutdown_thread_pool
            shutdown_thread_pool(wait=True)
            
            # DatabaseManager uses context managers, no explicit close needed
            print("Application closed successfully")
        except Exception as e:
            print(f"Error in on_app_close: {e}")
