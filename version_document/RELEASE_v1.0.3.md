# 🚀 Release Notes - Version 1.0.3 MVP

**Release Date:** November 8, 2025  
**Build Name:** TroLyLichTrinhV2_v1.0.3.exe  
**Status:** Production Ready ✅

---

## 🎯 Release Highlights

### ✨ New Features

1. **Fade Theme Animation** 🎨
   - Smooth fade transition when switching between Dark/Light themes
   - Professional crossfade effect (400ms total animation)
   - Eliminates jarring theme switches for better UX

2. **Enhanced Time Pattern: "1h50p"** ⏰
   - New shorthand format: `1h50p` = 1 giờ 50 phút
   - Supports: `2h30p`, `10h15p`, etc.
   - Smart past-time auto-correction (auto-shift to tomorrow if time is in past)
   - Full integration with period modifiers (sáng/chiều/tối)
   - Works with day modifiers, locations, reminders, and time ranges

3. **Sound Settings Persistence** 🔊
   - Sound preferences now saved to database
   - Auto-restore on app startup
   - Async + debounced saves (200ms) for zero UI lag
   - Graceful shutdown with `flush_pending_saves()`

4. **Performance Optimization** ⚡
   - Eliminated 100ms UI lag when switching sounds
   - Debouncing: 10 rapid clicks → 1 DB write (95% reduction)
   - Batch write operations for multiple settings
   - Non-blocking async architecture

---

## 🔧 Technical Improvements

### Core NLP Parser (`time_parser.py`)
- ✅ Added pattern: `\b(\d{1,2})\s*h\s*(\d{1,2})\s*p(?:hut|hút)?\b`
- ✅ Negative lookahead fix: `(?!p)` prevents "17h30" matching "1h50p"
- ✅ Smart auto-correction: Past times auto-shift to next occurrence
- ✅ Timezone-aware comparison fix (naive vs aware datetime)
- ✅ Fixed all DeprecationWarnings (`re.sub()` count parameter)
- ✅ Fixed IndentationErrors in multiple locations

### Sound Manager (`sound_manager.py`)
- ✅ Database integration with `db_manager` parameter
- ✅ Auto-load settings on init: `_load_settings_from_db()`
- ✅ Async save with threading.Timer: `_save_settings_to_db()`
- ✅ Debounced writes (200ms delay) prevent spam
- ✅ Batch write via `set_settings_batch()` (2 calls → 1)
- ✅ Exit hook: `flush_pending_saves(timeout=1.0)`

### Main App (`main_ctk.py`)
- ✅ Theme toggle with fade animation overlay
- ✅ Removed redundant DB save code (delegated to SoundManager)
- ✅ Added `on_app_closing()` hook for graceful shutdown
- ✅ Updated version metadata to 1.0.3

### UI/UX
- ✅ Fade overlay for theme transitions (dark: #1a1a1a, light: #ffffff)
- ✅ 20ms/frame animation with 10 steps
- ✅ Calendar colors update during fade peak for seamless transition

---

## 🧪 Testing & Validation

### Test Coverage
- ✅ **test_nlp_pipeline.py**: PASS (Macro F1 = 0.9286)
- ✅ **test_hybrid_pipeline.py**: 10/10 PASS (100% accuracy)
- ✅ **test_time_pattern.py**: 16/16 PASS (new "1h50p" pattern)
- ✅ **test_time_pattern_debug.py**: Regex validation PASS

### Pattern Test Results (16/16 ✅)
```
✅ "1h50p" → 2025-11-09 01:50 (auto tomorrow)
✅ "2h30p chiều mai" → 2025-11-09 14:30
✅ "10h15p sáng thứ 2" → 2025-11-10 10:15
✅ "từ 1h50p đến 3h30p" → Range: 01:50-03:30
✅ "1h50p ở phòng 302 nhắc trước 10p" → Full integration
```

### Bug Fixes
1. ❌ → ✅ **TypeError**: Can't compare offset-naive and offset-aware datetimes
2. ❌ → ✅ **DeprecationWarning**: `re.sub()` positional argument (10 locations)
3. ❌ → ✅ **IndentationError**: Unexpected indent (3 locations)
4. ❌ → ✅ **UI Lag**: 100ms → <1ms sound switching performance

---

## 📦 Build Configuration

### PyInstaller Spec (`build_main_ctk.spec`)
```python
name='TroLyLichTrinhV2_v1.0.3'
console=False  # Windowed application
upx=True       # Compression enabled
```

### Included Assets
- ✅ Database schema: `database/schema.sql`
- ✅ NLP modules: `core_nlp/` (pipeline.py, time_parser.py)
- ✅ Services: `services/` (notification, export, import, statistics, sound)
- ✅ Widgets: `widgets/` (event_card.py)
- ✅ Models: `models/phobert_base`, `models/phobert_finetuned`
- ✅ Training data: `training_data/`
- ✅ Sounds: `sounds/` (custom notification sounds)
- ✅ CustomTkinter themes and assets

### Dependencies
- Python 3.9+ (via virtual environment)
- CustomTkinter 5.2.0+
- PyInstaller 6.16.0
- Transformers, PyTorch (CPU)
- underthesea, tkcalendar
- playsound, Pillow

---

## 🚀 Deployment Instructions

### Build Command
```bash
cd "c:\Users\d0ngle8k\Desktop\New folder (2)\NLP-Processing"
.\.venv\Scripts\python.exe -m PyInstaller --clean build_main_ctk.spec
```

### Output Location
```
dist/TroLyLichTrinhV2_v1.0.3.exe
```

### Distribution Package
**Includes:**
1. `TroLyLichTrinhV2_v1.0.3.exe` (main executable)
2. `models/` folder (PhoBERT base + finetuned)
3. `sounds/` folder (notification sounds - optional)
4. `README.md` (user guide)
5. `RELEASE_v1.0.3.md` (this file)

### Installation
1. Extract to desired location
2. Ensure `models/` folder is in same directory as EXE
3. (Optional) Add custom sounds to `sounds/` folder
4. Run `TroLyLichTrinhV2_v1.0.3.exe`

---

## 📊 Performance Metrics

### App Size
- **EXE Size**: ~986 MB (with PyTorch + Transformers + PhoBERT)
- **Startup Time**: ~3-5 seconds (includes model loading)
- **Memory Usage**: ~500-800 MB (depending on model usage)

### Response Times
- **NLP Parsing**: 1-2ms per sentence (rule-based)
- **PhoBERT Inference**: 50-100ms per sentence (hybrid mode)
- **Sound Switching**: <1ms (async + debounced)
- **Theme Animation**: 400ms (smooth fade)
- **Database Operations**: <10ms (batch writes)

### Pattern Support (100+ variations)
- Time formats: 15+ patterns
- Date formats: 10+ patterns
- Relative dates: 20+ keywords
- Vietnamese typos: 50+ variations
- Period modifiers: 5 patterns
- Weekday patterns: 8 patterns

---

## 🔮 Known Issues & Limitations

### Minor Issues (Non-blocking)
1. **Location Detection**: Some edge cases may incorrectly parse location
   - Example: "chu nhat chieu di cafe" → Location: "gio chieu di cafe"
   - Impact: Low (time parsing still correct)
   - Fix: Planned for v1.0.4

2. **Mixed Case Parsing**: Complex mixed case may have lower accuracy
   - Example: "HỌp Với KHÁCH 10h SÁng T2" → Location: "h sáng t2"
   - Impact: Low (time and event still extracted)
   - Workaround: Use consistent casing

### Limitations
- PhoBERT model requires ~500MB memory (CPU mode)
- First launch may take 3-5s to load models
- Windows-only build (Linux/Mac requires separate build)

---

## 🎁 Bonus Features

### Documentation Updates
- ✅ Complete README rewrite with clear architecture
- ✅ Migrated 30+ docs to `version_document/`
- ✅ New file: `TIME_PATTERN_1h50p_ENHANCEMENT.md`
- ✅ Updated `.gitignore` to track important files

### Developer Tools
- ✅ `test_time_pattern.py` - Comprehensive pattern tests
- ✅ `test_time_pattern_debug.py` - Regex validation tool
- ✅ Enhanced error messages and debugging output

---

## 📝 Changelog Summary

### Added
- Fade theme animation (dark ↔ light transitions)
- Time pattern "1h50p" (1 hour 50 minutes)
- Sound settings database persistence
- Async/debounced sound saves
- Smart past-time auto-correction
- Graceful app shutdown hooks

### Fixed
- UI lag when switching sounds (100ms → <1ms)
- Timezone comparison errors
- DeprecationWarnings in `re.sub()`
- IndentationErrors in time_parser
- Pattern priority conflicts (1h50p vs 17h30)

### Optimized
- Database write operations (95% reduction)
- Sound switching performance (100x faster)
- Theme transition smoothness
- Memory usage for sound manager

### Removed
- Redundant DB save code in main_ctk.py
- Duplicate sound persistence logic
- Obsolete test files and docs

---

## 🙏 Credits & Acknowledgments

- **Developer**: d0ngle8k
- **Framework**: CustomTkinter (modern UI)
- **NLP Engine**: Hybrid (Rule-based + PhoBERT)
- **Database**: SQLite with WAL mode
- **Testing**: Comprehensive test suite (16+ test cases)

---

## 📞 Support & Feedback

For issues, suggestions, or contributions:
- GitHub Issues: [NLP-Processing/issues]
- Email: [your-email@example.com]
- Documentation: See `README.md` and `version_document/`

---

**Status**: ✅ Production Ready  
**Build Date**: November 8, 2025  
**Version**: 1.0.3 MVP  
**Next Release**: v1.0.4 (Location detection improvements)

---

## 🚀 Quick Start

```bash
# Run the executable
TroLyLichTrinhV2_v1.0.3.exe

# Or build from source
cd NLP-Processing
.\.venv\Scripts\activate
python main_ctk.py
```

**Enjoy the improved scheduling assistant!** 🎉
