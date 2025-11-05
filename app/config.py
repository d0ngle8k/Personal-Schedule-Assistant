"""
Configuration file for Google Calendar UI
Contains colors, fonts, spacing, and other constants
"""

# Google Calendar Color Palette - Light Mode
COLORS_LIGHT = {
    # Primary Colors
    "primary_blue": "#1a73e8",
    "primary_blue_hover": "#1557b0",
    "primary_blue_light": "#e8f0fe",
    "primary_blue_dark": "#174ea6",
    
    # Background Colors
    "bg_white": "#ffffff",
    "bg_gray": "#f1f3f4",
    "bg_gray_hover": "#e8eaed",
    "bg_gray_dark": "#dadce0",
    
    # Text Colors
    "text_primary": "#3c4043",
    "text_secondary": "#5f6368",
    "text_disabled": "#80868b",
    "text_light": "#ffffff",
    "text_white": "#ffffff",
    
    # Border Colors
    "border_light": "#dadce0",
    "border_focus": "#1a73e8",
    "border_error": "#d93025",
    
    # Event Category Colors (6 categories)
    "event_work": "#039be5",          # Blue - Công việc
    "event_health": "#7cb342",        # Green - Khám bệnh
    "event_food": "#f6bf26",          # Yellow - Ăn uống
    "event_study": "#e67c73",         # Red - Học tập
    "event_sport": "#33b679",         # Dark Green - Thể thao
    "event_entertainment": "#8e24aa", # Purple - Giải trí
    
    # Status Colors
    "success": "#0f9d58",
    "success_green": "#0f9d58",
    "success_green_hover": "#0d8043",
    "warning": "#f9ab00",
    "warning_yellow": "#f9ab00",
    "error": "#d93025",
    "info": "#1a73e8",
}

# Dark Mode Color Palette
COLORS_DARK = {
    # Primary Colors
    "primary_blue": "#8ab4f8",
    "primary_blue_hover": "#aecbfa",
    "primary_blue_light": "#1a2e45",
    "primary_blue_dark": "#669df6",
    
    # Background Colors
    "bg_white": "#202124",
    "bg_gray": "#292a2d",
    "bg_gray_hover": "#35363a",
    "bg_gray_dark": "#3c4043",
    
    # Text Colors
    "text_primary": "#e8eaed",
    "text_secondary": "#9aa0a6",
    "text_disabled": "#5f6368",
    "text_light": "#202124",
    "text_white": "#ffffff",
    
    # Border Colors
    "border_light": "#5f6368",
    "border_focus": "#8ab4f8",
    "border_error": "#f28b82",
    
    # Event Category Colors (adjusted for dark mode)
    "event_work": "#4285f4",
    "event_health": "#81c995",
    "event_food": "#fdd663",
    "event_study": "#ee675c",
    "event_sport": "#57bb8a",
    "event_entertainment": "#ab47bc",
    
    # Status Colors
    "success": "#81c995",
    "success_green": "#81c995",
    "success_green_hover": "#57bb8a",
    "warning": "#fdd663",
    "warning_yellow": "#fdd663",
    "error": "#f28b82",
    "info": "#8ab4f8",
}

# Default to light mode
COLORS = COLORS_LIGHT.copy()

# Event Category Mapping
EVENT_CATEGORIES = {
    "work": {"name": "Công việc", "color": COLORS["event_work"], "icon": "💼"},
    "health": {"name": "Khám bệnh", "color": COLORS["event_health"], "icon": "🏥"},
    "food": {"name": "Ăn uống", "color": COLORS["event_food"], "icon": "🍽️"},
    "study": {"name": "Học tập", "color": COLORS["event_study"], "icon": "📚"},
    "sport": {"name": "Thể thao", "color": COLORS["event_sport"], "icon": "⚽"},
    "entertainment": {"name": "Giải trí", "color": COLORS["event_entertainment"], "icon": "🎬"},
}

# Typography System (Google Fonts - Roboto)
FONTS = {
    "title": ("Segoe UI", 22, "bold"),      # Windows fallback for Roboto
    "heading": ("Segoe UI", 16, "bold"),
    "subheading": ("Segoe UI", 14, "bold"),
    "body": ("Segoe UI", 13, "normal"),
    "body_bold": ("Segoe UI", 13, "bold"),
    "caption": ("Segoe UI", 11, "normal"),
    "button": ("Segoe UI", 14, "bold"),
    "small": ("Segoe UI", 10, "normal"),
}

# Spacing System (8px base unit)
SPACING = {
    "xxs": 2,  # Extra extra small
    "xs": 4,   # Extra small
    "sm": 8,   # Small
    "md": 16,  # Medium
    "lg": 24,  # Large
    "xl": 32,  # Extra large
    "xxl": 48, # Extra extra large
}

# Size/Radius System
SIZES = {
    "radius_sm": 4,
    "radius_md": 8,
    "radius_lg": 12,
    "radius_xl": 16,
}

# Layout Dimensions
LAYOUT = {
    "sidebar_width": 260,
    "topbar_height": 64,
    "button_height": 44,
    "input_height": 40,
    "card_corner_radius": 8,
    "button_corner_radius": 24,
    "window_min_width": 1000,
    "window_min_height": 600,
    "window_default_width": 1200,
    "window_default_height": 800,
}

# Animation & Transitions - OPTIMIZED for instant feel
ANIMATIONS = {
    "hover_duration": 100,  # milliseconds (faster = more responsive)
    "transition_duration": 150,  # Reduced from 300ms
    "fade_duration": 100,  # Reduced from 200ms (users prefer instant)
    "slide_duration": 120,  # Reduced from 250ms
    "theme_transition": 150,  # Reduced from 300ms
    "fps": 60,  # frames per second for smooth animation
    "easing": "ease_out_expo",  # Fast deceleration for snappy feel
    "debounce_delay": 50,  # Debounce UI updates (ms)
}

# View Types
VIEW_TYPES = {
    "day": "Ngày",
    "week": "Tuần",
    "month": "Tháng",
    "year": "Năm",
    "schedule": "Lịch trình",
}

# Vietnamese Weekdays
WEEKDAYS_SHORT = ["CN", "T2", "T3", "T4", "T5", "T6", "T7"]
WEEKDAYS_LONG = [
    "Chủ nhật",
    "Thứ hai",
    "Thứ ba",
    "Thứ tư",
    "Thứ năm",
    "Thứ sáu",
    "Thứ bảy",
]

# Vietnamese Months
MONTHS = [
    "Tháng 1", "Tháng 2", "Tháng 3", "Tháng 4",
    "Tháng 5", "Tháng 6", "Tháng 7", "Tháng 8",
    "Tháng 9", "Tháng 10", "Tháng 11", "Tháng 12",
]

# Time Format
TIME_FORMAT = {
    "hour_24": "%H:%M",
    "hour_12": "%I:%M %p",
    "date": "%d/%m/%Y",
    "datetime": "%d/%m/%Y %H:%M",
    "iso": "%Y-%m-%d %H:%M:%S",
}

# Application Metadata
APP_INFO = {
    "name": "Trợ Lý Lịch Trình",
    "version": "0.7.0",
    "author": "d0ngle8k",
    "description": "Personal Schedule Assistant with NLP Vietnamese",
}
