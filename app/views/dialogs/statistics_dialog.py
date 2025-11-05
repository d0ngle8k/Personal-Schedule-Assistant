"""Statistics Dialog - Event Analytics Dashboard"""

import customtkinter as ctk
from tkinter import messagebox
from typing import Dict, Any
from app.config import COLORS, FONTS, SPACING, SIZES


class StatisticsDialog(ctk.CTkToplevel):
    """Statistics dialog showing event analytics"""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        self.controller = controller
        self.stats = {}
        
        # Window configuration
        self.title("📊 Thống kê lịch trình")
        self.geometry("900x700")
        self.resizable(True, True)
        
        # Modal
        self.transient(parent)
        self.grab_set()
        
        # Style
        self.configure(fg_color=COLORS['bg_white'])
        
        # Load statistics
        self._load_statistics()
        
        # Create UI
        self._create_ui()
        
        # Center window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.winfo_screenheight() // 2) - (700 // 2)
        self.geometry(f"+{x}+{y}")
        
        # Bind shortcuts
        self.bind("<Escape>", lambda e: self.destroy())
    
    def _load_statistics(self):
        """Load statistics from controller"""
        try:
            # Get stats from controller
            overview = self.controller.get_overview_statistics()
            category_stats = self.controller.get_category_statistics()
            
            self.stats = {
                'overview': overview,
                'category': category_stats
            }
        except Exception as e:
            print(f"Error loading statistics: {e}")
            self.stats = {
                'overview': {
                    'total_events': 0,
                    'upcoming_events': 0,
                    'past_events': 0,
                    'this_week': 0,
                    'this_month': 0
                },
                'category': {}
            }
    
    def _create_ui(self):
        """Create statistics UI"""
        # Main container with padding
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=SPACING['xl'], pady=SPACING['xl'])
        
        # Title bar
        title_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, SPACING['lg']))
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="📊 Thống kê lịch trình",
            font=FONTS['title'],
            text_color=COLORS['text_primary']
        )
        title_label.pack(side="left")
        
        refresh_btn = ctk.CTkButton(
            title_frame,
            text="🔄 Làm mới",
            width=100,
            height=35,
            fg_color=COLORS['primary_blue'],
            hover_color=COLORS['primary_blue_hover'],
            text_color=COLORS['text_white'],
            font=FONTS['small'],
            corner_radius=SIZES['radius_md'],
            command=self._refresh_statistics
        )
        refresh_btn.pack(side="right")
        
        # Scrollable content
        scrollable_frame = ctk.CTkScrollableFrame(
            main_container,
            fg_color=COLORS['bg_white'],
            corner_radius=SIZES['radius_md']
        )
        scrollable_frame.pack(fill="both", expand=True)
        
        # Overview cards (top row)
        self._create_overview_section(scrollable_frame)
        
        # Category breakdown
        self._create_category_section(scrollable_frame)
        
        # Time distribution (weekday breakdown)
        self._create_time_section(scrollable_frame)
        
        # Close button
        close_btn = ctk.CTkButton(
            main_container,
            text="Đóng",
            width=120,
            height=40,
            fg_color=COLORS['bg_gray'],
            hover_color=COLORS['bg_gray_hover'],
            text_color=COLORS['text_primary'],
            font=FONTS['body'],
            corner_radius=SIZES['radius_md'],
            command=self.destroy
        )
        close_btn.pack(pady=(SPACING['lg'], 0))
    
    def _create_overview_section(self, parent):
        """Create overview statistics cards"""
        section_frame = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )
        section_frame.pack(fill="x", pady=(0, SPACING['xl']))
        
        # Section title
        section_title = ctk.CTkLabel(
            section_frame,
            text="📈 Tổng quan",
            font=FONTS['heading'],
            text_color=COLORS['text_primary'],
            anchor="w"
        )
        section_title.pack(fill="x", pady=(0, SPACING['md']))
        
        # Cards container
        cards_container = ctk.CTkFrame(section_frame, fg_color="transparent")
        cards_container.pack(fill="x")
        
        # Configure grid
        cards_container.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="stat_card")
        
        # Get overview stats
        overview = self.stats.get('overview', {})
        
        # Create stat cards
        cards_data = [
            ("📅", "Tổng số sự kiện", overview.get('total_events', 0), COLORS['primary_blue']),
            ("🔜", "Sắp tới", overview.get('upcoming_events', 0), COLORS['success_green']),
            ("✅", "Đã qua", overview.get('past_events', 0), COLORS['text_secondary']),
            ("📆", "Tuần này", overview.get('this_week', 0), COLORS['warning_yellow']),
        ]
        
        for col, (icon, label, value, color) in enumerate(cards_data):
            card = self._create_stat_card(cards_container, icon, label, value, color)
            card.grid(row=0, column=col, padx=SPACING['sm'], sticky="ew")
    
    def _create_stat_card(self, parent, icon, label, value, color):
        """Create a single stat card"""
        card = ctk.CTkFrame(
            parent,
            fg_color=COLORS['bg_gray'],
            corner_radius=SIZES['radius_md']
        )
        
        # Icon
        icon_label = ctk.CTkLabel(
            card,
            text=icon,
            font=("Segoe UI Emoji", 32),
            text_color=color
        )
        icon_label.pack(pady=(SPACING['md'], SPACING['xs']))
        
        # Value
        value_label = ctk.CTkLabel(
            card,
            text=str(value),
            font=("Segoe UI", 28, "bold"),
            text_color=COLORS['text_primary']
        )
        value_label.pack(pady=SPACING['xs'])
        
        # Label
        label_widget = ctk.CTkLabel(
            card,
            text=label,
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        )
        label_widget.pack(pady=(0, SPACING['md']))
        
        return card
    
    def _create_category_section(self, parent):
        """Create category breakdown section"""
        section_frame = ctk.CTkFrame(
            parent,
            fg_color=COLORS['bg_gray'],
            corner_radius=SIZES['radius_md']
        )
        section_frame.pack(fill="x", pady=(0, SPACING['lg']))
        
        # Section title
        section_title = ctk.CTkLabel(
            section_frame,
            text="📂 Phân loại theo danh mục",
            font=FONTS['heading'],
            text_color=COLORS['text_primary'],
            anchor="w"
        )
        section_title.pack(fill="x", padx=SPACING['lg'], pady=(SPACING['lg'], SPACING['md']))
        
        # Category data
        category_stats = self.stats.get('category', {})
        
        if not category_stats:
            # No data message
            no_data_label = ctk.CTkLabel(
                section_frame,
                text="Chưa có dữ liệu danh mục",
                font=FONTS['body'],
                text_color=COLORS['text_secondary']
            )
            no_data_label.pack(pady=SPACING['xl'])
        else:
            # Create bars for each category
            total_events = self.stats['overview'].get('total_events', 1)
            
            for category, count in sorted(category_stats.items(), key=lambda x: x[1], reverse=True):
                self._create_category_bar(section_frame, category, count, total_events)
        
        # Add padding at bottom
        ctk.CTkFrame(section_frame, fg_color="transparent", height=SPACING['lg']).pack()
    
    def _create_category_bar(self, parent, category, count, total):
        """Create a horizontal bar chart for category"""
        bar_container = ctk.CTkFrame(parent, fg_color="transparent")
        bar_container.pack(fill="x", padx=SPACING['lg'], pady=SPACING['xs'])
        
        # Category label and count
        label_frame = ctk.CTkFrame(bar_container, fg_color="transparent")
        label_frame.pack(fill="x", pady=(0, SPACING['xxs']))
        
        category_label = ctk.CTkLabel(
            label_frame,
            text=category,
            font=FONTS['body'],
            text_color=COLORS['text_primary'],
            anchor="w"
        )
        category_label.pack(side="left")
        
        percentage = (count / total * 100) if total > 0 else 0
        count_label = ctk.CTkLabel(
            label_frame,
            text=f"{count} ({percentage:.1f}%)",
            font=FONTS['small'],
            text_color=COLORS['text_secondary'],
            anchor="e"
        )
        count_label.pack(side="right")
        
        # Progress bar
        progress_bar = ctk.CTkProgressBar(
            bar_container,
            height=12,
            corner_radius=SIZES['radius_sm'],
            fg_color=COLORS['bg_white'],
            progress_color=COLORS['primary_blue']
        )
        progress_bar.pack(fill="x")
        progress_bar.set(percentage / 100)
    
    def _create_time_section(self, parent):
        """Create time distribution section (weekday breakdown)"""
        section_frame = ctk.CTkFrame(
            parent,
            fg_color=COLORS['bg_gray'],
            corner_radius=SIZES['radius_md']
        )
        section_frame.pack(fill="x", pady=(0, SPACING['lg']))
        
        # Section title
        section_title = ctk.CTkLabel(
            section_frame,
            text="📅 Phân bố theo ngày trong tuần",
            font=FONTS['heading'],
            text_color=COLORS['text_primary'],
            anchor="w"
        )
        section_title.pack(fill="x", padx=SPACING['lg'], pady=(SPACING['lg'], SPACING['md']))
        
        # Weekday labels
        weekdays = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'Chủ nhật']
        
        # Calculate weekday distribution (simplified - just show equal distribution for now)
        # TODO: Get actual weekday distribution from database
        total_events = self.stats['overview'].get('total_events', 0)
        avg_per_day = total_events / 7 if total_events > 0 else 0
        
        # Create weekday cards
        weekday_container = ctk.CTkFrame(section_frame, fg_color="transparent")
        weekday_container.pack(fill="x", padx=SPACING['lg'], pady=(0, SPACING['lg']))
        
        # Configure grid for 7 columns
        for i in range(7):
            weekday_container.grid_columnconfigure(i, weight=1, uniform="weekday")
        
        for i, day in enumerate(weekdays):
            day_card = ctk.CTkFrame(
                weekday_container,
                fg_color=COLORS['bg_white'],
                corner_radius=SIZES['radius_sm']
            )
            day_card.grid(row=0, column=i, padx=SPACING['xxs'], pady=SPACING['xs'], sticky="ew")
            
            # Day label
            day_label = ctk.CTkLabel(
                day_card,
                text=day,
                font=FONTS['small'],
                text_color=COLORS['text_secondary']
            )
            day_label.pack(pady=(SPACING['xs'], 0))
            
            # Count (using average for now)
            count_label = ctk.CTkLabel(
                day_card,
                text=str(int(avg_per_day)),
                font=("Segoe UI", 16, "bold"),
                text_color=COLORS['text_primary']
            )
            count_label.pack(pady=(0, SPACING['xs']))
        
        # Add padding at bottom
        ctk.CTkFrame(section_frame, fg_color="transparent", height=SPACING['md']).pack()
    
    def _refresh_statistics(self):
        """Refresh statistics data"""
        try:
            self._load_statistics()
            # Destroy and recreate UI
            for widget in self.winfo_children():
                widget.destroy()
            self._create_ui()
            messagebox.showinfo("Thành công", "✅ Đã làm mới thống kê")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể làm mới thống kê:\n{str(e)}")
