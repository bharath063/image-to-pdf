#!/bin/bash
# Local build script for testing PyInstaller builds

set -e

echo "🔨 Building ImageToPDF locally..."
echo ""

# Check if UV is installed
if ! command -v uv &> /dev/null; then
    echo "❌ UV is not installed. Please install it first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    uv venv
fi

# Install dependencies
echo "📦 Installing dependencies..."
uv pip install -e ".[dev]"

# Build with PyInstaller
echo "🏗️  Building with PyInstaller..."
source .venv/bin/activate
pyinstaller --clean --noconfirm ImageToPDF.spec

echo ""
echo "✅ Build complete!"
echo "📁 Output location: dist/ImageToPDF.app (macOS) or dist/ImageToPDF/ (Linux/Windows)"
echo ""
echo "To run the built application:"
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "   open dist/ImageToPDF.app"
else
    echo "   ./dist/ImageToPDF/ImageToPDF"
fi
