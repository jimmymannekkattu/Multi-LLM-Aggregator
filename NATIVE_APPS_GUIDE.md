# 📱 AI Nexus - Native Apps Build Guide

## Overview

AI Nexus now has **native applications** for all major platforms:

### Desktop Apps (Electron-based)
- ✅ **Windows** - `.exe` installer (NSIS) and portable version
- ✅ **macOS** - `.dmg` installer and `.zip`
- ✅ **Linux** - AppImage, `.deb`, and `.rpm` packages

### Mobile Apps (React Native)
- ✅ **Android** - `.apk` and `.aab` (Play Store ready)
- ✅ **iOS** - `.ipa` (App Store ready)

---

## 🖥️ Desktop Apps (Windows, macOS, Linux)

### Prerequisites

```bash
# Install Node.js 16+ (https://nodejs.org)
node --version  # Should be v16 or higher

# Navigate to desktop directory
cd desktop
```

### Installation

```bash
# Install dependencies
npm install
```

### Development Mode

```bash
# Run in development  
npm start

# This will:
# 1. Start Electron app
# 2. Load the chat interface
# 3. Hot-reload on changes
```

### Building for Distribution

#### Build for Current Platform
```bash
npm run build
```

#### Build for Specific Platforms

**Windows:**
```bash
npm run build:win
```
Output: `dist/AI Nexus Setup 1.0.0.exe` and `dist/AI Nexus 1.0.0.exe` (portable)

**macOS:**
```bash
npm run build:mac
```
Output: `dist/AI Nexus-1.0.0.dmg` and `dist/AI Nexus-1.0.0-mac.zip`

**Linux:**
```bash
npm run build:linux
```
Output: 
- `dist/AI Nexus-1.0.0.AppImage`
- `dist/ai-nexus_1.0.0_amd64.deb`
- `dist/ai-nexus-1.0.0.x86_64.rpm`

#### Build for All Platforms (requires each OS or CI/CD)
```bash
npm run build:all
```

### Features

- ✅ **Multiple Interface Modes**
  - Web Chat Interface (chat-full.html)
  - Desktop App (Streamlit)
  - Landing Page

- ✅ **Built-in Menu System**
  - File → Reload, DevTools, Exit
  - View → Switch interfaces, Zoom controls
  - Settings → Server configuration
  - Help → Documentation, About

- ✅ **Auto-Update Ready** (configure in package.json)

- ✅ **Platform-Specific Features**
  - Windows: Start menu integration, taskbar  
  - macOS: Dock integration, native window
  - Linux: Desktop file, system integration

### Customization

#### Change App Icon

1. Replace icons in `desktop/build/`:
   - `icon.ico` - Windows (256x256)
   - `icon.icns` - macOS (512x512)  
   - `icon.png` - Linux (512x512)

2. Use tools:
   - **Windows**: Use `png2ico` or online converters
   - **macOS**: Use `png2icns` or Icon Composer
   - **Linux**: Just use PNG file

#### Modify Window Size/Appearance

Edit `desktop/main.js`:
```javascript
const mainWindow = new BrowserWindow({
    width: 1400,  // Change width
    height: 900,  // Change height
    // ... other options
});
```

---

## 📱 Mobile Apps (Android & iOS)

### Prerequisites

#### For Both Platforms
```bash
# Install Node.js 16+
node --version

# Install React Native CLI
npm install -g react-native-cli

# Navigate to mobile app directory
cd mobile-app
```

#### For Android
```bash
# Install Android Studio
# Download from: https://developer.android.com/studio

# Set ANDROID_HOME environment variable
export ANDROID_HOME=$HOME/Android/Sdk
export PATH=$PATH:$ANDROID_HOME/emulator
export PATH=$PATH:$ANDROID_HOME/tools
export PATH=$PATH:$ANDROID_HOME/tools/bin
export PATH=$PATH:$ANDROID_HOME/platform-tools
```

#### For iOS (macOS only)
```bash
# Install Xcode from Mac App Store
# Install CocoaPods
sudo gem install cocoapods

# Install iOS dependencies
cd mobile-app/ios
pod install
cd ..
```

### Installation

```bash
# Install dependencies
npm install
```

### Development Mode

#### Android
```bash
# Start Metro bundler
npm start

# In another terminal, run on Android
npm run android

# Or run on specific device
adb devices  # List devices
npx react-native run-android --deviceId=DEVICE_ID
```

#### iOS
```bash
# Start Metro bundler
npm start

# In another terminal, run on iOS
npm run ios

# Or specific simulator
npx react-native run-ios --simulator="iPhone 15 Pro"
```

### Building for Production

#### Android APK (for testing/sideload)

```bash
# Build release APK
npm run build:android

# Output: android/app/build/outputs/apk/release/app-release.apk
```

#### Android AAB (for Play Store)

```bash
cd android

# Generate release bundle
./gradlew bundleRelease

# Output: app/build/outputs/bundle/release/app-release.aab
```

**Sign the APK/AAB:**
```bash
# Generate keystore (first time only)
keytool -genkey -v -keystore my-release-key.keystore -alias my-key-alias -keyalg RSA -keysize 2048 -validity 10000

# Configure in android/gradle.properties:
MYAPP_RELEASE_STORE_FILE=my-release-key.keystore
MYAPP_RELEASE_KEY_ALIAS=my-key-alias
MYAPP_RELEASE_STORE_PASSWORD=*****
MYAPP_RELEASE_KEY_PASSWORD=*****
```

#### iOS IPA (for App Store)

```bash
# Open Xcode
cd ios
open AIexusMobile.xcworkspace

# In Xcode:
# 1. Select "Any iOS Device" as target
# 2. Product → Archive
# 3. Distribute App → App Store Connect
# 4. Follow prompts to upload
```

### Features

- ✅ **Native UI** - Platform-specific components
- ✅ **Dark Theme** - Modern, consistent with desktop
- ✅ **Real-time Chat** - Full API integration
- ✅ **QR Code Scanner** - Scan server URL (planned)
- ✅ **Markdown Support** - Rich text responses
- ✅ **Persistent Settings** - AsyncStorage
- ✅ **Auto-reconnect** - Smart server detection

### Configuration

#### Change API URL

The app remembers the last used server URL. To set default:

Edit `mobile-app/App.js`:
```javascript
const [apiUrl, setApiUrl] = useState('http://YOUR_SERVER_IP:8000');
```

#### App Icons and Splash Screens

**Android:**
- Icons: `android/app/src/main/res/mipmap-*/ic_launcher.png`
- Use Android Studio's Asset Studio for generation

**iOS:**
- Icons: `ios/AIexusMobile/Images.xcassets/AppIcon.appiconset/`
- Use Xcode's asset catalog

### Publishing

#### Google Play Store

1. Create Developer Account ($25 one-time fee)
2. Build signed AAB
3. Upload to Play Console
4. Fill in store listing
5. Submit for review

#### Apple App Store

1. Enroll in Apple Developer Program ($99/year)
2. Create App ID in Developer Portal
3. Build and archive in Xcode
4. Upload to App Store Connect
5. Fill in app information
6. Submit for review

---

## 🔧 Advanced Configuration

### Desktop App - Server Auto-Start

To make desktop app start backend automatically, modify `desktop/main.js`:

```javascript
const { spawn } = require('child_process');

let serverProcess;

function startServer() {
    serverProcess = spawn('python3', ['start.py'], {
        cwd: path.join(__dirname, '..')
    });
    
    serverProcess.stdout.on('data', (data) => {
        console.log(`Server: ${data}`);
    });
}

// Call in app.whenReady()
app.whenReady().then(() => {
    startServer();
    setTimeout(createWindow, 5000); // Wait for server
});

// Kill server on quit
app.on('quit', () => {
    if (serverProcess) {
        serverProcess.kill();
    }
});
```

### Mobile App - Deep Linking

Enable `ainexus://` URLs to open the app:

**Android** - Add to `android/app/src/main/AndroidManifest.xml`:
```xml
<intent-filter>
    <action android:name="android.intent.action.VIEW" />
    <category android:name="android.intent.category.DEFAULT" />
    <category android:name="android.intent.category.BROWSABLE" />
    <data android:scheme="ainexus" />
</intent-filter>
```

**iOS** - Add to `ios/AIexusMobile/Info.plist`:
```xml
<key>CFBundleURLTypes</key>
<array>
    <dict>
        <key>CFBundleURLSchemes</key>
        <array>
            <string>ainexus</string>
        </array>
    </dict>
</array>
```

---

## 📊 File Structure

### Desktop App
```
desktop/
├── main.js              # Main Electron process
├── preload.js           # Secure bridge to renderer
├── package.json         # Dependencies and build config
├── build/               # Icons and assets
│   ├── icon.ico        # Windows icon
│   ├── icon.icns       # macOS icon
│   └── icon.png        # Linux icon
└── dist/               # Built apps (generated)
```

### Mobile App
```
mobile-app/
├── App.js              # Main React Native component
├── package.json        # Dependencies
├── android/            # Android-specific code
│   ├── app/
│   │   └── build/      # Built APKs/AABs
│   └── gradle/
└── ios/                # iOS-specific code
    ├── AIexusMobile.xcworkspace
    └── AIexusMobile/
```

---

## 🐛 Troubleshooting

### Desktop App

**"Module not found" errors:**
```bash
cd desktop
rm -rf node_modules package-lock.json
npm install
```

**Build fails:**
- Ensure you have electron-builder: `npm install -D electron-builder`
- Check platform-specific requirements in electron-builder docs

**App doesn't connect to server:**
- Ensure backend is running: `python3 start.py`
- Check API URL in settings
- Run network diagnostic: `python3 diagnose_network.py`

### Mobile App

**Android build fails:**
- Run `cd android && ./gradlew clean`
- Check Java version: `java -version` (need JDK 11 or 17)
- Verify ANDROID_HOME is set

**iOS build fails:**
- Run `cd ios && pod install`
- Open in Xcode and check for issues
- Ensure Xcode Command Line Tools installed

**Metro bundler issues:**
```bash
# Clear cache
npm start -- --reset-cache

# Or
react-native start --reset-cache
```

**App crashes on launch:**
- Check server URL is correct
- Ensure server is accessible from mobile device
- Check logs: `npx react-native log-android` or `npx react-native log-ios`

---

## 📦 Distribution Checklist

### Desktop
- [ ] Icons created for all platforms
- [ ] Version bumped in package.json
- [ ] Code signed (for macOS and Windows)
- [ ] Tested on target OS
- [ ] Installer tested
- [ ] Auto-update configured (optional)

### Mobile
- [ ] App icons created
- [ ] Splash screens created
- [ ] Version code and name updated
- [ ] Signed with release keystore
- [ ] Tested on physical devices
- [ ] Screenshots for store listings
- [ ] Privacy policy URL ready
- [ ] Store listings written

---

## 🚀 Quick Commands Reference

### Desktop
```bash
# Development
cd desktop && npm start

# Build current platform
npm run build

# Build all
npm run build:all
```

### Android
```bash
# Development
cd mobile-app && npm run android

# Production APK
npm run build:android
```

### iOS
```bash
# Development
cd mobile-app && npm run ios

# Production (via Xcode)
cd ios && open AIexusMobile.xcworkspace
```

---

## 📞 Support

- **Desktop Issues**: See `desktop/README.md`
- **Mobile Issues**: See `mobile-app/README.md`
- **General**: See main `PORTABILITY.md`
- **GitHub**: [Repository Issues](https://github.com/your-repo/issues)

---

**Your AI Nexus is now available as native apps on ALL platforms!** 🎉
