"""
Event Dialog Component
Create and Edit Event Dialog with full form
"""
import customtkinter as ctk
from datetime import date, datetime, time
from typing import Optional, Callable
from tkinter import messagebox
from app.config import COLORS, FONTS, SPACING
from app.models import Event


class EventDialog(ctk.CTkToplevel):
    """
    Event creation/editing dialog
    Shows form for all event fields with validation
    """
    
    def __init__(self, parent, controller, event: Optional[Event] = None, initial_date: Optional[date] = None):
        """
        Initialize event dialog
        
        Args:
            parent: Parent window
            controller: MainController instance
            event: Event object for editing (None for creating new)
            initial_date: Pre-selected date for new events
        """
        super().__init__(parent)
        
        self.controller = controller
        self.event = event
        self.selected_date = initial_date or date.today()
        self.result = None
        
        # Dialog configuration
        is_edit = event is not None
        self.title("Chỉnh sửa sự kiện" if is_edit else "Tạo sự kiện mới")
        self.geometry("600x750")
        self.resizable(False, False)
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        # Center on parent
        self._center_on_parent(parent)
        
        # Setup UI
        self._setup_ui()
        
        # Populate fields if editing
        if event:
            self._populate_fields(event)
        elif initial_date:
            self.selected_date = initial_date
            self.date_display.configure(text=initial_date.strftime("%d/%m/%Y"))
    
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
        # Scrollable main container
        scroll_container = ctk.CTkScrollableFrame(
            self,
            fg_color='transparent',
            scrollbar_button_color=COLORS['primary_blue']
        )
        scroll_container.pack(fill='both', expand=True, padx=SPACING['md'], pady=SPACING['md'])
        
        # Content container
        container = ctk.CTkFrame(scroll_container, fg_color='transparent')
        container.pack(fill='both', expand=True, padx=SPACING['sm'])
        
        # Title
        title_text = "Chỉnh sửa sự kiện" if self.event else "Tạo sự kiện mới"
        title_label = ctk.CTkLabel(
            container,
            text=title_text,
            font=FONTS['heading'],
            text_color=COLORS['text_primary']
        )
        title_label.pack(pady=(0, SPACING['lg']))
        
        # NLP Input Section (for new events)
        if not self.event:
            self._create_nlp_input(container)
            
            # Separator
            separator = ctk.CTkFrame(container, height=2, fg_color=COLORS['border_light'])
            separator.pack(fill='x', pady=SPACING['md'])
            
            ctk.CTkLabel(
                container,
                text="Hoặc nhập thủ công:",
                font=FONTS['caption'],
                text_color=COLORS['text_secondary']
            ).pack(pady=(0, SPACING['sm']))
        
        # Form fields
        self._create_form_fields(container)
        
        # Buttons
        self._create_buttons(container)
    
    def _create_nlp_input(self, parent):
        """Create NLP input section"""
        # NLP Label with icon
        nlp_label = ctk.CTkLabel(
            parent,
            text="🤖 Nhập bằng tiếng Việt tự nhiên",
            font=FONTS['body_bold'],
            text_color=COLORS['primary_blue']
        )
        nlp_label.pack(pady=(0, SPACING['xs']))
        
        # Example text
        example = ctk.CTkLabel(
            parent,
            text='Ví dụ: "Tập gym 18h hôm nay ở California Fitness"',
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        )
        example.pack(pady=(0, SPACING['sm']))
        
        # NLP Input frame
        nlp_frame = ctk.CTkFrame(parent, fg_color='transparent')
        nlp_frame.pack(fill='x', pady=(0, SPACING['sm']))
        
        # NLP text input
        self.nlp_entry = ctk.CTkEntry(
            nlp_frame,
            height=40,
            font=FONTS['body'],
            placeholder_text="Nhập câu mô tả sự kiện..."
        )
        self.nlp_entry.pack(side='left', fill='x', expand=True, padx=(0, SPACING['sm']))
        
        # Parse button
        parse_btn = ctk.CTkButton(
            nlp_frame,
            text="✨ Phân tích",
            width=100,
            height=40,
            fg_color=COLORS['primary_blue'],
            command=self._parse_nlp_input
        )
        parse_btn.pack(side='left')
        
        # Bind Enter key
        self.nlp_entry.bind('<Return>', lambda e: self._parse_nlp_input())
    
    def _parse_nlp_input(self):
        """Parse NLP input and fill form fields"""
        nlp_text = self.nlp_entry.get().strip()
        if not nlp_text:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập câu mô tả sự kiện")
            return
        
        try:
            # Import NLP pipeline
            from core_nlp.pipeline import NLPPipeline
            
            # Parse the input
            nlp = NLPPipeline()
            result = nlp.parse_event(nlp_text)
            
            if not result:
                messagebox.showerror("Lỗi", "Không thể phân tích câu này. Vui lòng thử lại hoặc nhập thủ công.")
                return
            
            # Fill form fields with parsed data
            # Event name
            if result.get('event'):
                self.name_entry.delete(0, 'end')
                self.name_entry.insert(0, result['event'])
            
            # Date and time
            if result.get('start_time'):
                start_dt = result['start_time']
                self.selected_date = start_dt.date()
                self.date_display.configure(text=start_dt.strftime("%d/%m/%Y"))
                self.start_hour_var.set(f"{start_dt.hour:02d}")
                self.start_minute_var.set(f"{start_dt.minute:02d}")
            
            if result.get('end_time'):
                end_dt = result['end_time']
                # Validate end time is after start time
                if result.get('start_time') and end_dt > result['start_time']:
                    self.end_hour_var.set(f"{end_dt.hour:02d}")
                    self.end_minute_var.set(f"{end_dt.minute:02d}")
                else:
                    # Default to 1 hour after start if invalid
                    start_dt = result['start_time']
                    end_hour = (start_dt.hour + 1) % 24
                    self.end_hour_var.set(f"{end_hour:02d}")
                    self.end_minute_var.set(f"{start_dt.minute:02d}")
            
            # Category (from auto-detection)
            if result.get('category'):
                # Map Vietnamese categories to display names
                category_map = {
                    'họp': 'Công việc',
                    'khám': 'Sức khỏe',
                    'ăn': 'Ăn uống',
                    'học': 'Học tập',
                    'thể thao': 'Thể thao',
                    'giải trí': 'Giải trí'
                }
                category_display = category_map.get(result['category'], 'Công việc')
                self.category_var.set(category_display)
            
            # Reminder minutes
            if result.get('reminder_minutes', 0) > 0:
                self.reminder_var.set(str(result['reminder_minutes']))
            
            # Location in description
            if result.get('location'):
                self.desc_text.delete("1.0", "end")
                self.desc_text.insert("1.0", f"Địa điểm: {result['location']}")
            
            # Show success message
            messagebox.showinfo(
                "Thành công", 
                "✅ Đã phân tích thành công!\n\n"
                f"📌 Sự kiện: {result.get('event', 'N/A')}\n"
                f"📅 Ngày: {self.selected_date.strftime('%d/%m/%Y')}\n"
                f"⏰ Thời gian: {self.start_hour_var.get()}:{self.start_minute_var.get()} - {self.end_hour_var.get()}:{self.end_minute_var.get()}\n"
                f"📂 Danh mục: {self.category_var.get()}\n\n"
                "Kiểm tra và chỉnh sửa nếu cần, sau đó nhấn 'Tạo sự kiện'."
            )
            
            # Clear NLP input after successful parsing
            self.nlp_entry.delete(0, 'end')
            
        except Exception as e:
            import traceback
            print(f"Error parsing NLP input: {e}")
            print(traceback.format_exc())
            messagebox.showerror("Lỗi", f"Lỗi phân tích: {str(e)}\nVui lòng nhập thủ công.")
    
    def _create_form_fields(self, parent):
        """Create form input fields"""
        # Event Name
        self._create_field_label(parent, "Tên sự kiện *")
        self.name_entry = ctk.CTkEntry(
            parent,
            height=40,
            font=FONTS['body'],
            placeholder_text="Nhập tên sự kiện..."
        )
        self.name_entry.pack(fill='x', pady=(0, SPACING['md']))
        
        # Date
        self._create_field_label(parent, "Ngày *")
        date_frame = ctk.CTkFrame(parent, fg_color='transparent')
        date_frame.pack(fill='x', pady=(0, SPACING['md']))
        
        self.date_display = ctk.CTkLabel(
            date_frame,
            text=self.selected_date.strftime("%d/%m/%Y"),
            font=FONTS['body'],
            text_color=COLORS['text_primary'],
            anchor='w',
            width=200
        )
        self.date_display.pack(side='left', padx=(0, SPACING['sm']))
        
        date_button = ctk.CTkButton(
            date_frame,
            text="📅 Chọn ngày",
            width=120,
            height=32,
            command=self._show_date_picker
        )
        date_button.pack(side='left')
        
        # Time section
        time_container = ctk.CTkFrame(parent, fg_color='transparent')
        time_container.pack(fill='x', pady=(0, SPACING['md']))
        
        # Start time
        start_frame = ctk.CTkFrame(time_container, fg_color='transparent')
        start_frame.pack(side='left', fill='both', expand=True, padx=(0, SPACING['sm']))
        
        self._create_field_label(start_frame, "Giờ bắt đầu *")
        self.start_hour_var = ctk.StringVar(value="09")
        self.start_minute_var = ctk.StringVar(value="00")
        
        start_time_frame = ctk.CTkFrame(start_frame, fg_color='transparent')
        start_time_frame.pack(fill='x')
        
        self.start_hour_menu = ctk.CTkOptionMenu(
            start_time_frame,
            variable=self.start_hour_var,
            values=[f"{h:02d}" for h in range(24)],
            width=80,
            height=36
        )
        self.start_hour_menu.pack(side='left', padx=(0, SPACING['xs']))
        
        ctk.CTkLabel(start_time_frame, text=":", font=FONTS['body']).pack(side='left', padx=2)
        
        self.start_minute_menu = ctk.CTkOptionMenu(
            start_time_frame,
            variable=self.start_minute_var,
            values=[f"{m:02d}" for m in range(0, 60, 1)],  # All minutes 00-59
            width=80,
            height=36
        )
        self.start_minute_menu.pack(side='left', padx=(SPACING['xs'], 0))
        
        # End time
        end_frame = ctk.CTkFrame(time_container, fg_color='transparent')
        end_frame.pack(side='left', fill='both', expand=True)
        
        self._create_field_label(end_frame, "Giờ kết thúc *")
        self.end_hour_var = ctk.StringVar(value="10")
        self.end_minute_var = ctk.StringVar(value="00")
        
        end_time_frame = ctk.CTkFrame(end_frame, fg_color='transparent')
        end_time_frame.pack(fill='x')
        
        self.end_hour_menu = ctk.CTkOptionMenu(
            end_time_frame,
            variable=self.end_hour_var,
            values=[f"{h:02d}" for h in range(24)],
            width=80,
            height=36
        )
        self.end_hour_menu.pack(side='left', padx=(0, SPACING['xs']))
        
        ctk.CTkLabel(end_time_frame, text=":", font=FONTS['body']).pack(side='left', padx=2)
        
        self.end_minute_menu = ctk.CTkOptionMenu(
            end_time_frame,
            variable=self.end_minute_var,
            values=[f"{m:02d}" for m in range(0, 60, 1)],  # All minutes 00-59
            width=80,
            height=36
        )
        self.end_minute_menu.pack(side='left', padx=(SPACING['xs'], 0))
        
        # Category
        self._create_field_label(parent, "Danh mục")
        self.category_var = ctk.StringVar(value="Công việc")
        categories = ["Công việc", "Sức khỏe", "Ăn uống", "Học tập", "Thể thao", "Giải trí"]
        
        self.category_menu = ctk.CTkOptionMenu(
            parent,
            variable=self.category_var,
            values=categories,
            height=36
        )
        self.category_menu.pack(fill='x', pady=(0, SPACING['md']))
        
        # Reminder
        self._create_field_label(parent, "Nhắc nhở")
        
        # Reminder container
        reminder_container = ctk.CTkFrame(parent, fg_color='transparent')
        reminder_container.pack(fill='x', pady=(0, SPACING['md']))
        
        self.reminder_var = ctk.StringVar(value="0")
        self.reminder_buttons = {}  # Store button references
        self.selected_reminder = "0"  # Track selected reminder
        
        # Row 1: Quick presets
        reminder_row1 = ctk.CTkFrame(reminder_container, fg_color='transparent')
        reminder_row1.pack(fill='x', pady=(0, SPACING['xs']))
        
        quick_reminders = [
            ("Không", "0"),
            ("5 phút", "5"),
            ("15 phút", "15"),
            ("30 phút", "30"),
            ("1 giờ", "60")
        ]
        
        for label, value in quick_reminders:
            btn = ctk.CTkButton(
                reminder_row1,
                text=label,
                width=85,
                height=34,
                fg_color=COLORS['primary_blue'] if value == "0" else COLORS['bg_gray'],
                text_color='white' if value == "0" else COLORS['text_primary'],
                hover_color=COLORS['primary_blue_hover'] if value == "0" else COLORS['border_light'],
                font=FONTS['body'],
                corner_radius=6,
                command=lambda v=value, l=label: self._select_reminder(v, l)
            )
            btn.pack(side='left', padx=(0, SPACING['xs']))
            self.reminder_buttons[value] = btn
        
        # Row 2: Extended options
        reminder_row2 = ctk.CTkFrame(reminder_container, fg_color='transparent')
        reminder_row2.pack(fill='x', pady=(0, SPACING['xs']))
        
        extended_reminders = [
            ("2 giờ", "120"),
            ("1 ngày", "1440"),
            ("1 tuần", "10080"),
            ("📅 Tùy chỉnh", "custom")
        ]
        
        for label, value in extended_reminders:
            btn = ctk.CTkButton(
                reminder_row2,
                text=label,
                width=85,
                height=34,
                fg_color=COLORS['bg_gray'],
                text_color=COLORS['text_primary'],
                hover_color=COLORS['border_light'],
                font=FONTS['body'],
                corner_radius=6,
                command=lambda v=value, l=label: self._select_reminder(v, l)
            )
            btn.pack(side='left', padx=(0, SPACING['xs']))
            self.reminder_buttons[value] = btn
        
        # Custom reminder input frame (hidden by default)
        self.custom_reminder_frame = ctk.CTkFrame(reminder_container, fg_color=COLORS['bg_gray'], corner_radius=6)
        self.custom_reminder_frame.pack(fill='x', pady=(SPACING['xs'], 0))
        self.custom_reminder_frame.pack_forget()  # Initially hidden
        
        # Custom input row
        custom_input_row = ctk.CTkFrame(self.custom_reminder_frame, fg_color='transparent')
        custom_input_row.pack(fill='x', padx=SPACING['sm'], pady=SPACING['sm'])
        
        ctk.CTkLabel(
            custom_input_row,
            text="Nhắc trước:",
            font=FONTS['body'],
            text_color=COLORS['text_primary']
        ).pack(side='left', padx=(0, SPACING['xs']))
        
        self.reminder_entry = ctk.CTkEntry(
            custom_input_row,
            textvariable=self.reminder_var,
            width=80,
            height=32,
            font=FONTS['body'],
            placeholder_text="Số"
        )
        self.reminder_entry.pack(side='left', padx=(0, SPACING['xs']))
        
        # Unit selector
        self.reminder_unit_var = ctk.StringVar(value="phút")
        reminder_unit_menu = ctk.CTkOptionMenu(
            custom_input_row,
            variable=self.reminder_unit_var,
            values=["phút", "giờ", "ngày"],
            width=80,
            height=32,
            font=FONTS['body']
        )
        reminder_unit_menu.pack(side='left', padx=(0, SPACING['xs']))
        
        # Apply button
        apply_btn = ctk.CTkButton(
            custom_input_row,
            text="✓ Áp dụng",
            width=90,
            height=32,
            fg_color=COLORS['primary_blue'],
            text_color='white',
            font=FONTS['body'],
            command=self._apply_custom_reminder
        )
        apply_btn.pack(side='left')
        
        # Description
        self._create_field_label(parent, "Mô tả")
        self.desc_text = ctk.CTkTextbox(
            parent,
            height=100,
            font=FONTS['body']
        )
        self.desc_text.pack(fill='both', expand=True, pady=(0, SPACING['md']))
    
    def _select_reminder(self, value: str, label: str):
        """
        Handle reminder button selection
        
        Args:
            value: Reminder value (minutes or 'custom')
            label: Button label text
        """
        # Reset all buttons to default color
        for btn_value, btn in self.reminder_buttons.items():
            btn.configure(
                fg_color=COLORS['bg_gray'],
                text_color=COLORS['text_primary'],
                hover_color=COLORS['border_light']
            )
        
        # Highlight selected button
        if value in self.reminder_buttons:
            self.reminder_buttons[value].configure(
                fg_color=COLORS['primary_blue'],
                text_color='white',
                hover_color=COLORS['primary_blue_hover']
            )
        
        self.selected_reminder = value
        
        if value == "custom":
            # Show custom input frame
            self.custom_reminder_frame.pack(fill='x', pady=(SPACING['xs'], 0))
            self.reminder_entry.focus()
        else:
            # Hide custom input frame
            self.custom_reminder_frame.pack_forget()
            # Set reminder value
            self.reminder_var.set(value)
    
    def _apply_custom_reminder(self):
        """Apply custom reminder value"""
        try:
            amount = int(self.reminder_entry.get())
            unit = self.reminder_unit_var.get()
            
            # Convert to minutes
            if unit == "giờ":
                minutes = amount * 60
            elif unit == "ngày":
                minutes = amount * 1440
            else:  # phút
                minutes = amount
            
            # Validate
            if minutes < 0:
                messagebox.showwarning("Cảnh báo", "Thời gian nhắc nhở phải là số dương")
                return
            
            if minutes > 43200:  # Max 30 days
                messagebox.showwarning("Cảnh báo", "Thời gian nhắc nhở tối đa là 30 ngày (43,200 phút)")
                return
            
            # Update reminder value
            self.reminder_var.set(str(minutes))
            
            # Update custom button text to show applied value
            self.reminder_buttons["custom"].configure(
                text=f"📅 {amount} {unit}"
            )
            
            # Keep custom button highlighted
            self._select_reminder("custom", f"{amount} {unit}")
            
            messagebox.showinfo("Thành công", f"✅ Đã đặt nhắc nhở trước {amount} {unit}")
            
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ")
    
    def _create_field_label(self, parent, text: str):
        """Create form field label"""
        label = ctk.CTkLabel(
            parent,
            text=text,
            font=FONTS['body'],
            text_color=COLORS['text_secondary'],
            anchor='w'
        )
        label.pack(fill='x', pady=(0, SPACING['xs']))
    
    def _create_buttons(self, parent):
        """Create action buttons"""
        button_frame = ctk.CTkFrame(parent, fg_color='transparent')
        button_frame.pack(fill='x', pady=(SPACING['lg'], 0))
        
        # Delete button (left side, only for edit mode)
        if self.event:
            delete_btn = ctk.CTkButton(
                button_frame,
                text="🗑️ Xóa",
                width=100,
                height=44,
                fg_color=COLORS['error'],
                text_color='white',
                hover_color="#b71c1c",
                font=FONTS['body'],
                corner_radius=6,
                command=self._delete_event
            )
            delete_btn.pack(side='left')
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="❌ Hủy",
            width=140,
            height=44,
            fg_color=COLORS['bg_gray'],
            text_color=COLORS['text_primary'],
            hover_color=COLORS['border_light'],
            font=FONTS['body'],
            command=self._cancel
        )
        cancel_btn.pack(side='right', padx=(SPACING['sm'], 0))
        
        # Save button with prominent styling
        save_text = "✅ Cập nhật sự kiện" if self.event else "✅ Tạo sự kiện"
        save_btn = ctk.CTkButton(
            button_frame,
            text=save_text,
            width=180,
            height=44,
            fg_color=COLORS['primary_blue'],
            hover_color="#1E5A8E",
            font=FONTS['body_bold'],
            command=self._save
        )
        save_btn.pack(side='right')
        
        # Bind Enter key to save (when not in text area)
        self.bind('<Return>', lambda e: self._save() if not self.desc_text.focus_get() == self.desc_text else None)
    
    def _delete_event(self):
        """Handle delete event button"""
        if self.event and self.controller:
            self.destroy()  # Close edit dialog first
            self.controller.show_delete_confirm_dialog(self.event.id)
    
    def _show_date_picker(self):
        """Show interactive calendar date picker"""
        from app.views.dialogs.date_picker_dialog import DatePickerDialog
        
        # Open date picker dialog
        picker = DatePickerDialog(self, initial_date=self.selected_date)
        picker.wait_window()
        
        # Get selected date
        result = picker.get_result()
        if result:
            self.selected_date = result
            self.date_display.configure(text=result.strftime("%d/%m/%Y"))
    
    def _populate_fields(self, event: Event):
        """Populate form fields with event data"""
        # Name
        self.name_entry.insert(0, event.event_name)
        
        # Date and Time (from datetime)
        if event.start_time:
            self.selected_date = event.start_time.date()
            self.date_display.configure(text=event.start_time.date().strftime("%d/%m/%Y"))
            self.start_hour_var.set(f"{event.start_time.hour:02d}")
            self.start_minute_var.set(f"{event.start_time.minute:02d}")
        
        # End time
        if event.end_time:
            self.end_hour_var.set(f"{event.end_time.hour:02d}")
            self.end_minute_var.set(f"{event.end_time.minute:02d}")
        
        # Category
        if event.category:
            self.category_var.set(event.category)
        
        # Location (if available)
        if hasattr(event, 'location') and event.location:
            # TODO: Add location field to dialog
            pass
    
    def _validate_inputs(self) -> bool:
        """Validate form inputs"""
        # Check event name
        if not self.name_entry.get().strip():
            messagebox.showerror("Lỗi", "Vui lòng nhập tên sự kiện")
            self.name_entry.focus()
            return False
        
        # No need to validate end_time - it's optional now
        # User can leave end time as default or modify it
        
        return True
    
    def _save(self):
        """Save event"""
        # Validate inputs
        if not self._validate_inputs():
            return
        
        # Build datetime objects from date + time
        start_datetime = datetime.combine(
            self.selected_date,
            time(int(self.start_hour_var.get()), int(self.start_minute_var.get()))
        )
        
        # End time is optional - only set if provided and valid
        end_datetime = None
        try:
            end_hour = int(self.end_hour_var.get())
            end_minute = int(self.end_minute_var.get())
            end_time_temp = datetime.combine(
                self.selected_date,
                time(end_hour, end_minute)
            )
            # Only use end_time if it's after start_time
            if end_time_temp > start_datetime:
                end_datetime = end_time_temp
            else:
                # Default to 1 hour after start
                from datetime import timedelta
                end_datetime = start_datetime + timedelta(hours=1)
        except:
            # Default to 1 hour after start if any error
            from datetime import timedelta
            end_datetime = start_datetime + timedelta(hours=1)
        
        # Get reminder minutes (validate 0-43200, max 30 days)
        try:
            reminder_minutes = int(self.reminder_var.get())
            if reminder_minutes < 0:
                reminder_minutes = 0
            elif reminder_minutes > 43200:  # 30 days max
                reminder_minutes = 43200
        except ValueError:
            reminder_minutes = 0
        
        # Build event data
        event_data = {
            'event_name': self.name_entry.get().strip(),
            'start_time': start_datetime,
            'end_time': end_datetime,
            'category': self.category_var.get(),
            'location': '',
            'reminder_minutes': reminder_minutes,
            'status': 'pending'
        }
        
        # Call controller
        try:
            if self.event:
                # Update existing event
                success = self.controller.handle_update_event(self.event.id, event_data)
                if success:
                    messagebox.showinfo("Thành công", "✅ Đã cập nhật sự kiện thành công!")
                    self.result = 'updated'
                    self.destroy()
                else:
                    messagebox.showerror("Lỗi", "❌ Không thể cập nhật sự kiện. Vui lòng thử lại.")
            else:
                # Create new event
                success = self.controller.handle_create_event(event_data)
                if success:
                    messagebox.showinfo("Thành công", "✅ Đã tạo sự kiện thành công!")
                    self.result = 'created'
                    self.destroy()
                else:
                    messagebox.showerror("Lỗi", "❌ Không thể tạo sự kiện. Vui lòng kiểm tra lại thông tin.")
        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            print(f"[ERROR] Save event failed: {error_detail}")
            messagebox.showerror("Lỗi", f"❌ Lỗi khi lưu sự kiện:\n{str(e)}\n\nVui lòng kiểm tra console để biết chi tiết.")
    
    def _cancel(self):
        """Cancel and close dialog"""
        self.result = 'cancelled'
        self.destroy()
