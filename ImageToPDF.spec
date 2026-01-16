# -*- mode: python ; coding: utf-8 -*-
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Collect PyQt6 data files and plugins
pyqt6_datas = collect_data_files('PyQt6')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=pyqt6_datas,
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'PyQt6.sip',
        'PIL._imaging',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['pyi_rth_qt6.py'],
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
    [],
    exclude_binaries=True,
    name='ImageToPDF',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ImageToPDF',
)

app = BUNDLE(
    coll,
    name='ImageToPDF.app',
    icon=None,
    bundle_identifier='com.imagetopdf.app',
    info_plist={
        'CFBundleName': 'ImageToPDF',
        'CFBundleDisplayName': 'Image to PDF',
        'CFBundleIdentifier': 'com.imagetopdf.app',
        'CFBundleVersion': '0.2.0',
        'CFBundleShortVersionString': '0.2.0',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.13',
        'NSRequiresAquaSystemAppearance': False,
    },
)
