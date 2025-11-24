# AI Nexus Desktop App

Native desktop application for AI Nexus built with Electron.

## Features

- ✅ **Cross-platform**: Windows, macOS, Linux
- ✅ **Multiple interfaces**: Web Chat, Streamlit App, Landing Page
- ✅ **Native menus**: Platform-specific menu integration
- ✅ **Auto-update ready**: Built-in update mechanism
- ✅ **Persistent settings**: Remembers your preferences
- ✅ **Offline-ready**: Can run with local server

## Quick Start

### Development

```bash
# Install dependencies
npm install

# Run in development mode
npm start
```

### Building

```bash
# Build for current platform
npm run build

# Build for specific platform
npm run build:win      # Windows
npm run build:mac      # macOS
npm run build:linux    # Linux

# Build for all platforms
npm run build:all
```

### Build Scripts

**Linux/macOS:**
```bash
chmod +x build.sh
./build.sh [win|mac|linux|all]
```

**Windows:**
```cmd
build.bat [win|all]
```

## Project Structure

```
desktop/
├── main.js              # Main Electron process
├── preload.js           # Secure IPC bridge
├── package.json         # Configuration and dependencies
├── build.sh             # Unix build script
├── build.bat            # Windows build script
├── build/               # Assets
│   ├── icon.ico        # Windows icon (256x256)
│   ├── icon.icns       # macOS icon (512x512)
│   └── icon.png        # Linux icon (512x512)
└── dist/               # Built applications (auto-generated)
```

## Requirements

- **Node.js** 16 or higher
- **npm** 7 or higher

### Platform-Specific Requirements

**Windows:**
- No additional requirements

**macOS:**
- Xcode Command Line Tools (for codesigning)

**Linux:**
- Standard development tools (`build-essential`)

## Configuration

### Change Default Server URL

Edit `main.js`:
```javascript
const DEFAULT_API_URL = 'http://your-server:8000';
```

### Customize Window

Edit `main.js`:
```javascript
new BrowserWindow({
    width: 1400,      // Your width
    height: 900,      // Your height
    // ...
});
```

### Change App Icons

Replace files in `build/` directory:
- `icon.ico` - Windows (256x256 or multi-size)
- `icon.icns` - macOS (512x512, created with `png2icns`)
- `icon.png` - Linux (512x512 PNG)

## Features

### Menu System

- **File**
  - Reload / Force Reload
  - Toggle DevTools
  - Exit

- **View**
  - Switch between interfaces (Chat/Streamlit/Landing)
  - Zoom In/Out/Reset

- **Settings**
  - Server Configuration
  - Check Server Status
  - Clear Cache

- **Help**
  - Documentation
  - Report Issue
  - About

### Keyboard Shortcuts

- `Ctrl/Cmd + R` - Reload
- `Ctrl/Cmd + Shift + R` - Force Reload
- `Ctrl/Cmd + Shift + I` - Toggle DevTools
- `Ctrl/Cmd + Q` - Quit
- `Ctrl/Cmd + Plus` - Zoom In
- `Ctrl/Cmd + Minus` - Zoom Out
- `Ctrl/Cmd + 0` - Reset Zoom

## Distribution

### Windows

Built files in `dist/`:
- `AI Nexus Setup 1.0.0.exe` - Installer
- `AI Nexus 1.0.0.exe` - Portable version

### macOS

Built files in `dist/`:
- `AI Nexus-1.0.0.dmg` - Disk image
- `AI Nexus-1.0.0-mac.zip` - Zipped app

### Linux

Built files in `dist/`:
- `AI Nexus-1.0.0.AppImage` - Universal package
- `ai-nexus_1.0.0_amd64.deb` - Debian/Ubuntu
- `ai-nexus-1.0.0.x86_64.rpm` - RedHat/Fedora

## Troubleshooting

### Module Not Found

```bash
rm -rf node_modules package-lock.json
npm install
```

### Build Fails

```bash
# Clean and rebuild
rm -rf dist node_modules
npm install
npm run build
```

### App Won't Connect to Server

1. Ensure backend is running: `python3 start.py`
2. Check server status in Settings menu
3. Verify API URL in Settings

## Advanced

### Auto-Start Backend

Modify `main.js` to spawn the Python server automatically:

```javascript
const { spawn } = require('child_process');
const serverProcess = spawn('python3', ['start.py'], {
    cwd: path.join(__dirname, '..')
});
```

### Code Signing

**macOS:**
```bash
export CSC_LINK=/path/to/certificate.p12
export CSC_KEY_PASSWORD=your_password
npm run build:mac
```

**Windows:**
```bash
export CSC_LINK=/path/to/certificate.pfx
export CSC_KEY_PASSWORD=your_password
npm run build:win
```

## See Also

- [Main Documentation](../NATIVE_APPS_GUIDE.md)
- [Portability Guide](../PORTABILITY.md)
- [Electron Documentation](https://www.electronjs.org/docs)

## Support

For issues, see the main project [GitHub Issues](https://github.com/your-repo/issues)
