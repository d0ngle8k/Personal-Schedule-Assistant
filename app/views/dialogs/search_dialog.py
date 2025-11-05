"""
Event Search Dialog
Search events by keyword with results display
"""
import customtkinter as ctk
from tkinter import messagebox
from typing import List, Optional
from datetime import datetime
from app.config import COLORS, FONTS, SPACING


class SearchDialog(ctk.CTkToplevel):
    """
    Modal search dialog for finding events
    Search by event name, location, description
    """
    
    def __init__(self, parent, controller):
        """
        Initialize search dialog
        
        Args:
            parent: Parent window
            controller: MainController instance
        """
        super().__init__(parent)
        
        self.controller = controller
        self.search_results = []
        
        # Configure window
        self.title("🔍 Tìm kiếm sự kiện")
        self.geometry("700x600")
        self.resizable(False, False)
        
        # Modal behavior
        self.transient(parent)
        self.grab_set()
        
        # Center on parent
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 700) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 600) // 2
        self.geometry(f"+{x}+{y}")
        
        # Build UI
        self._create_ui()
        
        # Keyboard shortcuts
        self.bind('<Escape>', lambda e: self.destroy())
        self.bind('<Return>', lambda e: self._search())
        
        # Focus on search input
        self.search_entry.focus_set()
    
    def _create_ui(self):
        """Build the UI"""
        # Main container
        container = ctk.CTkFrame(self, fg_color=COLORS['bg_white'])
        container.pack(fill='both', expand=True, padx=SPACING['lg'], pady=SPACING['lg'])
        
        # Header
        header = ctk.CTkLabel(
            container,
            text="🔍 Tìm kiếm sự kiện",
            font=FONTS['heading'],
            text_color=COLORS['text_primary']
        )
        header.pack(pady=(0, SPACING['md']))
        
        # Search input section
        search_frame = ctk.CTkFrame(container, fg_color='transparent')
        search_frame.pack(fill='x', pady=(0, SPACING['lg']))
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            height=44,
            font=FONTS['body'],
            placeholder_text="Nhập từ khóa tìm kiếm..."
        )
        self.search_entry.pack(side='left', fill='x', expand=True, padx=(0, SPACING['sm']))
        
        search_btn = ctk.CTkButton(
            search_frame,
            text="🔍 Tìm",
            width=100,
            height=44,
            fg_color=COLORS['primary_blue'],
            hover_color=COLORS['primary_blue_hover'],
            font=FONTS['body_bold'],
            command=self._search
        )
        search_btn.pack(side='right')
        
        # Results info
        self.results_label = ctk.CTkLabel(
            container,
            text="",
            font=FONTS['caption'],
            text_color=COLORS['text_secondary']
        )
        self.results_label.pack(anchor='w', pady=(0, SPACING['sm']))
        
        # Results list (scrollable)
        self.results_frame = ctk.CTkScrollableFrame(
            container,
            fg_color=COLORS['bg_gray'],
            corner_radius=8
        )
        self.results_frame.pack(fill='both', expand=True, pady=(0, SPACING['md']))
        
        # Close button
        close_btn = ctk.CTkButton(
            container,
            text="✕ Đóng",
            width=120,
            height=40,
            fg_color=COLORS['bg_gray'],
            hover_color=COLORS['bg_gray_hover'],
            font=FONTS['body'],
            command=self.destroy
        )
        close_btn.pack()
    
    def _search(self):
        """Perform search"""
        keyword = self.search_entry.get().strip()
        
        if not keyword:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập từ khóa tìm kiếm")
            return
        
        # Search using controller
        try:
            self.search_results = self.controller.search_events(keyword)
            self._display_results()
        except Exception as e:
            print(f"Error searching events: {e}")
            messagebox.showerror("Lỗi", f"Lỗi khi tìm kiếm: {str(e)}")
    
    def _display_results(self):
        """Display search results"""
        # Clear existing results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        if not self.search_results:
            # No results
            self.results_label.configure(text="❌ Không tìm thấy kết quả")
            
            no_results_label = ctk.CTkLabel(
                self.results_frame,
                text="Không có sự kiện nào khớp với từ khóa",
                font=FONTS['body'],
                text_color=COLORS['text_secondary']
            )
            no_results_label.pack(pady=SPACING['xl'])
            return
        
        # Show results count
        self.results_label.configure(
            text=f"✅ Tìm thấy {len(self.search_results)} sự kiện"
        )
        
        # Display each result
        for event in self.search_results:
            self._create_result_item(event)
    
    def _create_result_item(self, event):
        """Create a single result item"""
        item_frame = ctk.CTkFrame(
            self.results_frame,
            fg_color=COLORS['bg_white'],
            corner_radius=8,
            cursor="hand2"
        )
        item_frame.pack(fill='x', pady=SPACING['xs'], padx=SPACING['sm'])
        
        # Content container
        content = ctk.CTkFrame(item_frame, fg_color='transparent')
        content.pack(fill='both', expand=True, padx=SPACING['md'], pady=SPACING['sm'])
        
        # Event name (bold)
        name_label = ctk.CTkLabel(
            content,
            text=event.event_name,
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary'],
            anchor='w'
        )
        name_label.pack(anchor='w', fill='x')
        
        # Event details row
        details_frame = ctk.CTkFrame(content, fg_color='transparent')
        details_frame.pack(anchor='w', fill='x', pady=(SPACING['xs'], 0))
        
        # Date and time
        date_time_text = f"📅 {event.get_formatted_date()} • ⏰ {event.get_formatted_time()}"
        details_label = ctk.CTkLabel(
            details_frame,
            text=date_time_text,
            font=FONTS['caption'],
            text_color=COLORS['text_secondary'],
            anchor='w'
        )
        details_label.pack(side='left')
        
        # Location (if available)
        if event.location:
            location_label = ctk.CTkLabel(
                details_frame,
                text=f" • 📍 {event.location}",
                font=FONTS['caption'],
                text_color=COLORS['text_secondary'],
                anchor='w'
            )
            location_label.pack(side='left')
        
        # Category badge
        category_badge = ctk.CTkLabel(
            content,
            text=f"🏷️ {event.category}",
            font=FONTS['small'],
            text_color='white',
            fg_color=event.category_color,
            corner_radius=4,
            padx=SPACING['sm'],
            pady=2
        )
        category_badge.pack(anchor='w', pady=(SPACING['xs'], 0))
        
        # Bind click to navigate to event
        item_frame.bind("<Button-1>", lambda e, evt=event: self._on_result_click(evt))
        for child in item_frame.winfo_children():
            child.bind("<Button-1>", lambda e, evt=event: self._on_result_click(evt))
    
    def _on_result_click(self, event):
        """Handle result item click"""
        try:
            # Navigate to event's date
            if event.start_time:
                self.controller.model.set_current_date(event.start_time.date())
                self.controller.refresh_events()
                self.controller.update_calendar_title()
            
            # Close search dialog
            self.destroy()
            
            # Open edit dialog
            self.controller.show_edit_dialog(event.id)
        except Exception as e:
            print(f"Error navigating to event: {e}")
