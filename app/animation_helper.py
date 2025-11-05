"""
Animation Utilities - Smooth transitions and effects
"""
import customtkinter as ctk
from typing import Callable, Optional
import threading
import time


class AnimationHelper:
    """Helper class for smooth animations"""
    
    @staticmethod
    def fade_out(widget: ctk.CTkBaseClass, duration_ms: int = 200, callback: Optional[Callable] = None):
        """
        Fade out animation for widget
        
        Args:
            widget: Widget to fade out
            duration_ms: Duration in milliseconds
            callback: Optional callback after animation
        """
        steps = 20
        delay = duration_ms / steps / 1000.0  # Convert to seconds
        
        def animate():
            try:
                for i in range(steps, -1, -1):
                    alpha = i / steps
                    if hasattr(widget, 'winfo_exists') and widget.winfo_exists():
                        widget.configure(fg_color=AnimationHelper._adjust_alpha(
                            widget.cget('fg_color'), alpha
                        ))
                        time.sleep(delay)
                    else:
                        break
                
                if callback:
                    widget.after(0, callback)
            except Exception as e:
                print(f"Fade out animation error: {e}")
        
        threading.Thread(target=animate, daemon=True).start()
    
    @staticmethod
    def fade_in(widget: ctk.CTkBaseClass, duration_ms: int = 200, callback: Optional[Callable] = None):
        """
        Fade in animation for widget
        
        Args:
            widget: Widget to fade in
            duration_ms: Duration in milliseconds
            callback: Optional callback after animation
        """
        steps = 20
        delay = duration_ms / steps / 1000.0
        
        def animate():
            try:
                for i in range(steps + 1):
                    alpha = i / steps
                    if hasattr(widget, 'winfo_exists') and widget.winfo_exists():
                        # Simply show widget progressively
                        time.sleep(delay)
                    else:
                        break
                
                if callback:
                    widget.after(0, callback)
            except Exception as e:
                print(f"Fade in animation error: {e}")
        
        threading.Thread(target=animate, daemon=True).start()
    
    @staticmethod
    def slide_left(widget: ctk.CTkBaseClass, distance: int = 300, duration_ms: int = 250):
        """
        Slide widget to the left
        
        Args:
            widget: Widget to slide
            distance: Distance to slide in pixels
            duration_ms: Duration in milliseconds
        """
        steps = 20
        delay = duration_ms / steps / 1000.0
        step_distance = distance / steps
        
        def animate():
            try:
                current_x = widget.winfo_x()
                for i in range(steps + 1):
                    if hasattr(widget, 'winfo_exists') and widget.winfo_exists():
                        new_x = current_x - (step_distance * i)
                        widget.place(x=new_x)
                        time.sleep(delay)
                    else:
                        break
            except Exception as e:
                print(f"Slide left animation error: {e}")
        
        threading.Thread(target=animate, daemon=True).start()
    
    @staticmethod
    def slide_right(widget: ctk.CTkBaseClass, distance: int = 300, duration_ms: int = 250):
        """
        Slide widget to the right
        
        Args:
            widget: Widget to slide
            distance: Distance to slide in pixels
            duration_ms: Duration in milliseconds
        """
        steps = 20
        delay = duration_ms / steps / 1000.0
        step_distance = distance / steps
        
        def animate():
            try:
                current_x = widget.winfo_x()
                for i in range(steps + 1):
                    if hasattr(widget, 'winfo_exists') and widget.winfo_exists():
                        new_x = current_x + (step_distance * i)
                        widget.place(x=new_x)
                        time.sleep(delay)
                    else:
                        break
            except Exception as e:
                print(f"Slide right animation error: {e}")
        
        threading.Thread(target=animate, daemon=True).start()
    
    @staticmethod
    def crossfade(old_widget: ctk.CTkBaseClass, new_widget: ctk.CTkBaseClass, 
                  duration_ms: int = 200):
        """
        Crossfade between two widgets
        
        Args:
            old_widget: Widget to fade out
            new_widget: Widget to fade in
            duration_ms: Duration in milliseconds
        """
        # Hide new widget initially
        if hasattr(new_widget, 'place_forget'):
            new_widget.place_forget()
        
        # Fade out old widget
        AnimationHelper.fade_out(old_widget, duration_ms, lambda: old_widget.place_forget())
        
        # Wait a bit then fade in new widget
        def show_new():
            time.sleep(duration_ms / 2000.0)  # Wait half duration
            if hasattr(new_widget, 'winfo_exists') and new_widget.winfo_exists():
                new_widget.place(relx=0.5, rely=0.5, anchor='center')
                AnimationHelper.fade_in(new_widget, duration_ms)
        
        threading.Thread(target=show_new, daemon=True).start()
    
    @staticmethod
    def _adjust_alpha(color: str, alpha: float) -> str:
        """
        Adjust alpha channel of color (simplified)
        
        Args:
            color: Color string
            alpha: Alpha value (0-1)
            
        Returns:
            Color string with adjusted alpha
        """
        # For simplicity, return original color
        # CustomTkinter doesn't support alpha in colors directly
        return color
    
    @staticmethod
    def smooth_scroll(scrollable_frame, target_y: float, duration_ms: int = 300):
        """
        Smooth scroll animation for scrollable frames
        
        Args:
            scrollable_frame: CTkScrollableFrame instance
            target_y: Target scroll position (0-1)
            duration_ms: Duration in milliseconds
        """
        if not hasattr(scrollable_frame, '_parent_canvas'):
            return
        
        steps = 20
        delay = duration_ms / steps / 1000.0
        
        def animate():
            try:
                current_y = scrollable_frame._parent_canvas.yview()[0]
                step_y = (target_y - current_y) / steps
                
                for i in range(steps + 1):
                    if hasattr(scrollable_frame, 'winfo_exists') and scrollable_frame.winfo_exists():
                        new_y = current_y + (step_y * i)
                        scrollable_frame._parent_canvas.yview_moveto(new_y)
                        time.sleep(delay)
                    else:
                        break
            except Exception as e:
                print(f"Smooth scroll animation error: {e}")
        
        threading.Thread(target=animate, daemon=True).start()
