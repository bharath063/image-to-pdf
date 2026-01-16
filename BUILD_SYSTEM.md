# Build System Documentation

This document explains the automated build system for creating installers across macOS, Linux, and Windows platforms.

## Overview

The project uses GitHub Actions to automatically build platform-specific installers when code is merged to the main branch. The build system leverages:

- **UV**: For fast, reliable Python dependency management
- **PyInstaller**: For creating standalone executables
- **GitHub Actions**: For CI/CD automation

## Files Created

### 1. `.github/workflows/build-installers.yml`
The main GitHub Actions workflow file that orchestrates the build process.

**Triggers:**
- Push to `main` or `master` branch (after PR merge)
- Manual workflow dispatch (via GitHub UI)

**Build Matrix:**
- macOS (latest)
- Ubuntu Linux (latest)
- Windows (latest)

**Workflow Steps:**
1. Checkout code
2. Set up Python 3.12
3. Install UV package manager
4. Create virtual environment
5. Install dependencies
6. Build with PyInstaller
7. Package application
8. Upload artifacts

### 2. `ImageToPDF.spec`
PyInstaller specification file that defines how to bundle the application.

**Key Features:**
- Includes PyQt6 hidden imports
- Configures windowed mode (no console)
- Creates macOS .app bundle
- Optimizes with UPX compression

### 3. `pyproject.toml` (Updated)
Added development dependencies section:

```toml
[project.optional-dependencies]
dev = [
    "pyinstaller>=6.0.0",
]
```

### 4. `.gitignore`
Ignores build artifacts, virtual environments, and temporary files.

### 5. `build_local.sh` (Unix/macOS)
Local build script for testing on Unix-like systems.

**Usage:**
```bash
./build_local.sh
```

### 6. `build_local.ps1` (Windows)
Local build script for testing on Windows.

**Usage:**
```powershell
.\build_local.ps1
```

### 7. `README.md` (Updated)
Comprehensive documentation including:
- Features
- Installation instructions
- Development guide
- CI/CD documentation

## Platform-Specific Details

### macOS
- **Output**: `ImageToPDF.app` (macOS application bundle)
- **Package**: `ImageToPDF.app.zip`
- **Installation**: Unzip and drag to Applications folder
- **Notes**: The .app bundle includes all dependencies

### Linux
- **Output**: `ImageToPDF/` (directory with executable and dependencies)
- **Package**: `ImageToPDF-linux.tar.gz`
- **Installation**: Extract and run the executable
- **Dependencies**: Qt6 libraries are installed via apt during build

### Windows
- **Output**: `ImageToPDF/` (directory with .exe and dependencies)
- **Package**: `ImageToPDF-windows.zip`
- **Installation**: Extract and run `ImageToPDF.exe`
- **Notes**: No additional installation required

## Testing the Build System

### Local Testing

**On macOS/Linux:**
```bash
# Make script executable (first time only)
chmod +x build_local.sh

# Run build
./build_local.sh

# Test the application
open dist/ImageToPDF.app  # macOS
./dist/ImageToPDF/ImageToPDF  # Linux
```

**On Windows:**
```powershell
# Run build
.\build_local.ps1

# Test the application
.\dist\ImageToPDF\ImageToPDF.exe
```

### GitHub Actions Testing

1. Push to a feature branch
2. Create a Pull Request to main
3. Merge the PR
4. Go to Actions tab to watch the build
5. Download artifacts once complete

Or trigger manually:
1. Go to Actions tab
2. Select "Build Installers" workflow
3. Click "Run workflow"
4. Select branch and run

## Troubleshooting

### Build Fails on Linux
**Issue**: Missing Qt6 libraries
**Solution**: The workflow includes all necessary dependencies. If building locally, install:
```bash
sudo apt-get install libxcb-xinerama0 libxcb-cursor0 libxkbcommon-x11-0
```

### UV Installation Fails
**Issue**: UV not found in PATH
**Solution**: The workflow adds UV to PATH automatically. If building locally, ensure UV is installed:
```bash
# Unix/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
irm https://astral.sh/uv/install.ps1 | iex
```

### PyInstaller Build Fails
**Issue**: Hidden imports not found
**Solution**: Check `ImageToPDF.spec` and add missing imports to `hiddenimports` list.

### Application Won't Launch
**Issue**: Missing dependencies
**Solution**: 
- macOS: Check Console.app for error messages
- Linux: Run from terminal to see error output
- Windows: Check Event Viewer

## Customization

### Adding Dependencies

1. Update `pyproject.toml`:
```toml
dependencies = [
    "pillow>=12.1.0",
    "pyqt6>=6.10.2",
    "your-new-package>=1.0.0",
]
```

2. Update `ImageToPDF.spec` if needed (add hidden imports)

3. Commit and push - builds will automatically include new dependencies

### Changing Application Icon

1. Create icons for each platform:
   - macOS: `.icns` file
   - Windows: `.ico` file
   - Linux: `.png` file

2. Update `ImageToPDF.spec`:
```python
app = BUNDLE(
    ...
    icon='path/to/icon.icns',
    ...
)
```

### Build Optimization

To reduce build size, edit `ImageToPDF.spec`:

```python
a = Analysis(
    ...
    excludes=['module_to_exclude'],
    ...
)
```

## Artifact Retention

Build artifacts are automatically retained for **30 days**. After this period, they are automatically deleted by GitHub.

To change retention:
```yaml
- name: Upload artifact
  uses: actions/upload-artifact@v4
  with:
    retention-days: 90  # Change to desired number
```

## Release Creation

To create a GitHub Release with installers:

1. Create and push a tag:
```bash
git tag v1.0.0
git push origin v1.0.0
```

2. Update workflow to trigger on tags (optional):
```yaml
on:
  push:
    tags:
      - 'v*'
```

3. Add release creation step to workflow:
```yaml
- name: Create Release
  uses: softprops/action-gh-release@v1
  if: startsWith(github.ref, 'refs/tags/')
  with:
    files: dist/*
```

## Performance

Typical build times:
- **macOS**: ~5-7 minutes
- **Linux**: ~4-6 minutes
- **Windows**: ~6-8 minutes

Total workflow time: ~8-10 minutes (builds run in parallel)

## Security Considerations

1. **Dependencies**: UV ensures reproducible builds with locked dependencies
2. **Artifacts**: Build artifacts are only accessible to repository collaborators
3. **Code Signing**: Not implemented (consider for production releases)

## Future Improvements

Potential enhancements:
- [ ] Code signing for macOS and Windows
- [ ] Notarization for macOS
- [ ] Create installers (DMG for macOS, MSI for Windows, AppImage for Linux)
- [ ] Automated testing before build
- [ ] Version number automation
- [ ] Release notes generation

## Support

For issues with the build system:
1. Check GitHub Actions logs
2. Test locally using build scripts
3. Verify dependencies in `pyproject.toml`
4. Check PyInstaller configuration in `ImageToPDF.spec`
