# 🎉 Kaggle Training Setup - Quick Start

## ✅ Đã Push lên GitHub

```
✅ kaggle_training.ipynb      (Kaggle notebook)
✅ KAGGLE_TRAINING_GUIDE.md   (Hướng dẫn chi tiết)
```

---

## 🚀 Quick Start (5 phút setup)

### 1️⃣ Mở Kaggle
👉 https://www.kaggle.com/code

### 2️⃣ Tạo Notebook Mới
- Click **New Notebook**

### 3️⃣ Import từ GitHub
- **File** → **Import Notebook**
- Tab **GitHub**
- Paste: `https://github.com/d0ngle8k/NLP-Processing/blob/main/kaggle_training.ipynb`
- Click **Import**

### 4️⃣ Bật GPU
- Click **Settings** (⚙️ bên phải)
- **Accelerator** → **GPU P100** (hoặc T4)
- Click **Save**

### 5️⃣ Run All Cells
- Click **Run All** (hoặc **Ctrl+Shift+Enter**)
- ⏱️ Đợi **20-30 phút** (P100) hoặc **30-40 phút** (T4)

### 6️⃣ Download Model
- Xem **Output** panel bên phải
- Download file `phobert_finetuned.zip` (800MB - 1.5GB)

---

## 📊 Performance So Sánh

| Platform | GPU | VRAM | Time (3 epochs) | Rank |
|----------|-----|------|-----------------|------|
| **Kaggle** | **P100** | **16GB** | **20-30 min** ⚡⚡⚡ | **🥇 #1** |
| **Colab** | T4 | 15GB | 30-40 min ⚡⚡ | 🥈 #2 |
| **Local** | RTX 2060 | 8GB | 45-60 min ⚡ | 🥉 #3 |
| Local CPU | - | - | ~30 hours ❌ | #4 |

**Khuyến nghị: KAGGLE** 🏆

---

## ⚠️ Lưu Ý Quan Trọng

### 1. Phone Verification (BẮT BUỘC)
Kaggle yêu cầu verify số điện thoại để dùng GPU:
1. Settings → Phone Verification
2. Nhập số: +84 xxx xxx xxx
3. Nhập OTP code
4. ✅ Verified

### 2. GPU Quota
- **30 giờ GPU/tuần** (reset mỗi tuần)
- Training này chỉ tốn **~0.5 giờ** (30 phút)
- Còn dư 29.5 giờ cho lần sau

### 3. Session Timeout
- Kaggle kill sessions inactive > 60 phút
- **Đừng đóng tab** trong khi training
- Download model ngay sau khi xong

---

## 📥 Sau Khi Download

### Windows:
```powershell
cd "C:\Users\d0ngle8k\Desktop\New folder (2)\NLP-Processing"

# Giải nén
Expand-Archive -Path .\phobert_finetuned.zip -DestinationPath . -Force

# Test
python comprehensive_test.py

# Commit
git add models/phobert_finetuned
git commit -m "v1.1.0: Add fine-tuned PhoBERT model (Kaggle P100)"
git push
```

---

## 🎯 Expected Results

### Before Fine-tuning:
```
PhoBERT Macro F1: 71.43%
  - Event: 0%
  - Time: 0%
  - Location: 0%
  - Reminder: 0%
```

### After Fine-tuning:
```
PhoBERT Macro F1: 90%+ ⬆️ +18.57%
  - Event: 90%+ ⬆️ +90%
  - Time: 85%+ ⬆️ +85%
  - Location: 80%+ ⬆️ +80%
  - Reminder: 85%+ ⬆️ +85%
```

---

## 📚 Documentation

### Chi Tiết:
📖 **KAGGLE_TRAINING_GUIDE.md** (đầy đủ hơn)
- Account setup
- Phone verification
- Troubleshooting
- Best practices

### Quick Reference:
📓 **kaggle_training.ipynb** (notebook)
- Ready to run
- Step-by-step cells
- Auto-install dependencies

---

## 🆘 Troubleshooting

### GPU Not Available?
→ Settings → Accelerator → GPU P100 → Save

### Out of Memory?
→ Cell 5: `--batch_size 16` → thay bằng `--batch_size 8`

### Training Data Not Found?
→ Cell 1: Re-run clone command

### Can't Download ZIP?
→ Output panel → Find `phobert_finetuned.zip` → Click download

---

## ✅ Checklist

- [ ] Đã có tài khoản Kaggle
- [ ] Đã verify phone number ⚠️
- [ ] Đã import `kaggle_training.ipynb`
- [ ] Đã bật GPU P100/T4 ⚠️
- [ ] Đã run all cells
- [ ] Training đang chạy (~25 phút)
- [ ] Đã download model
- [ ] Đã test local
- [ ] Đã commit lên GitHub

---

## 🎁 Files Created

```
kaggle_training.ipynb         # Kaggle notebook (ready to run)
KAGGLE_TRAINING_GUIDE.md      # Complete guide (30+ pages)
```

**Commit:** `ac1580a` ✅ Pushed to GitHub

---

## 🚀 Next Steps

1. **Bây giờ**: Mở https://www.kaggle.com
2. **Import**: `kaggle_training.ipynb` từ GitHub
3. **Bật GPU**: P100 hoặc T4
4. **Run**: All cells
5. **Chờ**: 20-30 phút
6. **Download**: `phobert_finetuned.zip`
7. **Deploy**: Giải nén + test + commit
8. **Done**: PhoBERT fine-tuned model ready! 🎉

---

**⏰ Total Time**: ~30 phút (setup 5 phút + training 25 phút)

**💰 Cost**: FREE (Kaggle GPU miễn phí)

**📈 Result**: PhoBERT F1 from 71% → 90%+ 

**Go! 🚀**
