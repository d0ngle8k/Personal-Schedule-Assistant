# Tạo ZIP file cho Google Colab upload
# Chạy: .\scripts\create_colab_zip.ps1

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Tao ZIP file cho Google Colab" -ForegroundColor Yellow  
Write-Host "========================================`n" -ForegroundColor Cyan

$ProjectRoot = "C:\Users\d0ngle8k\Desktop\New folder (2)\NLP-Processing"
$OutputZip = "$env:USERPROFILE\Desktop\NLP-Colab-Minimal.zip"

Write-Host "Project: $ProjectRoot" -ForegroundColor White
Write-Host "Output: $OutputZip`n" -ForegroundColor White

# Tạo temp folder
$TempDir = Join-Path $env:TEMP "NLP-Colab-Temp"
if (Test-Path $TempDir) {
    Remove-Item $TempDir -Recurse -Force
}
New-Item -ItemType Directory -Path $TempDir -Force | Out-Null

Write-Host "Copying files..." -ForegroundColor Green

# Copy core_nlp
Copy-Item -Path (Join-Path $ProjectRoot "core_nlp") -Destination $TempDir -Recurse -Force
Write-Host "  [OK] core_nlp/" -ForegroundColor Gray

# Copy training_data
Copy-Item -Path (Join-Path $ProjectRoot "training_data") -Destination $TempDir -Recurse -Force
Write-Host "  [OK] training_data/" -ForegroundColor Gray

# Copy requirements.txt
Copy-Item -Path (Join-Path $ProjectRoot "requirements.txt") -Destination $TempDir -Force
Write-Host "  [OK] requirements.txt" -ForegroundColor Gray

# Copy README
Copy-Item -Path (Join-Path $ProjectRoot "README.md") -Destination $TempDir -Force -ErrorAction SilentlyContinue
Write-Host "  [OK] README.md" -ForegroundColor Gray

# Tạo ZIP
Write-Host "`nCreating ZIP..." -ForegroundColor Green
if (Test-Path $OutputZip) {
    Remove-Item $OutputZip -Force
}
Compress-Archive -Path "$TempDir\*" -DestinationPath $OutputZip -Force

# Tính size
$SizeMB = [math]::Round((Get-Item $OutputZip).Length / 1MB, 2)

# Cleanup
Remove-Item $TempDir -Recurse -Force

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "HOAN THANH!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan

Write-Host "`nFile: $OutputZip" -ForegroundColor Yellow
Write-Host "Size: $SizeMB MB`n" -ForegroundColor Yellow

Write-Host "BUOC TIEP THEO:" -ForegroundColor Cyan
Write-Host "1. Mo Google Drive: https://drive.google.com" -ForegroundColor White
Write-Host "2. Tao folder: NLP-Processing" -ForegroundColor White  
Write-Host "3. Upload file ZIP vua tao" -ForegroundColor White
Write-Host "4. Mo Google Colab: https://colab.research.google.com" -ForegroundColor White
Write-Host "5. Upload Google_Colab_Training.ipynb" -ForegroundColor White
Write-Host "6. Runtime -> T4 GPU -> Run cells`n" -ForegroundColor White

# Mở folder
Start-Process explorer.exe -ArgumentList "/select,`"$OutputZip`""

Write-Host "Da mo folder chua ZIP file!`n" -ForegroundColor Green
