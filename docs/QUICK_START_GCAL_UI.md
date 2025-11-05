# 🚀 Quick Start Guide - Google Calendar UI Implementation

**For**: Development Team  
**Version**: v0.7.0 (Google Calendar UI)  
**Framework**: CustomTkinter  
**Pattern**: MVC (Model-View-Controller)

---

## ⚡ Quick Commands

```bash
# 1. Install CustomTkinter
pip install customtkinter

# 2. Create feature branch
git checkout -b feature/google-calendar-ui

# 3. Run current app (for reference)
python main.py

# 4. Create prototype
python prototype_gcal_ui.py
```

---

## 📦 Dependencies to Add

```txt
# Add to requirements.txt
customtkinter>=5.2.0
pillow>=10.0.0  # For icons
```

---

## 🎨 Color Constants (Copy-Paste Ready)

```python
# app/config.py
COLORS = {
    # Google Calendar Colors
    "primary_blue": "#1a73e8",
    "primary_blue_hover": "#1557b0",
    "primary_blue_light": "#e8f0fe",
    
    "bg_white": "#ffffff",
    "bg_gray": "#f1f3f4",
    "bg_gray_hover": "#e8eaed",
    
    "text_primary": "#3c4043",
    "text_secondary": "#5f6368",
    "text_disabled": "#80868b",
    
    "border_light": "#dadce0",
    "border_focus": "#1a73e8",
    
    # Event Categories
    "event_work": "#039be5",
    "event_health": "#7cb342",
    "event_food": "#f6bf26",
    "event_study": "#e67c73",
    "event_sport": "#33b679",
    "event_entertainment": "#8e24aa"
}

FONTS = {
    "title": ("Roboto", 22, "bold"),
    "heading": ("Roboto", 16, "bold"),
    "subheading": ("Roboto", 14, "bold"),
    "body": ("Roboto", 13, "normal"),
    "caption": ("Roboto", 11, "normal")
}

SPACING = {
    "xs": 4,
    "sm": 8,
    "md": 16,
    "lg": 24,
    "xl": 32
}
```

---

## 🏗️ File Structure to Create

```bash
mkdir -p app/{models,views,controllers,utils}
mkdir -p app/views/components
touch app/__init__.py
touch app/config.py
touch app/models/{__init__.py,event.py,calendar_state.py}
touch app/views/{__init__.py,main_window.py,sidebar_view.py,calendar_view.py}
touch app/views/components/{__init__.py,buttons.py,inputs.py}
touch app/controllers/{__init__.py,main_controller.py,event_controller.py}
touch app/utils/{__init__.py,date_utils.py,color_utils.py}
```

---

## 📝 Basic Template: Main Window

```python
# app/views/main_window.py
import customtkinter as ctk
from app.config import COLORS, FONTS, SPACING

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window config
        self.title("Trợ Lý Lịch Trình - v0.7")
        self.geometry("1200x800")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        self._setup_layout()
    
    def _setup_layout(self):
        # Configure grid
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Top bar
        self._create_top_bar()
        
        # Sidebar
        self._create_sidebar()
        
        # Main calendar area
        self._create_calendar_area()
    
    def _create_top_bar(self):
        """Top navigation bar"""
        top_bar = ctk.CTkFrame(
            self, 
            height=60, 
            fg_color=COLORS["bg_white"],
            corner_radius=0
        )
        top_bar.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        # Title
        title = ctk.CTkLabel(
            top_bar,
            text="☰ Trợ Lý Lịch Trình",
            font=FONTS["title"],
            text_color=COLORS["text_primary"]
        )
        title.pack(side="left", padx=SPACING["md"])
        
        # Today button
        today_btn = ctk.CTkButton(
            top_bar,
            text="Today",
            width=80,
            height=36,
            fg_color="transparent",
            text_color=COLORS["text_primary"],
            border_width=1,
            border_color=COLORS["border_light"],
            hover_color=COLORS["bg_gray_hover"]
        )
        today_btn.pack(side="left", padx=SPACING["sm"])
    
    def _create_sidebar(self):
        """Left sidebar"""
        sidebar = ctk.CTkFrame(
            self,
            width=250,
            fg_color=COLORS["bg_gray"],
            corner_radius=0
        )
        sidebar.grid(row=1, column=0, sticky="nsw")
        sidebar.grid_propagate(False)
        
        # Create button
        create_btn = ctk.CTkButton(
            sidebar,
            text="+ Tạo mới",
            width=200,
            height=44,
            fg_color=COLORS["primary_blue"],
            hover_color=COLORS["primary_blue_hover"],
            corner_radius=24,
            font=FONTS["subheading"]
        )
        create_btn.pack(pady=SPACING["md"], padx=SPACING["md"])
    
    def _create_calendar_area(self):
        """Main calendar view area"""
        calendar_area = ctk.CTkFrame(
            self,
            fg_color=COLORS["bg_white"]
        )
        calendar_area.grid(row=1, column=1, sticky="nsew", padx=SPACING["md"], pady=SPACING["md"])
        
        # View switcher
        view_switcher = ctk.CTkSegmentedButton(
            calendar_area,
            values=["Ngày", "Tuần", "Tháng", "Năm"],
            selected_color=COLORS["primary_blue"],
            selected_hover_color=COLORS["primary_blue_hover"]
        )
        view_switcher.pack(pady=SPACING["md"])
        view_switcher.set("Tháng")

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
```

---

## 🧪 Quick Prototype Test

```python
# prototype_gcal_ui.py
import customtkinter as ctk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Google Calendar UI Prototype")
app.geometry("1200x800")

# Test layout
frame = ctk.CTkFrame(app, corner_radius=0)
frame.pack(fill="both", expand=True)

label = ctk.CTkLabel(frame, text="✅ CustomTkinter is working!", font=("Roboto", 24))
label.pack(pady=100)

button = ctk.CTkButton(frame, text="Click Me", width=200, height=50)
button.pack(pady=20)

app.mainloop()
```

---

## 📋 Phase 1 Checklist (Week 1-2)

### Day 1-2: Setup
- [ ] Install CustomTkinter
- [ ] Create file structure
- [ ] Setup config.py with colors/fonts
- [ ] Test basic CTk window

### Day 3-4: Top Bar
- [ ] Create top navigation bar
- [ ] Add hamburger menu icon
- [ ] Add "Today" button
- [ ] Add navigation arrows
- [ ] Add search icon
- [ ] Add settings icon

### Day 5-6: Sidebar
- [ ] Create sidebar frame
- [ ] Add "Create" button
- [ ] Add mini calendar widget
- [ ] Add calendar toggles

### Day 7-8: Main Area
- [ ] Setup grid layout
- [ ] Add view switcher (Day/Week/Month)
- [ ] Create placeholder calendar grid
- [ ] Test responsiveness

### Day 9-10: Polish
- [ ] Fix spacing issues
- [ ] Add hover effects
- [ ] Test color consistency
- [ ] Code review

---

## 🎯 Success Criteria (Phase 1)

- ✅ CustomTkinter integrated
- ✅ Layout matches Google Calendar structure
- ✅ Colors match design spec
- ✅ Fonts are correct
- ✅ Spacing is consistent
- ✅ No crashes or errors
- ✅ Code is clean & documented

---

## 🐛 Common Issues & Solutions

### Issue 1: CustomTkinter not found
```bash
# Solution
pip install --upgrade customtkinter
```

### Issue 2: Fonts not rendering
```python
# Solution: Use system fonts
font = ("Segoe UI", 14)  # Windows
font = ("San Francisco", 14)  # Mac
font = ("Ubuntu", 14)  # Linux
```

### Issue 3: Colors look different
```python
# Solution: Use hex colors, not names
fg_color="#1a73e8"  # ✅ Good
fg_color="blue"     # ❌ Avoid
```

### Issue 4: Layout not responsive
```python
# Solution: Use grid weights
self.grid_rowconfigure(0, weight=1)
self.grid_columnconfigure(0, weight=1)
```

---

## 📚 Resources

### Documentation
- CustomTkinter Docs: https://customtkinter.tomschimansky.com/
- Tkinter Reference: https://docs.python.org/3/library/tkinter.html
- Google Calendar for reference: https://calendar.google.com

### Design Assets
- Google Fonts: https://fonts.google.com/specimen/Roboto
- Material Icons: https://fonts.google.com/icons
- Color Palette Tool: https://coolors.co/

### Code Examples
- CustomTkinter Examples: https://github.com/TomSchimansky/CustomTkinter/tree/master/examples
- MVC Pattern in Python: https://realpython.com/the-model-view-controller-mvc-pattern-and-its-relationship-to-web-development/

---

## 💻 Development Workflow

```bash
# 1. Start feature branch
git checkout -b feature/google-calendar-ui

# 2. Make changes
# ... code here ...

# 3. Test frequently
python app/views/main_window.py

# 4. Commit small changes
git add .
git commit -m "feat: add top navigation bar"

# 5. Push to remote
git push origin feature/google-calendar-ui

# 6. Create PR when phase complete
```

---

## 🔍 Code Review Checklist

Before submitting PR:
- [ ] Code follows PEP 8 style guide
- [ ] All functions have docstrings
- [ ] No hardcoded values (use config.py)
- [ ] Consistent naming conventions
- [ ] No print() statements (use logging)
- [ ] Code is DRY (Don't Repeat Yourself)
- [ ] Components are reusable
- [ ] Layout is responsive

---

## 📞 Support

**Questions?** Check these first:
1. `docs/BA_GOOGLE_CALENDAR_UI_REDESIGN.md` - Full specification
2. `docs/BA_SUMMARY.md` - Executive summary
3. This file - Quick reference

**Still stuck?**
- Create GitHub issue
- Ask in team chat
- Review CustomTkinter examples

---

**Status**: 🚦 **READY TO START**  
**First Task**: Install CustomTkinter and run prototype  
**Timeline**: Phase 1 - 10 days

---

<p align="center"><strong>Happy Coding! 🚀</strong></p>
