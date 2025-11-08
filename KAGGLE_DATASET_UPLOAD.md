# 🔧 Kaggle Training - Dataset Upload Method

## ⚠️ Vấn Đề: Kaggle Không Có Internet

Kaggle notebooks **KHÔNG thể** clone từ GitHub vì không có internet access.

**Giải pháp**: Upload code như Kaggle Dataset!

---

## 📦 Phương Pháp 1: Upload Dataset (Khuyến nghị)

### Bước 1: Download Repo về Máy

```powershell
# Windows - PowerShell
cd C:\Users\d0ngle8k\Desktop

# Download từ GitHub
git pull origin main

# Hoặc download ZIP từ GitHub:
# https://github.com/d0ngle8k/NLP-Processing/archive/refs/heads/main.zip
```

### Bước 2: Tạo ZIP File

```powershell
# Zip thư mục (không cần .git, .venv, build, dist)
cd "C:\Users\d0ngle8k\Desktop\New folder (2)\NLP-Processing"

# Tạo clean copy
mkdir temp_kaggle
Copy-Item -Path .\* -Destination .\temp_kaggle\ -Exclude .git,.venv,build,dist,__pycache__,*.pyc -Recurse

# Zip
Compress-Archive -Path .\temp_kaggle\* -DestinationPath .\nlp-processing-kaggle.zip

# Clean up
Remove-Item -Recurse -Force .\temp_kaggle
```

### Bước 3: Upload lên Kaggle Dataset

1. **Vào Kaggle Datasets**: https://www.kaggle.com/datasets
2. **Click "New Dataset"** (góc trên bên phải)
3. **Upload File**:
   - Kéo thả `nlp-processing-kaggle.zip`
   - Hoặc click "Select Files" → chọn ZIP
4. **Điền thông tin**:
   - **Title**: `NLP Processing Code`
   - **Subtitle**: `PhoBERT Fine-tuning for Vietnamese Event Extraction`
   - **Description**: 
     ```
     Code and training data for PhoBERT fine-tuning.
     
     Includes:
     - Training scripts
     - PhoBERT trainer
     - 76K+ training samples
     - Pipeline code
     ```
   - **Visibility**: Private (hoặc Public nếu muốn)
5. **Click "Create"**

⏱️ Upload time: ~2-5 phút (tùy mạng)

### Bước 4: Tạo Kaggle Notebook

1. **Vào**: https://www.kaggle.com/code
2. **Click "New Notebook"**
3. **Settings** → **Accelerator** → **GPU P100**
4. **Click "Add Data"** (bên phải):
   - Search: `nlp processing code` (dataset vừa upload)
   - Click **Add**

### Bước 5: Copy Code ra Working Directory

```python
# Cell 1: Setup
!ls -la /kaggle/input

# Cell 2: Extract code
!unzip /kaggle/input/nlp-processing-code/nlp-processing-kaggle.zip -d /kaggle/working/
%cd /kaggle/working

# Cell 3: Verify
!ls -la
!ls training_data/
```

### Bước 6: Install Dependencies

```python
# Cell 4: Install
!pip install -q torch transformers underthesea tqdm
```

### Bước 7: Check GPU

```python
# Cell 5: Check GPU
import torch
print(f"GPU: {torch.cuda.get_device_name(0)}")
print(f"CUDA: {torch.cuda.is_available()}")
```

### Bước 8: Start Training

```python
# Cell 6: Train (20-30 phút)
!python train_phobert.py --epochs 3 --batch_size 16
```

### Bước 9: Download Model

```python
# Cell 7: Create ZIP
!zip -r phobert_finetuned.zip models/phobert_finetuned/

# Cell 8: Check size
!ls -lh phobert_finetuned.zip

# Download từ Output panel →
```

---

## 📦 Phương Pháp 2: Copy-Paste Code (Alternative)

Nếu không muốn upload dataset, copy-paste code trực tiếp:

### Cell 1: Create Directory Structure
```python
!mkdir -p core_nlp services database scripts training_data
```

### Cell 2: Paste train_phobert.py
```python
%%writefile train_phobert.py
# Copy toàn bộ nội dung từ train_phobert.py
# Paste vào đây...
```

### Cell 3: Paste phobert_trainer.py
```python
%%writefile core_nlp/phobert_trainer.py
# Copy toàn bộ nội dung...
```

**❌ Nhược điểm**: Phải paste nhiều files (10+ files), dễ lỗi

---

## 🎯 So Sánh Phương Pháp

| Method | Pros | Cons | Time |
|--------|------|------|------|
| **Upload Dataset** | ✅ Dễ, nhanh, ít lỗi | Cần upload lần đầu | 5-10 phút |
| Copy-Paste Code | Không cần upload | ❌ Nhiều lỗi, mất thời gian | 20-30 phút |

**Khuyến nghị: Upload Dataset** 🏆

---

## 📝 Template Kaggle Notebook (Sau Upload Dataset)

```python
# ==================== CELL 1: Extract Code ====================
!ls /kaggle/input
!unzip /kaggle/input/nlp-processing-code/*.zip -d /kaggle/working/
%cd /kaggle/working
!ls -la

# ==================== CELL 2: Install ====================
!pip install -q torch transformers underthesea tqdm

# ==================== CELL 3: Check GPU ====================
import torch
print(f"GPU: {torch.cuda.get_device_name(0)}")
print(f"Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")

# ==================== CELL 4: Check Data ====================
!ls training_data/
import json
with open('training_data/phobert_training_augmented.json') as f:
    data = json.load(f)
print(f"Samples: {len(data):,}")

# ==================== CELL 5: Train (25 min) ====================
!python train_phobert.py --epochs 3 --batch_size 16

# ==================== CELL 6: Create ZIP ====================
!zip -r phobert_finetuned.zip models/phobert_finetuned/
!ls -lh phobert_finetuned.zip

# Download từ Output panel →
```

---

## ✅ Quick Checklist

### Before Starting:
- [ ] Đã download repo về máy
- [ ] Đã tạo ZIP file (clean, no .git/.venv)
- [ ] Đã upload lên Kaggle Dataset
- [ ] Đã verify phone number

### In Kaggle:
- [ ] Đã tạo notebook mới
- [ ] Đã bật GPU P100/T4
- [ ] Đã add dataset vào notebook
- [ ] Đã extract code ra /kaggle/working
- [ ] Đã install dependencies
- [ ] GPU confirmed working
- [ ] Training data verified
- [ ] Training started

### After Training:
- [ ] Training completed (3/3 epochs)
- [ ] Đã tạo ZIP file
- [ ] Đã download về local
- [ ] Đã test model
- [ ] Đã commit lên GitHub

---

## 🆘 Troubleshooting

### "Could not resolve host: github.com"
→ **Đúng rồi!** Kaggle không có internet. Dùng Dataset upload method.

### "No such file or directory"
→ Check dataset đã add vào notebook chưa: Click "Add Data" → Search dataset

### "Cannot unzip"
→ Check path: `!ls /kaggle/input/` để xem đúng tên dataset

### Dataset upload failed
→ File quá lớn? Xóa thư mục không cần: .git, .venv, build, dist, __pycache__

---

## 🎁 Files to Prepare

### Essential (Phải có):
```
✅ train_phobert.py
✅ core_nlp/phobert_trainer.py
✅ core_nlp/phobert_model.py
✅ core_nlp/pipeline.py
✅ core_nlp/time_parser.py
✅ training_data/phobert_training_augmented.json
```

### Optional (Có thể bỏ):
```
❌ .git/
❌ .venv/
❌ build/
❌ dist/
❌ __pycache__/
❌ *.pyc
❌ version_document/
❌ tests/*.json (trừ test_cases.json nếu cần)
```

---

## 🚀 Final Steps

1. ✅ Upload dataset lên Kaggle
2. ✅ Tạo notebook + bật GPU
3. ✅ Add dataset vào notebook
4. ✅ Extract + install
5. ✅ Train (25 phút)
6. ✅ Download model
7. ✅ Test local + commit

**Total time**: ~35-40 phút (setup 10' + training 25')

**Cost**: FREE

**Result**: PhoBERT fine-tuned model! 🎉
