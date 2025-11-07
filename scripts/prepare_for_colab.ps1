# Script tự động chuẩn bị files để upload lên Google Colab
# Usage: .\scripts\prepare_for_colab.ps1

param(
    [string]$OutputPath = "$env:USERPROFILE\Desktop",
    [switch]$Minimal,
    [switch]$Help
)

if ($Help) {
    Write-Host ""
    Write-Host "📤 Prepare Project for Google Colab" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor Cyan
    Write-Host "    .\scripts\prepare_for_colab.ps1 [options]" -ForegroundColor White
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Cyan
    Write-Host "    -OutputPath <path>    Output directory for ZIP file (default: Desktop)" -ForegroundColor White
    Write-Host "    -Minimal             Create minimal package (faster upload)" -ForegroundColor White
    Write-Host "    -Help                Show this help message" -ForegroundColor White
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Cyan
    Write-Host "    .\scripts\prepare_for_colab.ps1" -ForegroundColor White
    Write-Host "    .\scripts\prepare_for_colab.ps1 -Minimal" -ForegroundColor White
    Write-Host ""
    exit 0
}

Write-Host "`n==================================================================" -ForegroundColor Cyan
Write-Host "📤 Chuẩn bị Project cho Google Colab" -ForegroundColor Yellow
Write-Host "==================================================================" -ForegroundColor Cyan

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Write-Host "`n📁 Project root: $ProjectRoot" -ForegroundColor White

if ($Minimal) {
    Write-Host "📦 Mode: MINIMAL (chỉ files cần thiết)" -ForegroundColor Green
    
    # Tạo folder tạm
    $TempDir = Join-Path $env:TEMP "NLP-Colab-Minimal"
    if (Test-Path $TempDir) {
        Remove-Item $TempDir -Recurse -Force
    }
    New-Item -ItemType Directory -Path $TempDir -Force | Out-Null
    
    Write-Host "`n📋 Copying files..." -ForegroundColor White
    
    # Copy core_nlp
    Write-Host "   ✓ core_nlp/" -ForegroundColor Gray
    Copy-Item -Path (Join-Path $ProjectRoot "core_nlp") -Destination $TempDir -Recurse -Force
    
    # Copy training_data
    Write-Host "   ✓ training_data/" -ForegroundColor Gray
    Copy-Item -Path (Join-Path $ProjectRoot "training_data") -Destination $TempDir -Recurse -Force
    
    # Copy requirements.txt
    Write-Host "   ✓ requirements.txt" -ForegroundColor Gray
    Copy-Item -Path (Join-Path $ProjectRoot "requirements.txt") -Destination $TempDir -Force
    
    # Copy README
    if (Test-Path (Join-Path $ProjectRoot "README.md")) {
        Write-Host "   ✓ README.md" -ForegroundColor Gray
        Copy-Item -Path (Join-Path $ProjectRoot "README.md") -Destination $TempDir -Force
    }
    
    $ZipName = "NLP-Colab-Minimal.zip"
    $SourcePath = $TempDir
    
} else {
    Write-Host "📦 Mode: FULL (toàn bộ project)" -ForegroundColor Green
    
    # Tạo folder tạm và copy toàn bộ
    $TempDir = Join-Path $env:TEMP "NLP-Processing-Full"
    if (Test-Path $TempDir) {
        Remove-Item $TempDir -Recurse -Force
    }
    New-Item -ItemType Directory -Path $TempDir -Force | Out-Null
    
    Write-Host "`n📋 Copying project (excluding venv, __pycache__, models)..." -ForegroundColor White
    
    # Copy tất cả trừ những folder không cần
    $ExcludeDirs = @('.venv', '__pycache__', '.git', 'models', 'dist', 'build', '.pytest_cache')
    
    Get-ChildItem -Path $ProjectRoot | Where-Object {
        $_.Name -notin $ExcludeDirs
    } | ForEach-Object {
        Write-Host "   ✓ $($_.Name)" -ForegroundColor Gray
        Copy-Item -Path $_.FullName -Destination $TempDir -Recurse -Force
    }
    
    $ZipName = "NLP-Processing-Full.zip"
    $SourcePath = $TempDir
}

# Tạo ZIP
$ZipPath = Join-Path $OutputPath $ZipName

Write-Host "`n📦 Creating ZIP file..." -ForegroundColor White
if (Test-Path $ZipPath) {
    Remove-Item $ZipPath -Force
}

Compress-Archive -Path "$SourcePath\*" -DestinationPath $ZipPath -Force

# Tính kích thước
$SizeMB = (Get-Item $ZipPath).Length / 1MB

Write-Host "`n==================================================================" -ForegroundColor Cyan
Write-Host "✅ HOÀN THÀNH!" -ForegroundColor Green
Write-Host "==================================================================" -ForegroundColor Cyan

Write-Host "`n📁 ZIP File:" -ForegroundColor Yellow
Write-Host "   Path: $ZipPath" -ForegroundColor White
Write-Host "   Size: $("{0:N2}" -f $SizeMB) MB" -ForegroundColor White

Write-Host "`n📤 BƯỚC TIẾP THEO:" -ForegroundColor Yellow
Write-Host "   1. Mở Google Drive: https://drive.google.com" -ForegroundColor White
Write-Host "   2. Tạo folder mới: NLP-Processing" -ForegroundColor White
Write-Host "   3. Upload file: $ZipName" -ForegroundColor White
Write-Host "   4. Mở Google Colab: https://colab.research.google.com" -ForegroundColor White
Write-Host "   5. Upload notebook: Google_Colab_Training.ipynb" -ForegroundColor White
Write-Host "   6. Enable GPU: Runtime -> T4 GPU" -ForegroundColor White
Write-Host "   7. Run all cells" -ForegroundColor White

Write-Host "`n💡 Chi tiết:" -ForegroundColor Cyan
Write-Host "   Xem file GOOGLE_COLAB_UPLOAD_GUIDE.md" -ForegroundColor White

Write-Host "`n==================================================================" -ForegroundColor Cyan

# Cleanup temp dir
Remove-Item $TempDir -Recurse -Force

# Mở folder chứa ZIP
Start-Process explorer.exe -ArgumentList "/select,`"$ZipPath`""

Write-Host "`n✅ Đã mở folder chứa file ZIP" -ForegroundColor Green
Write-Host ""
