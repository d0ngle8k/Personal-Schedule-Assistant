# 🚀 Quick Start Guide - Trợ Lý Lịch Trình V2 v1.0.3

## 📥 Cài Đặt Nhanh (5 phút)

### Bước 1: Tải về
1. Tải file `TroLyLichTrinhV2_v1.0.3.zip` từ GitHub Releases
2. Giải nén vào thư mục mong muốn (VD: `C:\TroLyLichTrinh\`)

### Bước 2: Kiểm tra cấu trúc
Đảm bảo thư mục có cấu trúc sau:
```
TroLyLichTrinhV2_v1.0.3/
├── TroLyLichTrinhV2_v1.0.3.exe  ← File chính
├── models/                       ← Thư mục models (BẮT BUỘC)
│   ├── phobert_base/
│   └── phobert_finetuned/
└── sounds/                       ← Âm thanh tùy chỉnh (tùy chọn)
```

### Bước 3: Chạy ứng dụng
- Double-click vào `TroLyLichTrinhV2_v1.0.3.exe`
- Lần đầu chạy sẽ mất 3-5 giây để load models
- Cửa sổ ứng dụng sẽ hiện ra 🎉

---

## 💡 Hướng Dẫn Sử Dụng Cơ Bản

### 1. Tạo Sự Kiện Nhanh

**Cách 1: Gõ tự nhiên (NLP)**
```
Họp với khách hàng 10h sáng mai ở phòng 302 nhắc trước 30 phút
```
→ Nhấn "Thêm Sự Kiện" → Xong! ✅

**Cách 2: Sử dụng form chi tiết**
1. Nhập tên sự kiện: `Họp với khách hàng`
2. Chọn ngày từ calendar
3. Nhập thời gian: `10:00`
4. Nhập địa điểm: `Phòng 302`
5. Chọn nhắc nhở: `30 phút trước`
6. Nhấn "Thêm Sự Kiện"

### 2. Định Dạng Thời Gian Hỗ Trợ

#### Giờ cơ bản
- `10h`, `10h30`, `10:30`
- `10 giờ 30 phút`
- **MỚI v1.0.3**: `1h50p` (1 giờ 50 phút) ✨

#### Ngày
- `mai`, `hôm nay`, `ngày mai`
- `thứ 2`, `thứ 3`, `chủ nhật`
- `20/10`, `20/10/2025`
- `ngày 20 tháng 10`

#### Thời gian trong ngày
- `sáng` (06:00-11:59)
- `trưa` (12:00)
- `chiều` (12:00-17:59)
- `tối` (18:00-21:59)
- `đêm` (22:00-05:59)

#### Ví dụ kết hợp
```
Họp 1h50p chiều mai          → Mai 13:50
Gặp khách 10h15p sáng thứ 2  → Thứ 2 10:15
Meeting 2h30p                 → Ngày mai 02:30 (tự động sang ngày mai nếu quá khứ)
```

### 3. Chức Năng Chính

#### 🔍 Tìm Kiếm
- Gõ từ khóa vào ô tìm kiếm
- Tìm theo tên, địa điểm, mô tả

#### 📊 Sắp Xếp
- **Thời gian**: Gần nhất → xa nhất
- **Tên A-Z**: Theo thứ tự bảng chữ cái

#### ✏️ Sửa/Xóa Sự Kiện
- Click vào sự kiện trong danh sách
- Nhấn "Sửa" hoặc "Xóa"

#### 📤 Xuất/Nhập Dữ Liệu
- **Xuất JSON**: Menu → Export → JSON
- **Xuất ICS**: Menu → Export → ICS (dùng cho Google Calendar, Outlook)
- **Nhập**: Menu → Import → Chọn file

#### 📈 Thống Kê
- Xem tổng số sự kiện
- Sắp tới/Đã qua/Hôm nay
- Địa điểm phổ biến

---

## ⚙️ Cài Đặt

### 🔔 Âm Thanh Thông Báo

**Âm thanh mặc định Windows:**
- Windows Notify
- Windows Alarm
- Windows Reminder
- (Nhiều lựa chọn khác...)

**Âm thanh tùy chỉnh:**
1. Chọn "Custom Sound..."
2. Duyệt file âm thanh (.wav, .mp3, .ogg, .m4a)
3. Nhấn "Lưu"

**✨ MỚI v1.0.3:** Âm thanh được lưu tự động và khôi phục khi restart app! 🎉

### 🎨 Giao Diện

**Chuyển Dark/Light Mode:**
- Click nút "🌙 Dark Mode" ở góc trên
- **✨ MỚI v1.0.3:** Hiệu ứng fade mượt mà khi chuyển đổi!

---

## 🎯 Mẹo & Thủ Thuật

### 1. Nhập Nhanh với NLP
```
# Đầy đủ thông tin một lần
Họp team lúc 14h30 ngày mai ở văn phòng nhắc trước 15 phút

# Ngắn gọn - app tự hiểu
mai 10h họp phòng 302

# Dùng pattern mới "1h50p"
1h50p gặp khách
```

### 2. Khoảng Thời Gian
```
từ 10h đến 12h họp
từ 1h50p đến 3h30p training
```

### 3. Sự Kiện Lặp Lại
- Tạo template sự kiện
- Copy và chỉnh sửa ngày/giờ

### 4. Nhắc Nhở Thông Minh
```
nhắc trước 10 phút
nhắc trước 30p
nhắc trước 1 giờ
nhắc trước 1 ngày
```

---

## ❓ Khắc Phục Sự Cố

### App không khởi động được
**Nguyên nhân:** Thiếu thư mục `models/`  
**Giải pháp:** Đảm bảo folder `models/` nằm cùng thư mục với EXE

### Âm thanh không phát
**Nguyên nhân:** Volume hệ thống tắt hoặc file âm thanh lỗi  
**Giải pháp:**
1. Kiểm tra volume Windows
2. Thử chọn âm thanh mặc định khác
3. Restart app

### Sự kiện không được parse đúng
**Ví dụ:** "chu nhat chieu di cafe" → location sai  
**Giải pháp:** Sửa thủ công sau khi tạo, hoặc dùng format rõ ràng hơn:
```
chủ nhật 15h đi cafe  ← Rõ ràng hơn
```

### Database lỗi
**Triệu chứng:** Lỗi khi mở app  
**Giải pháp:**
1. Tìm file `events.db` (cùng folder với EXE)
2. Đổi tên thành `events.db.backup`
3. Restart app (database mới sẽ được tạo)

---

## 📝 Câu Hỏi Thường Gặp (FAQ)

**Q: App có cần cài Python không?**  
A: Không! File EXE đã bao gồm tất cả dependencies.

**Q: Dữ liệu lưu ở đâu?**  
A: File `events.db` (SQLite) cùng thư mục với EXE.

**Q: Có thể chạy trên Linux/Mac không?**  
A: Hiện tại chỉ hỗ trợ Windows. Linux/Mac cần build riêng.

**Q: App có gửi dữ liệu ra ngoài không?**  
A: Không! Tất cả dữ liệu lưu local, không kết nối internet.

**Q: Làm sao backup dữ liệu?**  
A: Copy file `events.db` hoặc dùng Export → JSON.

**Q: Pattern "1h50p" có bắt buộc dùng "p" không?**  
A: Không! `1h50`, `1:50`, `1 giờ 50 phút` đều work. "1h50p" chỉ là option ngắn gọn.

---

## 🎓 Ví Dụ Thực Tế

### Lịch Công Việc
```
# Thứ 2
Họp team 9h sáng ở phòng họp A nhắc trước 10 phút
Review code 14h văn phòng
Meeting khách hàng 16h30 phòng 302 nhắc trước 15 phút

# Thứ 3
Training nhân viên từ 10h đến 12h phòng đào tạo
Deadline báo cáo 17h nhắc trước 1 giờ
```

### Lịch Cá Nhân
```
# Cuối tuần
Thứ 7 10h tập gym
Chủ nhật 15h xem phim CGV
Chủ nhật 19h ăn tối với gia đình nhà hàng ABC
```

### Sự Kiện Quan Trọng
```
# Dùng format rõ ràng + reminder dài
Sinh nhật mẹ ngày 15/12/2025 lúc 18h nhắc trước 3 ngày
Deadline dự án ngày 30/11/2025 17h nhắc trước 1 tuần
Hẹn bác sĩ 20/11 10h bệnh viện XYZ nhắc trước 2 ngày
```

---

## 📞 Hỗ Trợ

**Gặp vấn đề?**
- Đọc phần "Khắc Phục Sự Cố" phía trên
- Xem file `RELEASE_v1.0.3.md` để biết tính năng mới
- Liên hệ: [GitHub Issues](https://github.com/d0ngle8k/NLP-Processing/issues)

**Góp ý cải tiến?**
- Mở GitHub Issue
- Mô tả chi tiết feature mong muốn
- Attach screenshot nếu có

---

## 🎉 Chúc Bạn Sử Dụng Vui Vẻ!

**Version:** 1.0.3 MVP  
**Build Date:** November 8, 2025  
**Developer:** d0ngle8k

---

**Tips cuối:** Thử gõ `1h50p họp` và xem magic xảy ra! ✨
