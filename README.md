# Image to PDF Converter

A modern, user-friendly desktop application to convert images to PDF files. Built with PyQt6 and Python.

## Features

- 📁 **Drag & Drop Support**: Simply drag images into the app
- 🔄 **Reorder Pages**: Drag images to reorder pages in your PDF
- 👁️ **Preview**: Preview your PDF before generating
- 🎨 **Beautiful UI**: Modern dark-themed interface
- 📄 **Multiple Formats**: Supports JPG, PNG, BMP, WEBP, and TIFF
- 🗑️ **Remove Images**: Select and remove unwanted images

## Installation

### From Pre-built Installers

Download the latest installer for your platform from the [Releases](../../releases) page:

- **macOS**: Download `ImageToPDF.app.zip`, unzip, and drag to Applications
- **Linux**: Download `ImageToPDF-linux.tar.gz`, extract, and run the executable
- **Windows**: Download `ImageToPDF-windows.zip`, extract, and run `ImageToPDF.exe`

### From Source

#### Prerequisites

- Python 3.12 or higher
- [UV](https://docs.astral.sh/uv/) package manager

#### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/img-to-pdf.git
cd img-to-pdf

# Install dependencies with UV
uv venv
uv pip install -e .

# Run the application
uv run python main.py
```

## Development

### Building Installers Locally

```bash
# Install development dependencies
uv pip install -e ".[dev]"

# Build with PyInstaller
pyinstaller --clean --noconfirm ImageToPDF.spec
```

The built application will be in the `dist/` directory.

### Project Structure

```
img-to-pdf/
├── main.py              # Main application code
├── ImageToPDF.spec      # PyInstaller configuration
├── pyproject.toml       # Project dependencies
└── .github/
    └── workflows/
        └── build-installers.yml  # CI/CD for building installers
```

## 🤖 Automated CI/CD

This project uses **fully automated CI/CD** - just push your code and get releases automatically!

### ✨ How It Works

Every push to `main` automatically:
1. 📊 **Analyzes** your commit messages
2. 🔢 **Bumps** the version (major/minor/patch)
3. 📝 **Updates** `pyproject.toml`
4. 🏷️ **Creates** a git tag
5. 🏗️ **Builds** installers for macOS, Linux, and Windows
6. 🚀 **Publishes** a GitHub Release with all installers

**No manual versioning needed!** Just use proper commit messages:

```bash
git commit -m "fix: resolve crash bug"        # → Patch bump (0.0.X)
git commit -m "feat: add new feature"         # → Minor bump (0.X.0)
git commit -m "feat!: breaking changes"       # → Major bump (X.0.0)
```

### 📚 Documentation

- **[CI_CD_GUIDE.md](CI_CD_GUIDE.md)** - Complete CI/CD guide with examples and troubleshooting
- **[RELEASING.md](RELEASING.md)** - Manual release instructions (if needed)
- **[BUILD_SYSTEM.md](BUILD_SYSTEM.md)** - Build system documentation

### 🎯 Quick Start for Developers

```bash
# 1. Make your changes
git add .

# 2. Commit with proper format
git commit -m "feat: add dark mode support"

# 3. Push to main
git push origin main

# 4. Done! Check the Releases page in ~5 minutes
```

### 📦 Downloading Installers

**From Releases:**
1. Go to [Releases](../../releases)
2. Download the latest version for your platform:
   - `ImageToPDF-X.Y.Z-macos.zip` for macOS
   - `ImageToPDF-X.Y.Z-linux.tar.gz` for Linux
   - `ImageToPDF-X.Y.Z-windows.zip` for Windows

### 🔍 Workflow Details

- **Version Detection**: Conventional Commits format
- **Platforms**: macOS (ARM64), Linux (x86_64), Windows (x86_64)
- **Build Tool**: PyInstaller 6.18+
- **Dependency Management**: UV
- **Release Notes**: Auto-generated from commits
- **Build Time**: ~5-10 minutes per release

## Usage

1. **Launch the application**
2. **Add images**: Click "➕ Add Images" or drag & drop images
3. **Reorder**: Drag images to reorder pages
4. **Remove**: Select images and click "🗑 Remove Selected"
5. **Preview**: Click "👁 Preview PDF" to see how it will look
6. **Generate**: Click "📄 Generate PDF" and choose save location

## Requirements

- Python 3.12+
- PyQt6 6.10.2+
- Pillow 12.1.0+

## License

MIT License - feel free to use this project however you'd like!

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
