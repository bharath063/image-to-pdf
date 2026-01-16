# PyInstaller runtime hook for Qt6
# This sets up Qt plugin paths correctly in the frozen app

import os
import sys

# Get the directory where the frozen app is running
if getattr(sys, 'frozen', False):
    bundle_dir = sys._MEIPASS
    
    # Set Qt plugin path
    qt_plugins_path = os.path.join(bundle_dir, 'PyQt6', 'Qt6', 'plugins')
    if os.path.exists(qt_plugins_path):
        os.environ['QT_PLUGIN_PATH'] = qt_plugins_path
    
    # Set Qt to use software rendering if needed (helps with compatibility)
    # os.environ['QT_MAC_WANTS_LAYER'] = '1'
