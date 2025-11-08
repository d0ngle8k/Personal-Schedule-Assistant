# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules, collect_data_files, collect_all
import os
import sys

block_cipher = None

# Get customtkinter path - use absolute path
import customtkinter
ctk_path = os.path.dirname(customtkinter.__file__)

# Manually add project data directories
datas = [
    (ctk_path, 'customtkinter'),  # Include entire customtkinter package
    ('database/schema.sql', 'database'),
    ('database/db_manager.py', 'database'),
    ('core_nlp', 'core_nlp'),
    ('services', 'services'),
    ('widgets', 'widgets'),
    ('requirements.txt', '.'),
]

# Add models if they exist
if os.path.exists('models/phobert_base'):
    datas.append(('models/phobert_base', 'models/phobert_base'))
if os.path.exists('models/phobert_finetuned'):
    datas.append(('models/phobert_finetuned', 'models/phobert_finetuned'))

# Add training data
if os.path.exists('training_data'):
    datas.append(('training_data', 'training_data'))

# Add sounds folders (create if empty)
if os.path.exists('sounds'):
    datas.append(('sounds', 'sounds'))

# Hidden imports for dependencies
hiddenimports = (
    collect_submodules('customtkinter') +
    collect_submodules('tkcalendar') +
    collect_submodules('playsound') +
    collect_submodules('PIL') +
    collect_submodules('dateutil') +
    collect_submodules('underthesea') +
    collect_submodules('transformers') +
    collect_submodules('torch') +
    ['customtkinter', 'customtkinter.windows', 'customtkinter.windows.widgets']
)

a = Analysis(
    ['main_ctk.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='TroLyLichTrinhV2_v1.0.3',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
