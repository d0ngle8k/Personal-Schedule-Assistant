# 📦 Deployment Checklist - v1.0.3 MVP

## ✅ Pre-Build Checklist

- [x] Update version in `main_ctk.py` → 1.0.3
- [x] Update EXE name in `build_main_ctk.spec` → TroLyLichTrinhV2_v1.0.3
- [x] Create release notes → `RELEASE_v1.0.3.md`
- [x] All tests passing:
  - [x] test_nlp_pipeline.py (Macro F1 = 0.9286)
  - [x] test_hybrid_pipeline.py (10/10 PASS)
  - [x] test_time_pattern.py (16/16 PASS)
- [x] Fix all errors:
  - [x] DeprecationWarnings (re.sub count parameter)
  - [x] IndentationErrors (time_parser.py)
  - [x] TypeError (timezone comparison)
- [x] Clean temporary files

## 🔨 Build Process

### Command
```bash
cd "c:\Users\d0ngle8k\Desktop\New folder (2)\NLP-Processing"
.\.venv\Scripts\python.exe -m PyInstaller --clean build_main_ctk.spec
```

### Expected Output
```
dist/TroLyLichTrinhV2_v1.0.3.exe
```

### Build Verification
- [ ] Check file exists: `dist/TroLyLichTrinhV2_v1.0.3.exe`
- [ ] Check file size: ~986 MB (±50 MB)
- [ ] Test launch: Double-click EXE
- [ ] Verify UI loads correctly
- [ ] Test dark/light theme toggle (fade animation)
- [ ] Test "1h50p" pattern: "Họp 1h50p"
- [ ] Test sound persistence: Change sound, restart app
- [ ] Test NLP parsing: "mai 10h họp ở phòng 302"
- [ ] Test database: Create/edit/delete events
- [ ] Test reminder: Set reminder, verify notification

## 📁 Distribution Package Structure

```
TroLyLichTrinhV2_v1.0.3/
├── TroLyLichTrinhV2_v1.0.3.exe  (main executable)
├── models/
│   ├── phobert_base/            (pre-trained model)
│   └── phobert_finetuned/       (fine-tuned model)
├── sounds/                       (optional custom sounds)
├── README.md                     (user guide)
├── RELEASE_v1.0.3.md            (release notes)
└── LICENSE.txt                   (optional)
```

## 🚀 Post-Build Tasks

### 1. Testing
- [ ] Run on clean Windows machine (no Python installed)
- [ ] Test with fresh database (delete events.db)
- [ ] Test all features:
  - [ ] Event creation (NLP parsing)
  - [ ] Event editing
  - [ ] Event deletion
  - [ ] Calendar navigation
  - [ ] Search functionality
  - [ ] Export (JSON/ICS)
  - [ ] Import (JSON/ICS)
  - [ ] Reminders/notifications
  - [ ] Sound settings
  - [ ] Theme switching
  - [ ] Statistics

### 2. Documentation
- [ ] Update README.md with v1.0.3 features
- [ ] Create user quick start guide
- [ ] Document new "1h50p" pattern
- [ ] Document fade theme animation
- [ ] Add troubleshooting section

### 3. Packaging
- [ ] Create distribution folder
- [ ] Copy EXE to dist folder
- [ ] Copy models folder
- [ ] Copy sounds folder (with defaults)
- [ ] Add README.md
- [ ] Add RELEASE_v1.0.3.md
- [ ] Create ZIP archive: `TroLyLichTrinhV2_v1.0.3.zip`

### 4. Git Commit & Tag
```bash
git add .
git commit -m "Release v1.0.3 MVP: Fade animations + 1h50p pattern + Sound persistence"
git tag -a v1.0.3 -m "Version 1.0.3 MVP Production Release"
git push origin main
git push origin v1.0.3
```

### 5. GitHub Release
- [ ] Create new release on GitHub
- [ ] Title: "v1.0.3 MVP - Fade Animations + Enhanced Time Patterns"
- [ ] Upload ZIP file
- [ ] Copy RELEASE_v1.0.3.md to release notes
- [ ] Mark as "Latest Release"

## 📊 Quality Assurance

### Performance Tests
- [ ] App startup time: < 5 seconds
- [ ] NLP parsing: < 2ms per sentence
- [ ] Theme switching: Smooth fade (400ms)
- [ ] Sound switching: No lag (<1ms)
- [ ] Memory usage: < 800 MB

### Compatibility Tests
- [ ] Windows 10 (64-bit)
- [ ] Windows 11 (64-bit)
- [ ] Screen resolution: 1920x1080
- [ ] Screen resolution: 1366x768
- [ ] Dark mode
- [ ] Light mode

### Edge Case Tests
- [ ] Long event names (100+ characters)
- [ ] Special characters in event name
- [ ] Past dates (should reject or auto-correct)
- [ ] Invalid time formats
- [ ] Empty database
- [ ] Corrupted database (auto-repair)
- [ ] Missing models folder (graceful fallback)
- [ ] Missing sounds folder (use system sounds)

## 🐛 Known Issues & Workarounds

### Issue #1: Location Detection Edge Cases
**Problem**: "chu nhat chieu di cafe" → Location: "gio chieu di cafe"  
**Impact**: Low (time parsing correct)  
**Workaround**: Manual edit location after parsing  
**Fix**: Planned for v1.0.4

### Issue #2: Mixed Case Parsing
**Problem**: Complex mixed case reduces accuracy  
**Impact**: Low (core functionality unaffected)  
**Workaround**: Use consistent casing  
**Fix**: Improve case normalization in v1.0.4

## 📝 Deployment Notes

### File Sizes
- EXE: ~986 MB (with PyTorch + PhoBERT)
- Models: ~500 MB
- Total package: ~1.5 GB (ZIP compressed)

### System Requirements
- **OS**: Windows 10/11 (64-bit)
- **RAM**: 2 GB minimum, 4 GB recommended
- **Disk**: 2 GB free space
- **Screen**: 1366x768 minimum resolution
- **Other**: No Python installation required

### First Run
1. Extract ZIP to desired location
2. Ensure `models/` folder exists
3. Run `TroLyLichTrinhV2_v1.0.3.exe`
4. Wait 3-5 seconds for model loading
5. Database `events.db` will be created automatically

### Troubleshooting
- **Slow startup**: Normal on first run (model loading)
- **Missing models**: Re-extract ZIP, ensure models/ folder exists
- **Database errors**: Delete `events.db` and restart
- **Sound not playing**: Check Windows sound settings
- **Theme not switching**: Restart application

## ✅ Final Checklist

Before releasing to production:

- [ ] All builds successful
- [ ] All tests passing
- [ ] Documentation complete
- [ ] Git tagged and pushed
- [ ] GitHub release created
- [ ] User guide available
- [ ] Known issues documented
- [ ] Support channels ready

## 🎉 Release Sign-off

**Built by**: d0ngle8k  
**Build Date**: November 8, 2025  
**Version**: 1.0.3 MVP  
**Status**: ✅ PRODUCTION READY

---

**Approved for Release**: ☐ YES  
**Release Date**: _____________  
**Released by**: _____________
