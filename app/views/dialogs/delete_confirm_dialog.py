"""
Delete Confirmation Dialog
Simple confirmation dialog for deleting events
"""
import customtkinter as ctk
from tkinter import messagebox
from app.config import COLORS, FONTS, SPACING


class DeleteConfirmDialog(ctk.CTkToplevel):
    """
    Confirmation dialog for deleting events
    Shows event name and warning message
    """
    
    def __init__(self, parent, event_name: str, on_confirm_delete):
        """
        Initialize delete confirmation dialog
        
        Args:
            parent: Parent window
            event_name: Name of event to delete
            on_confirm_delete: Callback function when delete confirmed
        """
        super().__init__(parent)
        
        self.event_name = event_name
        self.on_confirm_delete = on_confirm_delete
        self.result = None
        
        # Dialog configuration
        self.title("Xác nhận xóa")
        self.geometry("450x220")
        self.resizable(False, False)
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        # Center on parent
        self._center_on_parent(parent)
        
        # Setup UI
        self._setup_ui()
    
    def _center_on_parent(self, parent):
        """Center dialog on parent window"""
        self.update_idletasks()
        
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        
        dialog_width = self.winfo_width()
        dialog_height = self.winfo_height()
        
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        
        self.geometry(f"+{x}+{y}")
    
    def _setup_ui(self):
        """Setup dialog UI"""
        # Main container
        container = ctk.CTkFrame(self, fg_color='transparent')
        container.pack(fill='both', expand=True, padx=SPACING['xl'], pady=SPACING['xl'])
        
        # Warning icon and title
        header_frame = ctk.CTkFrame(container, fg_color='transparent')
        header_frame.pack(fill='x', pady=(0, SPACING['lg']))
        
        # Warning icon
        icon_label = ctk.CTkLabel(
            header_frame,
            text="⚠️",
            font=("Segoe UI", 48),
            text_color=COLORS['warning']
        )
        icon_label.pack(pady=(0, SPACING['sm']))
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="Xác nhận xóa sự kiện",
            font=FONTS['heading'],
            text_color=COLORS['text_primary']
        )
        title_label.pack()
        
        # Message container
        message_frame = ctk.CTkFrame(
            container,
            fg_color=COLORS['bg_gray'],
            corner_radius=8
        )
        message_frame.pack(fill='x', pady=(0, SPACING['lg']))
        
        # Event name
        event_label = ctk.CTkLabel(
            message_frame,
            text=f'"{self.event_name}"',
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary'],
            wraplength=350
        )
        event_label.pack(pady=(SPACING['md'], SPACING['xs']))
        
        # Warning message
        warning_label = ctk.CTkLabel(
            message_frame,
            text="Hành động này không thể hoàn tác!",
            font=FONTS['body'],
            text_color=COLORS['error'],
            wraplength=350
        )
        warning_label.pack(pady=(0, SPACING['md']))
        
        # Buttons
        button_frame = ctk.CTkFrame(container, fg_color='transparent')
        button_frame.pack(fill='x')
        
        # Cancel button (left)
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="↩️ Hủy",
            width=140,
            height=44,
            fg_color=COLORS['bg_gray'],
            text_color=COLORS['text_primary'],
            hover_color=COLORS['border_light'],
            font=FONTS['body'],
            corner_radius=6,
            command=self._cancel
        )
        cancel_btn.pack(side='left', expand=True, padx=(0, SPACING['sm']))
        
        # Delete button (right)
        delete_btn = ctk.CTkButton(
            button_frame,
            text="🗑️ Xóa sự kiện",
            width=140,
            height=44,
            fg_color=COLORS['error'],
            text_color='white',
            hover_color="#b71c1c",
            font=FONTS['body_bold'],
            corner_radius=6,
            command=self._confirm_delete
        )
        delete_btn.pack(side='right', expand=True, padx=(SPACING['sm'], 0))
        
        # Focus on cancel button by default (safe default)
        cancel_btn.focus()
        
        # Bind Escape key to cancel
        self.bind('<Escape>', lambda e: self._cancel())
    
    def _confirm_delete(self):
        """Confirm deletion"""
        self.result = 'deleted'
        self.destroy()
        
        # Call the callback
        if self.on_confirm_delete:
            self.on_confirm_delete()
    
    def _cancel(self):
        """Cancel deletion"""
        self.result = 'cancelled'
        self.destroy()
