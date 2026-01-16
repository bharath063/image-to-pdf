# Local build script for testing PyInstaller builds on Windows

Write-Host "🔨 Building ImageToPDF locally..." -ForegroundColor Cyan
Write-Host ""

# Check if UV is installed
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "❌ UV is not installed. Please install it first:" -ForegroundColor Red
    Write-Host "   irm https://astral.sh/uv/install.ps1 | iex" -ForegroundColor Yellow
    exit 1
}

# Create virtual environment if it doesn't exist
if (-not (Test-Path ".venv")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    uv venv
}

# Install dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
uv pip install -e ".[dev]"

# Build with PyInstaller
Write-Host "🏗️  Building with PyInstaller..." -ForegroundColor Yellow
.\.venv\Scripts\Activate.ps1
pyinstaller --clean --noconfirm ImageToPDF.spec

Write-Host ""
Write-Host "✅ Build complete!" -ForegroundColor Green
Write-Host "📁 Output location: dist\ImageToPDF\" -ForegroundColor Cyan
Write-Host ""
Write-Host "To run the built application:" -ForegroundColor Cyan
Write-Host "   .\dist\ImageToPDF\ImageToPDF.exe" -ForegroundColor White
