# PyInstaller runtime hook for Qt6
# This sets up Qt environment correctly in the frozen app BEFORE Qt initializes
# CRITICAL: This must run before any Qt imports

import os
import sys

# Get the directory where the frozen app is running
if getattr(sys, 'frozen', False):
    bundle_dir = sys._MEIPASS
    
    # CRITICAL for macOS: Set these BEFORE Qt loads to prevent CFBundle crashes
    # Qt6 on macOS needs these paths set via environment variables
    os.environ['QT_MAC_WANTS_LAYER'] = '1'
    
    # Set Qt plugin path
    qt_plugins_path = os.path.join(bundle_dir, 'PyQt6', 'Qt6', 'plugins')
    if os.path.exists(qt_plugins_path):
        os.environ['QT_PLUGIN_PATH'] = qt_plugins_path
    
    # Set QtCore library path to prevent CFBundle lookup failures
    # This tells Qt where to find its libraries without using CoreFoundation
    qt_prefix = os.path.join(bundle_dir, 'PyQt6', 'Qt6')
    if os.path.exists(qt_prefix):
        os.environ['QT6_PREFIX_PATH'] = qt_prefix
        
        # Also set individual Qt paths
        for path_name, subdir in [
            ('QT_QPA_PLATFORM_PLUGIN_PATH', 'plugins/platforms'),
            ('QT_PLUGIN_PATH', 'plugins'),
        ]:
            full_path = os.path.join(qt_prefix, subdir)
            if os.path.exists(full_path):
                os.environ[path_name] = full_path
