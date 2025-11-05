"""
Main Window Component - Google Calendar Style
Implements the main application window with top bar, sidebar, and calendar area
"""
import customtkinter as ctk
from datetime import date, datetime, timedelta
from app.config import COLORS, FONTS, SPACING, LAYOUT, APP_INFO, VIEW_TYPES, ANIMATIONS
from app.views.calendar_views import MonthView, WeekView, DayView, YearView, ScheduleView
from app.theme_manager import theme_manager
from app.animation_helper import AnimationHelper


class MainWindow(ctk.CTk):
    """Main application window with Google Calendar UI"""
    
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title(f"{APP_INFO['name']} - v{APP_INFO['version']}")
        self.geometry(f"{LAYOUT['window_default_width']}x{LAYOUT['window_default_height']}")
        self.minsize(LAYOUT['window_min_width'], LAYOUT['window_min_height'])
        
        # Set appearance
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Current state
        self.current_view = "month"
        self.current_date = date.today()
        self.controller = None  # Will be set by controller
        
        # Setup layout
        self._setup_grid()
        self._create_top_bar()
        self._create_sidebar()
        self._create_main_area()
    
    def _setup_grid(self):
        """Configure grid layout"""
        # Configure rows
        self.grid_rowconfigure(0, weight=0)  # Top bar (fixed)
        self.grid_rowconfigure(1, weight=1)  # Main content (expandable)
        
        # Configure columns
        self.grid_columnconfigure(0, weight=0)  # Sidebar (fixed)
        self.grid_columnconfigure(1, weight=1)  # Main area (expandable)
    
    def _create_top_bar(self):
        """Create top navigation bar"""
        top_bar = ctk.CTkFrame(
            self,
            height=LAYOUT['topbar_height'],
            fg_color=COLORS['bg_white'],
            corner_radius=0
        )
        top_bar.grid(row=0, column=0, columnspan=2, sticky="ew")
        top_bar.grid_propagate(False)
        
        # Left section - Title
        left_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        left_frame.pack(side="left", fill="y", padx=SPACING['md'])
        
        # Hamburger menu icon (☰)
        menu_btn = ctk.CTkButton(
            left_frame,
            text="☰",
            width=40,
            height=40,
            fg_color="transparent",
            text_color=COLORS['text_primary'],
            hover_color=COLORS['bg_gray_hover'],
            font=FONTS['title'],
            corner_radius=20,
            command=self._toggle_sidebar
        )
        menu_btn.pack(side="left", padx=(0, SPACING['sm']))
        
        # App title
        title_label = ctk.CTkLabel(
            left_frame,
            text=APP_INFO['name'],
            font=FONTS['title'],
            text_color=COLORS['text_primary']
        )
        title_label.pack(side="left", padx=SPACING['sm'])
        
        # Center section - Navigation
        center_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        center_frame.pack(side="left", fill="y", padx=SPACING['xl'])
        
        # Today button
        today_btn = ctk.CTkButton(
            center_frame,
            text="Hôm nay",
            width=90,
            height=36,
            fg_color="transparent",
            text_color=COLORS['text_primary'],
            border_width=1,
            border_color=COLORS['border_light'],
            hover_color=COLORS['bg_gray_hover'],
            font=FONTS['body_bold'],
            corner_radius=4,
            command=self._go_to_today
        )
        today_btn.pack(side="left", padx=SPACING['xs'])
        
        # Previous button
        prev_btn = ctk.CTkButton(
            center_frame,
            text="◀",
            width=36,
            height=36,
            fg_color="transparent",
            text_color=COLORS['text_primary'],
            hover_color=COLORS['bg_gray_hover'],
            font=FONTS['heading'],
            corner_radius=18,
            command=self._go_previous
        )
        prev_btn.pack(side="left", padx=SPACING['xs'])
        
        # Next button
        next_btn = ctk.CTkButton(
            center_frame,
            text="▶",
            width=36,
            height=36,
            fg_color="transparent",
            text_color=COLORS['text_primary'],
            hover_color=COLORS['bg_gray_hover'],
            font=FONTS['heading'],
            corner_radius=18,
            command=self._go_next
        )
        next_btn.pack(side="left", padx=SPACING['xs'])
        
        # Current date/period label
        self.period_label = ctk.CTkLabel(
            center_frame,
            text=self._get_period_text(),
            font=FONTS['heading'],
            text_color=COLORS['text_primary']
        )
        self.period_label.pack(side="left", padx=SPACING['md'])
        
        # Right section - Actions
        right_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        right_frame.pack(side="right", fill="y", padx=SPACING['md'])
        
        # Search button
        search_btn = ctk.CTkButton(
            right_frame,
            text="🔍",
            width=40,
            height=40,
            fg_color="transparent",
            text_color=COLORS['text_primary'],
            hover_color=COLORS['bg_gray_hover'],
            font=FONTS['heading'],
            corner_radius=20,
            command=self._show_search
        )
        search_btn.pack(side="left", padx=SPACING['xs'])
        
        # Statistics button
        stats_btn = ctk.CTkButton(
            right_frame,
            text="📊",
            width=40,
            height=40,
            fg_color="transparent",
            text_color=COLORS['text_primary'],
            hover_color=COLORS['bg_gray_hover'],
            font=FONTS['heading'],
            corner_radius=20,
            command=self._show_statistics
        )
        stats_btn.pack(side="left", padx=SPACING['xs'])
        
        # Dark mode toggle button
        self.theme_btn = ctk.CTkButton(
            right_frame,
            text="🌙",  # Moon for dark mode
            width=40,
            height=40,
            fg_color="transparent",
            text_color=COLORS['text_primary'],
            hover_color=COLORS['bg_gray_hover'],
            font=FONTS['heading'],
            corner_radius=20,
            command=self._toggle_theme
        )
        self.theme_btn.pack(side="left", padx=SPACING['xs'])
        
        # Settings button
        settings_btn = ctk.CTkButton(
            right_frame,
            text="⚙",
            width=40,
            height=40,
            fg_color="transparent",
            text_color=COLORS['text_primary'],
            hover_color=COLORS['bg_gray_hover'],
            font=FONTS['heading'],
            corner_radius=20,
            command=self._show_settings
        )
        settings_btn.pack(side="left", padx=SPACING['xs'])
    
    def _create_sidebar(self):
        """Create left sidebar"""
        self.sidebar = ctk.CTkFrame(
            self,
            width=LAYOUT['sidebar_width'],
            fg_color=COLORS['bg_gray'],
            corner_radius=0
        )
        self.sidebar.grid(row=1, column=0, sticky="nsw")
        self.sidebar.grid_propagate(False)
        self.sidebar_visible = True
        
        # Create button (prominent)
        create_btn = ctk.CTkButton(
            self.sidebar,
            text="+ Tạo mới",
            width=LAYOUT['sidebar_width'] - (SPACING['md'] * 2),
            height=LAYOUT['button_height'],
            fg_color=COLORS['primary_blue'],
            hover_color=COLORS['primary_blue_hover'],
            text_color=COLORS['text_light'],
            font=FONTS['button'],
            corner_radius=LAYOUT['button_corner_radius'],
            command=self._create_event
        )
        create_btn.pack(pady=SPACING['md'], padx=SPACING['md'])
        
        # Mini calendar (will be initialized by controller)
        self.mini_calendar = None  # Will be created after controller is set
        
        # My Calendars section
        calendars_label = ctk.CTkLabel(
            self.sidebar,
            text="Lịch của tôi",
            font=FONTS['subheading'],
            text_color=COLORS['text_primary'],
            anchor="w"
        )
        calendars_label.pack(pady=(SPACING['md'], SPACING['sm']), padx=SPACING['md'], fill="x")
        
        # Calendar checkboxes
        calendar_items = [
            ("✓ Công việc", COLORS['event_work']),
            ("✓ Sinh nhật", COLORS['event_health']),
            ("✓ Nhắc nhở", COLORS['event_study']),
        ]
        
        for text, color in calendar_items:
            checkbox = ctk.CTkCheckBox(
                self.sidebar,
                text=text,
                fg_color=color,
                hover_color=color,
                font=FONTS['body'],
                text_color=COLORS['text_primary']
            )
            checkbox.pack(pady=SPACING['xs'], padx=SPACING['md'], anchor="w")
            checkbox.select()  # Default checked
    
    def _create_main_area(self):
        """Create main calendar area"""
        main_area = ctk.CTkFrame(
            self,
            fg_color=COLORS['bg_white'],
            corner_radius=0
        )
        main_area.grid(row=1, column=1, sticky="nsew", padx=SPACING['md'], pady=SPACING['md'])
        
        # View switcher (always visible)
        view_frame = ctk.CTkFrame(
            main_area,
            fg_color=COLORS['bg_white'],
            height=50
        )
        view_frame.pack(pady=(0, SPACING['sm']), fill="x")
        view_frame.pack_propagate(False)
        
        self.view_switcher = ctk.CTkSegmentedButton(
            view_frame,
            values=list(VIEW_TYPES.values()),
            selected_color=COLORS['primary_blue'],
            selected_hover_color=COLORS['primary_blue_hover'],
            unselected_color=COLORS['bg_white'],
            unselected_hover_color=COLORS['bg_gray_hover'],
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary'],
            corner_radius=6,
            border_width=1,
            command=self._change_view
        )
        self.view_switcher.pack(pady=SPACING['sm'], padx=0, anchor='w')
        self.view_switcher.set(VIEW_TYPES['month'])
        
        # Calendar view area
        calendar_container = ctk.CTkFrame(
            main_area,
            fg_color=COLORS['bg_white'],
            corner_radius=LAYOUT['card_corner_radius'],
            border_width=1,
            border_color=COLORS['border_light']
        )
        calendar_container.pack(fill="both", expand=True)
        
        # Calendar views (will be set by controller)
        self.month_view = None  # Will be initialized with controller
        self.week_view = None  # Will be initialized with controller
        self.day_view = None  # Will be initialized with controller
        self.year_view = None  # Will be initialized with controller
        self.schedule_view = None  # Will be initialized with controller
        self.calendar_container = calendar_container
    
    def _get_period_text(self):
        """Get current period text based on view"""
        if self.current_view == "month":
            return f"Tháng {self.current_date.month}, {self.current_date.year}"
        elif self.current_view == "week":
            return f"Tuần {self.current_date.isocalendar()[1]}, {self.current_date.year}"
        elif self.current_view == "day":
            return self.current_date.strftime("%d/%m/%Y")
        return str(self.current_date.year)
    
    def _toggle_sidebar(self):
        """ULTRA OPTIMIZED: Instant toggle without blocking"""
        if self.sidebar_visible:
            # Use grid_remove() for instant hide (faster than grid_forget())
            self.sidebar.grid_remove()
            self.sidebar_visible = False
        else:
            # Show instantly
            self.sidebar.grid(row=1, column=0, sticky="nsw")
            self.sidebar_visible = True
        
        # NO update_idletasks() - it blocks UI and causes lag!
    
    def _go_to_today(self):
        """Navigate to today"""
        self.current_date = date.today()
        
        # Update appropriate view
        if self.current_view == 'month' and self.month_view:
            self.month_view.go_today()
            self.period_label.configure(text=self.month_view.get_current_period_text())
        elif self.current_view == 'week' and self.week_view:
            self.week_view.go_today()
            self.period_label.configure(text=self.week_view.get_current_period_text())
        elif self.current_view == 'day' and self.day_view:
            self.day_view.go_today()
            self.period_label.configure(text=self.day_view.get_current_period_text())
        elif self.current_view == 'year' and self.year_view:
            self.year_view.go_today()
            self.period_label.configure(text=self.year_view.get_current_period_text())
        elif self.current_view == 'schedule' and self.schedule_view:
            self.schedule_view.go_today()
            self.period_label.configure(text=self.schedule_view.get_current_period_text())
        
        print(f"✅ Navigated to today: {self.current_date}")
    
    def _go_previous(self):
        """Navigate to previous period"""
        if self.current_view == 'month' and self.month_view:
            self.month_view.go_previous_month()
            self.current_date = date(self.month_view.current_year, self.month_view.current_month, 1)
            self.period_label.configure(text=self.month_view.get_current_period_text())
        elif self.current_view == 'week' and self.week_view:
            self.week_view.go_previous_week()
            self.current_date = self.week_view.week_start
            self.period_label.configure(text=self.week_view.get_current_period_text())
        elif self.current_view == 'day' and self.day_view:
            self.day_view.go_previous_day()
            self.current_date = self.day_view.current_date
            self.period_label.configure(text=self.day_view.get_current_period_text())
        elif self.current_view == 'year' and self.year_view:
            self.year_view.go_previous_year()
            self.period_label.configure(text=self.year_view.get_current_period_text())
        # Schedule view doesn't have previous/next
        
        print("◀ Go to previous period")
    
    def _go_next(self):
        """Navigate to next period"""
        if self.current_view == 'month' and self.month_view:
            self.month_view.go_next_month()
            self.current_date = date(self.month_view.current_year, self.month_view.current_month, 1)
            self.period_label.configure(text=self.month_view.get_current_period_text())
        elif self.current_view == 'week' and self.week_view:
            self.week_view.go_next_week()
            self.current_date = self.week_view.week_start
            self.period_label.configure(text=self.week_view.get_current_period_text())
        elif self.current_view == 'day' and self.day_view:
            self.day_view.go_next_day()
            self.current_date = self.day_view.current_date
            self.period_label.configure(text=self.day_view.get_current_period_text())
        elif self.current_view == 'year' and self.year_view:
            self.year_view.go_next_year()
            self.period_label.configure(text=self.year_view.get_current_period_text())
        # Schedule view doesn't have previous/next
        
        print("▶ Go to next period")
    
    def _change_view(self, selected_view):
        """ULTRA OPTIMIZED: Instant view change with zero delay"""
        # Fast lookup without list comprehension
        view_key = None
        for k, v in VIEW_TYPES.items():
            if v == selected_view:
                view_key = k
                break
        
        if not view_key:
            return
        
        # INSTANT view switch - show_view is already optimized
        self.show_view(view_key)
        
        print(f"⚡ INSTANT: Changed to {selected_view} view")
    
    def _create_event(self):
        """Open create event dialog"""
        print("➕ Create new event")
        if self.controller:
            self.controller.show_create_dialog()
    
    def _show_search(self):
        """Show search dialog"""
        if self.controller:
            self.controller.show_search_dialog()
        else:
            print("⚠️ Controller not initialized")
    
    def _show_statistics(self):
        """Show statistics dialog"""
        if self.controller:
            self.controller.show_statistics_dialog()
        else:
            print("⚠️ Controller not initialized")
    
    def _show_settings(self):
        """Show settings dialog"""
        if self.controller:
            self.controller.show_settings_dialog()
        else:
            print("⚠️ Controller not initialized")
    
    def _toggle_theme(self):
        """Toggle between light and dark mode with animation"""
        # Toggle theme
        theme_manager.toggle_theme()
        
        # Update button icon
        if theme_manager.is_dark_mode:
            self.theme_btn.configure(text="☀️")  # Sun for light mode
        else:
            self.theme_btn.configure(text="🌙")  # Moon for dark mode
        
        # Apply theme to all widgets with fade animation
        self._apply_theme_animated()
    
    def _apply_theme_animated(self):
        """Apply theme colors to all widgets with smooth transition"""
        # Update main window
        self.configure(fg_color=COLORS['bg_white'])
        
        # Update all child widgets recursively
        self._update_widget_colors(self)
        
        # Notify controller to refresh views
        if self.controller:
            self.controller.handle_theme_change()
    
    def _update_widget_colors(self, widget):
        """Recursively update colors for widget and its children"""
        try:
            # Update widget colors based on type
            if isinstance(widget, ctk.CTkFrame):
                if widget.cget('fg_color') != 'transparent':
                    widget.configure(fg_color=COLORS['bg_white'])
            elif isinstance(widget, ctk.CTkLabel):
                widget.configure(text_color=COLORS['text_primary'])
            elif isinstance(widget, ctk.CTkButton):
                # Keep button-specific colors
                pass
            
            # Recursively update children
            for child in widget.winfo_children():
                self._update_widget_colors(child)
        except Exception as e:
            # Silently ignore errors during theme update
            pass
    
    # ==================== Controller Integration ====================
    
    def initialize_month_view(self, controller):
        """
        Initialize month view with controller
        Called by controller after setup
        
        Args:
            controller: MainController instance
        """
        # Store controller reference
        self.controller = controller
        
        # Create mini calendar in sidebar
        if not self.mini_calendar and hasattr(self, 'sidebar'):
            from app.views.components.mini_calendar import MiniCalendar
            self.mini_calendar = MiniCalendar(self.sidebar, controller)
            self.mini_calendar.pack(pady=SPACING['md'], padx=SPACING['md'], fill="x", after=self.sidebar.winfo_children()[0])
        
        if not hasattr(self, 'calendar_container'):
            print("⚠️ Calendar container not found")
            return
        
        # Create month view
        self.month_view = MonthView(self.calendar_container, controller)
        self.month_view.pack(fill='both', expand=True)
        
        # Initial calendar update
        self.month_view.update_calendar()
        
        # Update period label
        self.period_label.configure(text=self.month_view.get_current_period_text())
        
        print("✅ Month view initialized")
    
    def initialize_week_view(self, controller):
        """
        Initialize week view with controller
        Called by controller after setup
        
        Args:
            controller: MainController instance
        """
        if not hasattr(self, 'calendar_container'):
            print("⚠️ Calendar container not found")
            return
        
        # Create week view (initially hidden)
        self.week_view = WeekView(self.calendar_container, controller)
        self.week_view.pack_forget()
        
        # Initial update
        self.week_view.update_week()
        
        print("✅ Week view initialized")
    
    def initialize_day_view(self, controller):
        """
        Initialize day view with controller
        Called by controller after setup
        
        Args:
            controller: MainController instance
        """
        if not hasattr(self, 'calendar_container'):
            print("⚠️ Calendar container not found")
            return
        
        # Create day view (initially hidden)
        self.day_view = DayView(self.calendar_container, controller)
        self.day_view.pack_forget()
        
        # Initial update
        self.day_view.update_day()
        
        print("✅ Day view initialized")
    
    def initialize_year_view(self, controller):
        """Initialize year view with controller"""
        if not hasattr(self, 'calendar_container'):
            return
        
        self.year_view = YearView(self.calendar_container, controller)
        self.year_view.pack_forget()
        self.year_view.update_year()
        print("✅ Year view initialized")
    
    def initialize_schedule_view(self, controller):
        """Initialize schedule/agenda view with controller"""
        if not hasattr(self, 'calendar_container'):
            return
        
        self.schedule_view = ScheduleView(self.calendar_container, controller)
        self.schedule_view.pack_forget()
        self.schedule_view.update_schedule()
        print("✅ Schedule view initialized")
    
    def show_view(self, view_type: str):
        """
        ULTRA OPTIMIZED: Instant view switching with LAZY INITIALIZATION
        Only create views when first accessed - massive startup improvement
        
        Args:
            view_type: 'month', 'week', 'day', 'year', or 'schedule'
        """
        # LAZY INITIALIZATION: Initialize view on-demand if not yet created
        if self.controller and hasattr(self.controller, '_view_initialized'):
            if not self.controller._view_initialized.get(view_type, False):
                init_methods = {
                    'week': 'initialize_week_view',
                    'day': 'initialize_day_view',
                    'year': 'initialize_year_view',
                    'schedule': 'initialize_schedule_view'
                }
                method_name = init_methods.get(view_type)
                if method_name and hasattr(self, method_name):
                    getattr(self, method_name)(self.controller)
                    self.controller._view_initialized[view_type] = True
        
        # Map view types to view objects
        views = {
            'month': self.month_view,
            'week': self.week_view,
            'day': self.day_view,
            'year': self.year_view,
            'schedule': self.schedule_view
        }
        
        # Get current and new view
        current_view = views.get(self.current_view)
        new_view = views.get(view_type)
        
        if not new_view:
            return
        
        # OPTIMIZATION 1: Skip if already showing this view
        if view_type == self.current_view and new_view.winfo_ismapped():
            return
        
        # OPTIMIZATION 2: Hide current view instantly (no animation)
        if current_view and current_view.winfo_exists():
            current_view.pack_forget()
        
        # OPTIMIZATION 3: Show new view immediately (instant feedback)
        new_view.pack(fill='both', expand=True)
        
        # OPTIMIZATION 4: Update title immediately
        self.update_period_title(new_view.get_current_period_text())
        
        # OPTIMIZATION 5: NO DELAY - refresh immediately in background
        # Using after(0) instead of after(1) for instant execution
        self.after(0, lambda: self._instant_refresh(new_view))
        
        # Update current view state
        self.current_view = view_type
    
    def _instant_refresh(self, view):
        """
        Instant refresh without delay - view is already visible
        """
        try:
            if view and view.winfo_exists():
                view.refresh()
        except Exception as e:
            print(f"Instant refresh error: {e}")
    
    def update_period_title(self, text: str):
        """Update period title in top bar"""
        if hasattr(self, 'period_label'):
            self.period_label.configure(text=text)
    
    def update_events(self, events: list):
        """
        OPTIMIZED: Update calendar views with cache invalidation
        Called by controller when events change
        
        Args:
            events: List of Event objects
        """
        # Clear cache in all views since events changed
        if self.month_view and hasattr(self.month_view, 'clear_cache'):
            self.month_view.clear_cache()
        if self.week_view and hasattr(self.week_view, 'clear_cache'):
            self.week_view.clear_cache()
        if self.day_view and hasattr(self.day_view, 'clear_cache'):
            self.day_view.clear_cache()
        
        # Refresh views
        if self.month_view:
            self.month_view.refresh()
        if self.week_view:
            self.week_view.refresh()
        if self.day_view:
            self.day_view.refresh()
        if self.year_view:
            self.year_view.refresh()
        if self.schedule_view:
            self.schedule_view.refresh()
        print(f"✅ Calendar updated with {len(events)} events (cache cleared)")


def main():
    """Run the application"""
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
