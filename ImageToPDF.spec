# -*- mode: python ; coding: utf-8 -*-
import sys
import os
from pathlib import Path

block_cipher = None

# Only collect essential Qt plugins (not all data files)
def get_qt_plugins():
    """Get only the Qt plugins we actually need"""
    from PyQt6 import QtCore
    qt_plugins_dir = Path(QtCore.__file__).parent / 'Qt6' / 'plugins'
    
    plugins = []
    # Only include essential plugins
    for plugin_type in ['platforms', 'styles', 'imageformats']:
        plugin_path = qt_plugins_dir / plugin_type
        if plugin_path.exists():
            plugins.append((str(plugin_path), f'PyQt6/Qt6/plugins/{plugin_type}'))
    
    return plugins

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=get_qt_plugins(),  # Only essential plugins
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
    excludes=[
        # Exclude unused modules to reduce size
        'tkinter',
        'unittest',
        'email',
        'http',
        'xml',
        'pydoc',
        'doctest',
        'argparse',
        'zipfile',
        'tarfile',
        'csv',
        'json',
        'sqlite3',
        'ssl',
        'bz2',
        'lzma',
        'socket',
        'select',
        # Qt modules we don't use
        'PyQt6.QtNetwork',
        'PyQt6.QtPrintSupport',
        'PyQt6.QtSql',
        'PyQt6.QtTest',
        'PyQt6.QtXml',
        'PyQt6.QtBluetooth',
        'PyQt6.QtDBus',
        'PyQt6.QtDesigner',
        'PyQt6.QtHelp',
        'PyQt6.QtMultimedia',
        'PyQt6.QtMultimediaWidgets',
        'PyQt6.QtOpenGL',
        'PyQt6.QtOpenGLWidgets',
        'PyQt6.QtPdf',
        'PyQt6.QtPdfWidgets',
        'PyQt6.QtPositioning',
        'PyQt6.QtQml',
        'PyQt6.QtQuick',
        'PyQt6.QtQuick3D',
        'PyQt6.QtQuickWidgets',
        'PyQt6.QtRemoteObjects',
        'PyQt6.QtSensors',
        'PyQt6.QtSerialPort',
        'PyQt6.QtSvg',
        'PyQt6.QtSvgWidgets',
        'PyQt6.QtWebChannel',
        'PyQt6.QtWebEngine',
        'PyQt6.QtWebEngineCore',
        'PyQt6.QtWebEngineWidgets',
        'PyQt6.QtWebSockets',
    ],
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
    strip=False,  # Disable strip - can cause issues on macOS
    upx=False,    # Disable UPX - not needed and can cause issues
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
    strip=False,  # Disable strip - causes issues with Qt plugins on macOS
    upx=False,    # Disable UPX compression - corrupts Qt plugins
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
