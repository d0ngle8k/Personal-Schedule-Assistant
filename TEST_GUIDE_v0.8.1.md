# 🧪 HƯỚNG DẪN TEST v0.8.1

## ✅ Các Chức Năng Đã Sửa/Thêm

### 1. ✅ FIX: Chức năng SỬA đã hoạt động
### 2. ✅ NEW: SORT bảng bằng cách click vào header

---

## 📋 Các Bước Test

### BƯỚC 1: Chuẩn bị dữ liệu test

Chạy lệnh sau để tạo dữ liệu mẫu:

```powershell
python test_sort_and_edit.py
```

**Kết quả mong đợi**:
```
✅ ALL TESTS PASSED
✅ Added 8/8 test events
```

Database bây giờ có 8 sự kiện với:
- Tên đa dạng: số (123, 1on1, 999) và chữ (AAA, Abc, Bbb, Zoom)
- Thời gian khác nhau: hôm nay, ngày mai, tuần sau, tháng sau
- Địa điểm khác nhau: Room A, 1st Floor, Zoom, Coffee Shop...
- Nhắc nhở: Có (15, 30, 60 phút) và Không (0)

---

### BƯỚC 2: Chạy ứng dụng

```powershell
python main.py
```

Ứng dụng sẽ mở với 8 sự kiện test đã tạo.

---

### BƯỚC 3: Test SORTING (Click vào header)

#### 🔢 Test Sort ID

1. **Click vào "ID" (lần 1)**
   - Kết quả: ID 1 → 2 → 3 → ... → 8 (Thấp → Cao)
   - Header hiển thị: `ID ▼`

2. **Click vào "ID" (lần 2)**
   - Kết quả: ID 8 → 7 → 6 → ... → 1 (Cao → Thấp)
   - Header hiển thị: `ID ▲`

#### 📝 Test Sort Sự Kiện

1. **Click vào "Sự kiện" (lần 1)**
   - Kết quả mong đợi (theo thứ tự):
     ```
     1. 123 Meeting       ← Số trước
     2. 1on1 Chat         ← Số
     3. 999 Review        ← Số
     4. AAA Priority      ← Chữ A
     5. Abc Conference    ← Chữ A (case-insensitive)
     6. abc meeting       ← Chữ a (case-insensitive)
     7. Bbb Workshop      ← Chữ B
     8. Zoom Call         ← Chữ Z
     ```
   - **Logic**: Số trước → A/a → B/b → ... → Z/z (không phân biệt hoa thường)

2. **Click vào "Sự kiện" (lần 2)**
   - Kết quả: Đảo ngược (Zoom → Bbb → abc → ... → 123)

#### ⏰ Test Sort Thời Gian

1. **Click vào "Thời gian" (lần 1)**
   - Kết quả: Gần nhất → Xa nhất
   - Ví dụ:
     ```
     19:53 hôm nay
     20:53 hôm nay
     23:53 hôm nay
     08:00 ngày mai
     09:00 ngày 09/11
     ...
     18:53 ngày 07/12
     ```

2. **Click vào "Thời gian" (lần 2)**
   - Kết quả: Xa nhất → Gần nhất (đảo ngược)

#### 🔔 Test Sort Nhắc Tôi

1. **Click vào "Nhắc tôi" (lần 1)**
   - Kết quả: "Không" trước → "Có" sau
   - Ví dụ:
     ```
     123 Meeting - Không
     abc meeting - Không
     999 Review - Không
     AAA Priority - Không
     1on1 Chat - Có (10 phút)
     Abc Conference - Có (15 phút)
     Zoom Call - Có (30 phút)
     Bbb Workshop - Có (60 phút)
     ```

2. **Click vào "Nhắc tôi" (lần 2)**
   - Kết quả: "Có" trước → "Không" sau

#### 📍 Test Sort Địa Điểm

1. **Click vào "Địa điểm" (lần 1)**
   - Kết quả: Số trước → Chữ A-Z (giống logic Sự kiện)
   - Ví dụ:
     ```
     1st Floor        ← Số
     2nd Floor        ← Số
     Coffee Shop      ← Chữ C
     Online           ← Chữ O
     Room A           ← Chữ R
     Room B           ← Chữ R
     Zoom             ← Chữ Z
     (không có)       ← Trống cuối cùng
     ```

2. **Click vào "Địa điểm" (lần 2)**
   - Kết quả: Đảo ngược

---

### BƯỚC 4: Test EDIT Function

#### Test Case 1: Sửa tên sự kiện

1. **Click chọn** bất kỳ sự kiện nào (ví dụ: "123 Meeting")
2. **Click nút "Sửa"**
3. Form chỉnh sửa xuất hiện ở dưới cùng:
   ```
   Chỉnh sửa sự kiện
   ID: 1
   Sự kiện: [123 Meeting]
   Ngày (YYYY-MM-DD): [2025-11-08]
   Giờ (HH:MM): [18:53]
   Địa điểm: [Room A]
   Nhắc (phút): [0]
   [Lưu] [Hủy]
   ```
4. **Đổi tên** "123 Meeting" → "999 Important Meeting"
5. **Click "Lưu"**
6. **Kiểm tra**:
   - ✅ Popup "Đã lưu - Cập nhật sự kiện thành công"
   - ✅ Bảng cập nhật, tên mới xuất hiện
   - ✅ Không có lỗi

#### Test Case 2: Sửa thời gian

1. Click chọn sự kiện
2. Click "Sửa"
3. **Đổi thời gian**:
   - Ngày: 2025-11-08 → 2025-11-15
   - Giờ: 18:53 → 10:00
4. Click "Lưu"
5. **Kiểm tra**:
   - ✅ Thời gian mới hiển thị: "15/11/2025 10:00"
   - ✅ Không lỗi duplicate (nếu thời gian trùng sẽ có cảnh báo)

#### Test Case 3: Sửa địa điểm và nhắc nhở

1. Click chọn sự kiện
2. Click "Sửa"
3. **Thay đổi**:
   - Địa điểm: "Room A" → "Conference Room 302"
   - Nhắc (phút): 0 → 30
4. Click "Lưu"
5. **Kiểm tra**:
   - ✅ Địa điểm cập nhật
   - ✅ Cột "Nhắc tôi": "Không" → "Có"

#### Test Case 4: Hủy chỉnh sửa

1. Click chọn sự kiện
2. Click "Sửa"
3. Thay đổi bất kỳ field nào
4. **Click "Hủy"**
5. **Kiểm tra**:
   - ✅ Form đóng lại
   - ✅ Không có thay đổi nào được lưu

---

## 🎯 Expected Results - Tổng Hợp

### ✅ Sorting
- **ID**: Toggle Low↔High
- **Sự kiện**: Smart sort (Số → A/a → B/b)
- **Thời gian**: Nearest↔Farthest
- **Nhắc tôi**: No↔Yes
- **Địa điểm**: Smart sort (như Sự kiện)
- **Indicators**: ▼/▲ hiển thị đúng

### ✅ Edit Function
- **BEFORE v0.8.1**: Click "Lưu" → ❌ ERROR (100% broken)
- **AFTER v0.8.1**: Click "Lưu" → ✅ SUCCESS (100% working)

---

## 🐛 Các Lỗi Đã Sửa

### Critical Bug: Edit Function
```python
# ❌ BEFORE (v0.8.0)
payload = {
    'event': event_name,  # Wrong key!
    ...
}

# ✅ AFTER (v0.8.1)
payload = {
    'event_name': event_name,  # Correct key
    ...
}
```

**Impact**:
- BEFORE: Edit 100% broken, không lưu được
- AFTER: Edit 100% working, lưu thành công

---

## 📊 Test Checklist

Copy checklist này để test:

```
[ ] Test data created (python test_sort_and_edit.py)
[ ] App opened (python main.py)

SORTING:
[ ] ID sort (Click 1: Low→High, Click 2: High→Low)
[ ] Event sort (Click 1: 123→AAA→Bbb→Zoom, Click 2: Reverse)
[ ] Time sort (Click 1: Nearest, Click 2: Farthest)
[ ] Remind sort (Click 1: No→Yes, Click 2: Yes→No)
[ ] Location sort (Click 1: 1st→Coffee→Room, Click 2: Reverse)
[ ] Indicators show ▼/▲ correctly

EDIT:
[ ] Edit event name → Save → SUCCESS
[ ] Edit time → Save → SUCCESS
[ ] Edit location → Save → SUCCESS
[ ] Edit reminder → Save → SUCCESS
[ ] Cancel edit → No changes saved
[ ] No errors during edit save
```

---

## 💡 Tips

1. **Sort nhiều lần**: Click cùng 1 header nhiều lần để thấy toggle
2. **Sort khác column**: Click column khác sẽ reset indicator
3. **Edit nhiều event**: Thử edit nhiều sự kiện khác nhau
4. **Duplicate time**: Thử sửa thời gian trùng với event khác → Should show warning

---

## 🎉 Kết Luận

Nếu tất cả test cases PASS:
- ✅ v0.8.1 hoạt động hoàn hảo
- ✅ Edit function đã được sửa
- ✅ Sorting feature hoạt động thông minh
- ✅ Ready for production

---

*Made by Senior Dev for d0ngle8k*
*Version: 0.8.1*
*Date: November 7, 2025*
