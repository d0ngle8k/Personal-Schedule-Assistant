"""
Theme Manager - Handle Light/Dark Mode Switching
"""
from typing import Callable, Dict
from app.config import COLORS_LIGHT, COLORS_DARK, COLORS


class ThemeManager:
    """Manage application theme (Light/Dark mode)"""
    
    def __init__(self):
        self.is_dark_mode = False
        self._listeners = []
    
    def toggle_theme(self):
        """Toggle between light and dark mode"""
        self.is_dark_mode = not self.is_dark_mode
        self._update_colors()
        self._notify_listeners()
    
    def set_dark_mode(self, enabled: bool):
        """Set dark mode explicitly"""
        if self.is_dark_mode != enabled:
            self.is_dark_mode = enabled
            self._update_colors()
            self._notify_listeners()
    
    def get_current_colors(self) -> Dict:
        """Get current theme colors"""
        return COLORS_DARK if self.is_dark_mode else COLORS_LIGHT
    
    def _update_colors(self):
        """Update global COLORS dict"""
        source = COLORS_DARK if self.is_dark_mode else COLORS_LIGHT
        COLORS.clear()
        COLORS.update(source)
    
    def add_listener(self, callback: Callable):
        """Add a listener for theme changes"""
        if callback not in self._listeners:
            self._listeners.append(callback)
    
    def remove_listener(self, callback: Callable):
        """Remove a theme change listener"""
        if callback in self._listeners:
            self._listeners.remove(callback)
    
    def _notify_listeners(self):
        """Notify all listeners of theme change"""
        for callback in self._listeners:
            try:
                callback(self.is_dark_mode)
            except Exception as e:
                print(f"Error notifying theme listener: {e}")


# Global theme manager instance
theme_manager = ThemeManager()
