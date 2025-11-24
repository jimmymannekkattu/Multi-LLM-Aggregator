#!/bin/bash
# AI Nexus - Desktop App Build Script
# Builds native desktop applications for all platforms

set -e  # Exit on error

echo "======================================"
echo "  AI Nexus Desktop App Builder"
echo "======================================"
echo ""

# Check if we're in the desktop directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Must run from desktop/ directory"
    exit 1
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js not found. Please install Node.js 16+"
    exit 1
fi

echo "✅ Node.js version: $(node --version)"

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Parse command line arguments
BUILD_TARGET="${1:-current}"

case $BUILD_TARGET in
    win|windows)
        echo "🪟 Building for Windows..."
        npm run build:win
        echo "✅ Windows build complete!"
        echo "📁 Output: dist/*.exe"
        ;;
    mac|macos|darwin)
        echo "🍎 Building for macOS..."
        npm run build:mac
        echo "✅ macOS build complete!"
        echo "📁 Output: dist/*.dmg, dist/*.zip"
        ;;
    linux)
        echo "🐧 Building for Linux..."
        npm run build:linux
        echo "✅ Linux build complete!"
        echo "📁 Output: dist/*.AppImage, dist/*.deb, dist/*.rpm"
        ;;
    all)
        echo "🌍 Building for all platforms..."
        npm run build:all
        echo "✅ All builds complete!"
        echo "📁 Output: dist/*"
        ;;
    current)
        echo "💻 Building for current platform..."
        npm run build
        echo "✅ Build complete!"
        echo "📁 Output: dist/*"
        ;;
    *)
        echo "Usage: $0 [win|mac|linux|all|current]"
        echo ""
        echo "Examples:"
        echo "  $0          # Build for current platform"
        echo "  $0 win      # Build for Windows"
        echo "  $0 mac      # Build for macOS"
        echo "  $0 linux    # Build for Linux"
        echo "  $0 all      # Build for all platforms"
        exit 1
        ;;
esac

echo ""
echo "🎉 Build successful!"
echo ""
echo "To run the app:"
echo "  npm start"
echo ""
echo "To test the built app:"
echo "  Open the file in dist/ folder"
