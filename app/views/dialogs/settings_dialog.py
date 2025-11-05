"""Settings Dialog - Import/Export and App Configuration"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
from typing import Optional
from app.config import COLORS, FONTS, SPACING, SIZES


class SettingsDialog(ctk.CTkToplevel):
    """Settings dialog with Import/Export options"""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        self.controller = controller
        
        # Window configuration
        self.title("⚙️ Cài đặt")
        self.geometry("600x500")
        self.resizable(False, False)
        
        # Modal
        self.transient(parent)
        self.grab_set()
        
        # Style
        self.configure(fg_color=COLORS['bg_white'])
        
        # Create UI
        self._create_ui()
        
        # Center window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.winfo_screenheight() // 2) - (500 // 2)
        self.geometry(f"+{x}+{y}")
        
        # Bind shortcuts
        self.bind("<Escape>", lambda e: self.destroy())
    
    def _create_ui(self):
        """Create settings UI"""
        # Main container with padding
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=SPACING['xl'], pady=SPACING['xl'])
        
        # Title
        title_label = ctk.CTkLabel(
            main_container,
            text="⚙️ Cài đặt",
            font=FONTS['title'],
            text_color=COLORS['text_primary']
        )
        title_label.pack(pady=(0, SPACING['xl']))
        
        # Scrollable frame for settings sections
        scrollable_frame = ctk.CTkScrollableFrame(
            main_container,
            fg_color=COLORS['bg_white'],
            corner_radius=SIZES['radius_md']
        )
        scrollable_frame.pack(fill="both", expand=True)
        
        # Import/Export Section
        self._create_import_export_section(scrollable_frame)
        
        # App Info Section
        self._create_app_info_section(scrollable_frame)
        
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
    
    def _create_import_export_section(self, parent):
        """Create import/export buttons section"""
        # Section frame
        section_frame = ctk.CTkFrame(
            parent,
            fg_color=COLORS['bg_gray'],
            corner_radius=SIZES['radius_md']
        )
        section_frame.pack(fill="x", pady=(0, SPACING['md']))
        
        # Section title
        section_title = ctk.CTkLabel(
            section_frame,
            text="📦 Nhập/Xuất Dữ liệu",
            font=FONTS['heading'],
            text_color=COLORS['text_primary'],
            anchor="w"
        )
        section_title.pack(fill="x", padx=SPACING['lg'], pady=(SPACING['lg'], SPACING['md']))
        
        # Description
        desc_label = ctk.CTkLabel(
            section_frame,
            text="Sao lưu hoặc khôi phục dữ liệu lịch trình của bạn",
            font=FONTS['small'],
            text_color=COLORS['text_secondary'],
            anchor="w"
        )
        desc_label.pack(fill="x", padx=SPACING['lg'], pady=(0, SPACING['md']))
        
        # Buttons container
        buttons_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=SPACING['lg'], pady=(0, SPACING['lg']))
        
        # JSON buttons row
        json_row = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        json_row.pack(fill="x", pady=(0, SPACING['sm']))
        
        # Export JSON button
        export_json_btn = ctk.CTkButton(
            json_row,
            text="📤 Xuất ra JSON",
            width=260,
            height=45,
            fg_color=COLORS['primary_blue'],
            hover_color=COLORS['primary_blue_hover'],
            text_color=COLORS['text_white'],
            font=FONTS['body'],
            corner_radius=SIZES['radius_md'],
            command=self._export_json
        )
        export_json_btn.pack(side="left", padx=(0, SPACING['sm']))
        
        # Import JSON button
        import_json_btn = ctk.CTkButton(
            json_row,
            text="📥 Nhập từ JSON",
            width=260,
            height=45,
            fg_color=COLORS['success_green'],
            hover_color=COLORS['success_green_hover'],
            text_color=COLORS['text_white'],
            font=FONTS['body'],
            corner_radius=SIZES['radius_md'],
            command=self._import_json
        )
        import_json_btn.pack(side="left")
        
        # ICS buttons row
        ics_row = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        ics_row.pack(fill="x")
        
        # Export ICS button
        export_ics_btn = ctk.CTkButton(
            ics_row,
            text="📤 Xuất ra ICS",
            width=260,
            height=45,
            fg_color=COLORS['primary_blue'],
            hover_color=COLORS['primary_blue_hover'],
            text_color=COLORS['text_white'],
            font=FONTS['body'],
            corner_radius=SIZES['radius_md'],
            command=self._export_ics
        )
        export_ics_btn.pack(side="left", padx=(0, SPACING['sm']))
        
        # Import ICS button
        import_ics_btn = ctk.CTkButton(
            ics_row,
            text="📥 Nhập từ ICS",
            width=260,
            height=45,
            fg_color=COLORS['success_green'],
            hover_color=COLORS['success_green_hover'],
            text_color=COLORS['text_white'],
            font=FONTS['body'],
            corner_radius=SIZES['radius_md'],
            command=self._import_ics
        )
        import_ics_btn.pack(side="left")
    
    def _create_app_info_section(self, parent):
        """Create app information section"""
        # Section frame
        section_frame = ctk.CTkFrame(
            parent,
            fg_color=COLORS['bg_gray'],
            corner_radius=SIZES['radius_md']
        )
        section_frame.pack(fill="x", pady=(0, SPACING['md']))
        
        # Section title
        section_title = ctk.CTkLabel(
            section_frame,
            text="ℹ️ Thông tin ứng dụng",
            font=FONTS['heading'],
            text_color=COLORS['text_primary'],
            anchor="w"
        )
        section_title.pack(fill="x", padx=SPACING['lg'], pady=(SPACING['lg'], SPACING['md']))
        
        # App info
        info_items = [
            ("📱 Tên ứng dụng:", "Trợ Lý Lịch Trình"),
            ("🔢 Phiên bản:", "0.7.0"),
            ("👨‍💻 Phát triển bởi:", "Đồ Án NLP"),
            ("📅 Năm:", "2025")
        ]
        
        for label, value in info_items:
            info_row = ctk.CTkFrame(section_frame, fg_color="transparent")
            info_row.pack(fill="x", padx=SPACING['lg'], pady=(0, SPACING['xs']))
            
            label_widget = ctk.CTkLabel(
                info_row,
                text=label,
                font=FONTS['body'],
                text_color=COLORS['text_secondary'],
                anchor="w",
                width=150
            )
            label_widget.pack(side="left")
            
            value_widget = ctk.CTkLabel(
                info_row,
                text=value,
                font=FONTS['body'],
                text_color=COLORS['text_primary'],
                anchor="w"
            )
            value_widget.pack(side="left", padx=(SPACING['sm'], 0))
        
        # Add padding at bottom
        ctk.CTkFrame(section_frame, fg_color="transparent", height=SPACING['lg']).pack()
    
    # ==================== Import/Export Handlers ====================
    
    def _export_json(self):
        """Export events to JSON file"""
        try:
            file_path = filedialog.asksaveasfilename(
                title="Xuất dữ liệu ra JSON",
                defaultextension=".json",
                filetypes=[
                    ("JSON files", "*.json"),
                    ("All files", "*.*")
                ],
                initialfile="schedule_export.json"
            )
            
            if file_path:
                success = self.controller.handle_export_events('json', file_path)
                if success:
                    messagebox.showinfo(
                        "Thành công",
                        f"✅ Đã xuất dữ liệu ra:\n{file_path}"
                    )
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất JSON:\n{str(e)}")
    
    def _import_json(self):
        """Import events from JSON file"""
        try:
            file_path = filedialog.askopenfilename(
                title="Nhập dữ liệu từ JSON",
                filetypes=[
                    ("JSON files", "*.json"),
                    ("All files", "*.*")
                ]
            )
            
            if file_path:
                # Confirm before import
                confirm = messagebox.askyesno(
                    "Xác nhận",
                    "Nhập dữ liệu sẽ thêm các sự kiện mới vào lịch.\n\nTiếp tục?"
                )
                
                if confirm:
                    success = self.controller.handle_import_events('json', file_path)
                    if success:
                        messagebox.showinfo(
                            "Thành công",
                            f"✅ Đã nhập dữ liệu từ:\n{file_path}"
                        )
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể nhập JSON:\n{str(e)}")
    
    def _export_ics(self):
        """Export events to ICS file"""
        try:
            file_path = filedialog.asksaveasfilename(
                title="Xuất dữ liệu ra ICS",
                defaultextension=".ics",
                filetypes=[
                    ("iCalendar files", "*.ics"),
                    ("All files", "*.*")
                ],
                initialfile="schedule_export.ics"
            )
            
            if file_path:
                success = self.controller.handle_export_events('ics', file_path)
                if success:
                    messagebox.showinfo(
                        "Thành công",
                        f"✅ Đã xuất dữ liệu ra:\n{file_path}\n\n"
                        "File ICS có thể mở bằng Google Calendar, Outlook, Apple Calendar..."
                    )
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất ICS:\n{str(e)}")
    
    def _import_ics(self):
        """Import events from ICS file"""
        try:
            file_path = filedialog.askopenfilename(
                title="Nhập dữ liệu từ ICS",
                filetypes=[
                    ("iCalendar files", "*.ics"),
                    ("All files", "*.*")
                ]
            )
            
            if file_path:
                # Confirm before import
                confirm = messagebox.askyesno(
                    "Xác nhận",
                    "Nhập dữ liệu sẽ thêm các sự kiện mới vào lịch.\n\nTiếp tục?"
                )
                
                if confirm:
                    success = self.controller.handle_import_events('ics', file_path)
                    if success:
                        messagebox.showinfo(
                            "Thành công",
                            f"✅ Đã nhập dữ liệu từ:\n{file_path}"
                        )
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể nhập ICS:\n{str(e)}")
