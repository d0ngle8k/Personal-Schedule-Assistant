"""
Event Context Menu
Right-click menu for event items with actions
"""
import customtkinter as ctk
from tkinter import Menu
from typing import Callable, Optional
from app.config import COLORS


class EventContextMenu:
    """
    Context menu for event items
    Shows on right-click with Edit, Duplicate, Delete, Details options
    """
    
    def __init__(self, parent, event_id: int, event_name: str,
                 on_edit: Optional[Callable] = None,
                 on_duplicate: Optional[Callable] = None,
                 on_delete: Optional[Callable] = None,
                 on_details: Optional[Callable] = None):
        """
        Initialize context menu
        
        Args:
            parent: Parent widget
            event_id: ID of the event
            event_name: Name of the event (for display)
            on_edit: Callback for edit action
            on_duplicate: Callback for duplicate action
            on_delete: Callback for delete action
            on_details: Callback for details action
        """
        self.parent = parent
        self.event_id = event_id
        self.event_name = event_name
        self.on_edit = on_edit
        self.on_duplicate = on_duplicate
        self.on_delete = on_delete
        self.on_details = on_details
        
        # Create the menu
        self.menu = Menu(
            parent,
            tearoff=0,
            font=("Segoe UI", 11),
            bg='white',
            fg=COLORS['text_primary'],
            activebackground=COLORS['primary_blue'],
            activeforeground='white',
            relief='flat',
            borderwidth=1
        )
        
        self._build_menu()
    
    def _build_menu(self):
        """Build menu items"""
        # Edit option
        if self.on_edit:
            self.menu.add_command(
                label="✏️  Chỉnh sửa",
                command=self._handle_edit,
                font=("Segoe UI", 11)
            )
        
        # Duplicate option
        if self.on_duplicate:
            self.menu.add_command(
                label="📋  Nhân bản",
                command=self._handle_duplicate,
                font=("Segoe UI", 11)
            )
        
        self.menu.add_separator()
        
        # Delete option (red text)
        if self.on_delete:
            self.menu.add_command(
                label="🗑️  Xóa",
                command=self._handle_delete,
                font=("Segoe UI", 11, "bold"),
                foreground=COLORS['error']
            )
        
        self.menu.add_separator()
        
        # Details option
        if self.on_details:
            self.menu.add_command(
                label="ℹ️  Chi tiết",
                command=self._handle_details,
                font=("Segoe UI", 11)
            )
    
    def _handle_edit(self):
        """Handle edit action"""
        if self.on_edit:
            self.on_edit(self.event_id)
    
    def _handle_duplicate(self):
        """Handle duplicate action"""
        if self.on_duplicate:
            self.on_duplicate(self.event_id)
    
    def _handle_delete(self):
        """Handle delete action"""
        if self.on_delete:
            self.on_delete(self.event_id)
    
    def _handle_details(self):
        """Handle details action"""
        if self.on_details:
            self.on_details(self.event_id)
    
    def show(self, x: int, y: int):
        """
        Show the context menu at given coordinates
        
        Args:
            x: X coordinate (screen)
            y: Y coordinate (screen)
        """
        try:
            self.menu.tk_popup(x, y)
        finally:
            self.menu.grab_release()
