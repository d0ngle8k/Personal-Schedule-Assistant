# Hướng dẫn Build EXE

## Yêu cầu
- Python 3.12+ với venv đã cài đặt dependencies từ `requirements.txt`
- PyInstaller đã được cài đặt trong venv

## Phiên bản hiện tại

**v0.3** (Latest) - Build: 2025-11-05
- Hỗ trợ nhập test case format (input + expected) tự động parse qua NLP
- Generator test cases với --count argument (hỗ trợ tạo 10,000 cases)
- Cải thiện NLP parser: 99.6% accuracy trên 1000 test cases
- Semantic time period constraints (noon/midnight, morning/afternoon/evening)

## Build file .exe

### Cách 1: Sử dụng lệnh PyInstaller trực tiếp

```powershell
# Kích hoạt virtual environment
& C:/Users/d0ngle8k/Desktop/NLP-Processing/venv/bin/Activate.ps1

# Build file .exe (version 0.3 - latest)
python -m PyInstaller --name="TroLyLichTrinh0.3" --onefile --windowed --noconfirm --clean --add-data "database/schema.sql;database" --hidden-import="babel.numbers" --hidden-import="underthesea" --hidden-import="tkcalendar" main.py
```

### Cách 2: Sử dụng file spec có sẵn (nếu đã được tạo)

```powershell
# Kích hoạt virtual environment
& C:/Users/d0ngle8k/Desktop/NLP-Processing/venv/bin/Activate.ps1

# Build từ file spec (version 0.3)
python -m PyInstaller TroLyLichTrinh0.3.spec
```

## Kết quả

File executable sẽ được tạo tại: `dist/TroLyLichTrinh0.3.exe`

Kích thước: ~24.8 MB

## Version History

- **v0.3** (2025-11-05): Import test case format + 10k test generator + 99.6% NLP accuracy
- **v0.2** (2025-11-05): Time period semantics + UI input limit 300 chars
- **v0.1** (2025-11-05): Initial release with basic NLP + calendar + reminders

## Chạy ứng dụng

Chỉ cần double-click vào `TroLyLichTrinh.exe` trong thư mục `dist/`

## Lưu ý

- File .exe là standalone, có thể chạy trên máy Windows khác mà không cần cài Python
- Database sẽ được tạo tự động khi chạy lần đầu
- File schema.sql đã được embed vào trong .exe
- Các thư viện NLP (underthesea, babel) đã được bao gồm
