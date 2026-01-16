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

## CI/CD

This project uses GitHub Actions to automatically build installers for all platforms when code is merged to the main branch.

### Workflow Details

- **Triggers**: Push to `main` or `master` branch, or manual workflow dispatch
- **Platforms**: macOS, Linux (Ubuntu), Windows
- **Build Tool**: PyInstaller
- **Dependency Management**: UV
- **Artifacts**: Automatically uploaded and available for 30 days

### How It Works

1. Code is merged to main branch
2. GitHub Actions workflow triggers
3. Three parallel jobs run (one per platform)
4. Each job:
   - Sets up Python 3.12
   - Installs UV package manager
   - Installs project dependencies
   - Builds standalone executable with PyInstaller
   - Packages the application (zip/tar.gz)
   - Uploads artifacts

### Downloading Build Artifacts

After a successful build:
1. Go to the [Actions](../../actions) tab
2. Click on the latest workflow run
3. Scroll to "Artifacts" section
4. Download the installer for your platform

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
