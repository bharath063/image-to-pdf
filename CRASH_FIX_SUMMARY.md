# macOS Crash Fix Summary

## 🐛 The Problem

The app was crashing immediately when downloaded from GitHub releases with this error:
```
Exception Type: EXC_BAD_ACCESS (SIGSEGV)
Exception Subtype: KERN_INVALID_ADDRESS at 0x0000000000000008

Thread 0 Crashed:
0   CoreFoundation      __CFCheckCFInfoPACSignature + 4
1   CoreFoundation      CFBundleCopyBundleURL + 24
2   QtCore             QLibraryInfoPrivate::paths(...) + 2164
```

**Root Cause**: Qt framework couldn't find its plugins and resources in the frozen app bundle.

## ✅ The Solution

### 1. Fixed PyInstaller Spec (`ImageToPDF.spec`)

**Added**:
- Qt data files collection
- PyQt6.sip hidden import
- Runtime hook for Qt path configuration
- Proper Info.plist with version and settings

**Changes**:
```python
# Now collects PyQt6 plugins and resources
pyqt6_datas = collect_data_files('PyQt6')

# Added runtime hook
runtime_hooks=['pyi_rth_qt6.py']

# Proper bundle info
info_plist={
    'CFBundleVersion': '0.2.0',
    'NSHighResolutionCapable': True,
    ...
}
```

### 2. Created Qt Runtime Hook (`pyi_rth_qt6.py`)

Sets up Qt plugin paths correctly when the app starts:
```python
# Sets QT_PLUGIN_PATH to the correct location in the bundle
qt_plugins_path = os.path.join(bundle_dir, 'PyQt6', 'Qt6', 'plugins')
os.environ['QT_PLUGIN_PATH'] = qt_plugins_path
```

### 3. Added Code Signing to Workflow

Updated `.github/workflows/release.yml` to add ad-hoc signature:
```yaml
- name: Code sign (macOS)
  run: |
    codesign --force --deep --sign - dist/ImageToPDF.app
    codesign --verify --verbose dist/ImageToPDF.app
```

### 4. Created User Guide (`MACOS_INSTALLATION.md`)

Instructions for users on how to open the app despite macOS security warnings.

## 🧪 Testing

### Test Locally:
```bash
# Rebuild with fixes
./build_local.sh

# Test the app
open dist/ImageToPDF.app

# Simulate downloaded app behavior
xattr -w com.apple.quarantine "0081;00000000;Chrome;" dist/ImageToPDF.app
open dist/ImageToPDF.app
```

### Test from Release:
1. Download from GitHub releases
2. Right-click → Open
3. App should launch without crashing

## 📋 Files Changed

1. **ImageToPDF.spec** - Fixed Qt bundling
2. **pyi_rth_qt6.py** (NEW) - Qt runtime configuration
3. **.github/workflows/release.yml** - Added code signing
4. **MACOS_INSTALLATION.md** (NEW) - User installation guide
5. **CRASH_FIX_SUMMARY.md** (NEW) - This file

## 🚀 Deployment

After committing these changes:

```bash
# Commit fixes
git add ImageToPDF.spec pyi_rth_qt6.py .github/workflows/release.yml MACOS_INSTALLATION.md
git commit -m "fix: resolve macOS crash on app launch with Qt plugin path configuration"
git push origin main

# A new release will be created automatically
# Test the downloaded app to verify the fix
```

## 🔍 Why It Works

1. **Qt Plugin Path**: The runtime hook tells Qt where to find its plugins
2. **Data Files**: PyInstaller now includes all Qt resource files
3. **Code Signing**: Ad-hoc signature satisfies basic macOS security
4. **Bundle Info**: Proper plist ensures macOS recognizes it as a valid app

## 📝 Technical Details

### What Was Missing

The original spec file didn't:
- Include Qt plugin files
- Set up Qt environment variables
- Have proper Info.plist configuration

### What Changed

The new spec file:
- Collects all PyQt6 data files and plugins
- Runs a hook to set `QT_PLUGIN_PATH` before Qt initialization
- Includes proper bundle metadata
- Has required hidden imports (PyQt6.sip)

### Why Local Build Worked

When built locally, Qt could find plugins because:
- Development environment has Qt installed system-wide
- Python environment variables were set correctly
- No quarantine attributes on local files

### Why Downloaded Build Failed

When downloaded from GitHub:
- macOS quarantine prevented plugin loading
- Qt paths weren't configured for frozen app
- Plugin files were missing from bundle

## ✅ Verification Checklist

- [ ] App builds successfully with new spec
- [ ] App launches when built locally
- [ ] App launches when downloaded from release
- [ ] No Qt plugin errors in console
- [ ] All UI elements render correctly
- [ ] PDF generation works
- [ ] File dialogs work

## 🎯 Expected Behavior

**Before Fix**:
- ❌ Crash immediately on launch
- ❌ Error: KERN_INVALID_ADDRESS
- ❌ Qt initialization failure

**After Fix**:
- ✅ App launches successfully
- ✅ Qt finds plugins correctly
- ✅ UI renders properly
- ✅ All features work

## 📞 If Issues Persist

If the app still crashes after these fixes:

1. Check Console.app for detailed error messages
2. Run from terminal: `./ImageToPDF.app/Contents/MacOS/ImageToPDF`
3. Verify Qt plugins are in the bundle:
   ```bash
   ls -la ImageToPDF.app/Contents/MacOS/PyQt6/Qt6/plugins/
   ```
4. Check if runtime hook is included:
   ```bash
   grep -r "QT_PLUGIN_PATH" ImageToPDF.app/
   ```

## 🎉 Success Indicators

You'll know it's fixed when:
- No crash on app launch
- Main window appears immediately
- No console errors about Qt plugins
- All buttons and UI elements work
