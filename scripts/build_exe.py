from __future__ import annotations

"""Build Windows .exe for the Vietnamese NLP Calendar Assistant (Hybrid Model).

This script wraps PyInstaller to package the application including:
- main.py GUI entry point
- SQLite schema.sql
- Hybrid PhoBERT model directory (models/phobert_finetuned) if present
- Optional base PhoBERT model directory (models/phobert_base) if present

It will generate either an ONEDIR or ONEFILE build (default: onedir for large ML models).
Torch + transformers are heavy; ONEFILE will unpack slowly and increase build complexity.

USAGE (PowerShell):
    # Activate venv first
    .\.venv\Scripts\Activate.ps1

    # Install dependencies (ensure pyinstaller is available)
    pip install -r requirements.txt

    # Build onedir (recommended, no console window)
    python scripts/build_exe.py --name TroLyLichTrinhHybrid

    # Build onedir WITH console window for debug prints
    python scripts/build_exe.py --name TroLyLichTrinhHybrid --console

    # Build onefile (will be large, slower startup)
    python scripts/build_exe.py --name TroLyLichTrinhHybrid --onefile

    # Build onefile WITH console
    python scripts/build_exe.py --name TroLyLichTrinhHybrid --onefile --console

OUTPUT:
    dist/ TroLyLichTrinhHybrid/ (folder)  OR  dist/TroLyLichTrinhHybrid.exe (onefile)

REQUIREMENTS:
- Ensure models/phobert_finetuned exists for hybrid mode, else exe will fall back to rule-based.
- Underthesea may use a user home cache (~/.underthesea). The app overrides Path.home() in frozen mode;
  if you need those resources, copy that folder into 'underthesea_cache' and pass --underthesea-cache.

OPTIONS:
    --name NAME              Output executable/app name (default: CalendarAssistant)
    --onefile                Build a single-file exe instead of directory
    --underthesea-cache PATH Include a local underthesea cache directory
    --no-model               Exclude PhoBERT models (forces rule-based only)
    --console                Show console window (useful for debug / hybrid mode confirmation)

"""
import argparse
import os
import sys
from pathlib import Path
import shutil
import subprocess

# Ensure root path import resolution (in case script executed from elsewhere)
ROOT = Path(__file__).resolve().parent.parent
os.chdir(str(ROOT))

SPEC_NAME = "app_hybrid_autogen.spec"

def collect_data_pairs(source: Path, dest_rel: str):
    """Return list of (file, destination) pairs for PyInstaller --add-data."""
    pairs = []
    if source.is_file():
        pairs.append(f"{source};{dest_rel}")
    elif source.is_dir():
        for p in source.rglob('*'):
            if p.is_file():
                rel = p.relative_to(source)
                pairs.append(f"{p};{dest_rel}/{rel.as_posix()}")
    return pairs

def build_spec(args, data_pairs, hidden_imports):
    """Create a minimal spec file that includes dynamic datas and hidden imports.

    The console flag is injected directly into the EXE() call.
    """
    spec_path = ROOT / SPEC_NAME
    datas_entries = []
    for pair in data_pairs:
        # pair format: file;dest
        file_part, dest_part = pair.split(';', 1)
        # Normalize to forward slashes to avoid Windows unicode escape issues in spec
        file_norm = Path(file_part).as_posix()
        dest_norm = dest_part.replace('\\', '/')
        datas_entries.append(f"('{file_norm}', '{dest_norm}')")

    spec_content = f"""# Auto-generated PyInstaller spec (hybrid model)
# -*- mode: python -*-
import sys
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

a = Analysis(['main.py'],
             pathex=['{ROOT.as_posix()}'],
             binaries=[],
             datas=[{', '.join(datas_entries)}],
             hiddenimports={hidden_imports},
             hookspath=[],
             runtime_hooks=[],
             excludes=['pytest','unittest','test'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='{args.name}',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console={'True' if args.console else 'False'},
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None)
"""
    if not args.onefile:
        # Onedir build produces COLLECT section
        spec_content += f"""
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='{args.name}')
"""
    spec_path.write_text(spec_content, encoding='utf-8')
    return spec_path

def main():
    parser = argparse.ArgumentParser(description="Build hybrid NLP assistant executable")
    parser.add_argument('--name', default='CalendarAssistant', help='Executable name')
    parser.add_argument('--onefile', action='store_true', help='Build single-file exe')
    parser.add_argument('--underthesea-cache', type=str, help='Path to underthesea cache directory (~/.underthesea)')
    parser.add_argument('--no-model', action='store_true', help='Exclude PhoBERT model directories')
    parser.add_argument('--console', action='store_true', help='Show console window for debug prints')
    args = parser.parse_args()

    # Verify pyinstaller availability
    try:
        subprocess.run([sys.executable, '-m', 'PyInstaller', '--version'], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print('[ERROR] PyInstaller is not installed. Run: pip install pyinstaller')
        sys.exit(1)

    data_pairs = []

    # Always include schema.sql
    schema_path = ROOT / 'database' / 'schema.sql'
    if schema_path.exists():
        data_pairs.extend(collect_data_pairs(schema_path, 'database'))
    else:
        print('[WARN] database/schema.sql not found – DB init may fail in EXE.')

    # Include models if not disabled
    if not args.no_model:
        finetuned = ROOT / 'models' / 'phobert_finetuned'
        base_model = ROOT / 'models' / 'phobert_base'
        if finetuned.exists():
            data_pairs.extend(collect_data_pairs(finetuned, 'models/phobert_finetuned'))
        else:
            print('[WARN] models/phobert_finetuned missing – hybrid will fallback to base or rule-based.')
        if base_model.exists():
            data_pairs.extend(collect_data_pairs(base_model, 'models/phobert_base'))

    # Optional underthesea cache packing
    if args.underthesea_cache:
        cache_dir = Path(args.underthesea_cache).expanduser()
        if cache_dir.exists():
            data_pairs.extend(collect_data_pairs(cache_dir, '.underthesea'))
        else:
            print(f'[WARN] underthesea cache path not found: {cache_dir}')

    hidden_imports = [
        'tkcalendar', 'babel.numbers', 'underthesea', 'transformers', 'tqdm',
        'sklearn.utils._weight_vector', 'reportlab.graphics.barcode.common',
        'openpyxl.cell._writer'
    ]

    spec_path = build_spec(args, data_pairs, hidden_imports)
    print(f'[INFO] Generated spec: {spec_path}')

    cmd = [sys.executable, '-m', 'PyInstaller', str(spec_path)]
    if args.onefile:
        print('[INFO] Building ONEFILE executable (may be very large)...')
    else:
        print('[INFO] Building ONEDIR executable (recommended for large ML models)...')
    if args.console:
        print('[INFO] Console window ENABLED (hybrid debug prints visible).')
    else:
        print('[INFO] Console window hidden. Use --console to see debug output.')

    # Clean previous dist/build for this name
    dist_dir = ROOT / 'dist' / args.name
    onefile_exe = ROOT / 'dist' / f'{args.name}.exe'
    build_dir = ROOT / 'build' / args.name
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    if onefile_exe.exists():
        onefile_exe.unlink()
    if build_dir.exists():
        shutil.rmtree(build_dir)

    # Run PyInstaller
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print('[ERROR] PyInstaller build failed.')
        sys.exit(result.returncode)

    # Post-build summary
    if args.onefile:
        if onefile_exe.exists():
            size_mb = onefile_exe.stat().st_size / (1024*1024)
            print(f'[SUCCESS] Built onefile EXE: {onefile_exe} ({size_mb:.2f} MB)')
        else:
            print('[WARN] Expected onefile executable not found.')
    else:
        if dist_dir.exists():
            total_size = sum(p.stat().st_size for p in dist_dir.rglob('*') if p.is_file()) / (1024*1024)
            print(f'[SUCCESS] Built onedir app: {dist_dir} (≈{total_size:.2f} MB total files)')
        else:
            print('[WARN] dist directory missing after build.')

    print('\nNEXT STEPS:')
    print('  1. Test running the EXE: dist/<Name>/<Name>.exe (onedir) or dist/<Name>.exe (onefile)')
    print('  2. If built with --console, verify hybrid mode prints: "🔥 HYBRID MODE" on launch')
    print('  3. If fallback occurs, confirm model path packaged or rebuild with --no-model intentionally')
    print('  4. Distribute the dist/ folder (onedir) or single exe (onefile). Ensure LICENSE compliance for models.')


if __name__ == '__main__':
    main()
