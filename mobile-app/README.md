# AI Nexus Mobile App

Native mobile application for AI Nexus built with React Native.

## Features

- ✅ **Cross-platform**: iOS and Android
- ✅ **Native UI**: Platform-specific components
- ✅ **Real-time chat**: Full API integration
- ✅ **Dark theme**: Modern, beautiful interface
- ✅ **Markdown support**: Rich text rendering
- ✅ **Persistent settings**: Remembers server URL and preferences
- ✅ **QR Scanner**: Scan server URL (planned feature)

## Quick Start

### Prerequisites

**Both Platforms:**
- Node.js 16+
- React Native CLI: `npm install -g react-native-cli`

**Android:**
- Android Studio
- Android SDK (API 31+)
- Java JDK 11 or 17

**iOS (macOS only):**
- Xcode 14+
- CocoaPods: `sudo gem install cocoapods`

### Installation

```bash
# Install dependencies
npm install

# For iOS only
cd ios && pod install && cd ..
```

### Development

**Android:**
```bash
# Start Metro bundler
npm start

# In another terminal
npm run android
```

**iOS:**
```bash
# Start Metro bundler
npm start

# In another terminal
npm run ios
```

## Building for Production

### Android APK

```bash
# Build unsigned APK for testing
cd android
./gradlew assembleRelease

# Output: android/app/build/outputs/apk/release/app-release.apk
```

### Android AAB (Play Store)

```bash
cd android
./gradlew bundleRelease

# Output: android/app/build/outputs/bundle/release/app-release.aab
```

**Sign the build:**

1. Generate keystore (first time):
```bash
keytool -genkey -v -keystore my-release-key.keystore \
  -alias my-key-alias -keyalg RSA -keysize 2048 -validity 10000
```

2. Configure in `android/gradle.properties`:
```properties
MYAPP_RELEASE_STORE_FILE=my-release-key.keystore
MYAPP_RELEASE_KEY_ALIAS=my-key-alias
MYAPP_RELEASE_STORE_PASSWORD=*****
MYAPP_RELEASE_KEY_PASSWORD=*****
```

3. Place keystore in `android/app/`

### iOS (via Xcode)

```bash
cd ios
open AIexusMobile.xcworkspace
```

In Xcode:
1. Select "Any iOS Device" as target
2. Product → Archive
3. Distribute App → App Store Connect / Ad Hoc / Enterprise

## Project Structure

```
mobile-app/
├── App.js                  # Main application component
├── package.json            # Dependencies and scripts
├── android/               # Android-specific code
│   ├── app/
│   │   ├── build.gradle   # App build config
│   │   └── src/main/
│   │       ├── AndroidManifest.xml
│   │       └── res/       # Resources (icons, etc.)
│   └── build/             # Build outputs
└── ios/                   # iOS-specific code
    ├── AIexusMobile.xcworkspace
    ├── AIexusMobile/
    │   ├── Info.plist
    │   └── Images.xcassets/  # App icons
    └── Pods/              # CocoaPods dependencies
```

## Configuration

### Change Default Server URL

Edit `App.js`:
```javascript
const [apiUrl, setApiUrl] = useState('http://192.168.1.100:8000');
```

### Change App Name

**Android** - `android/app/src/main/res/values/strings.xml`:
```xml
<string name="app_name">AI Nexus</string>
```

**iOS** - Xcode → Target → General → Display Name

### Change App Icons

**Android:**
- Use Android Studio → Right-click `res` → New → Image Asset
- Or replace files in `android/app/src/main/res/mipmap-*/`

**iOS:**
- Use Xcode → Assets.xcassets → AppIcon
- Or use design tools to generate all sizes

## Features

### Chat Interface
- Send messages to AI models
- Markdown-formatted responses
- Typing indicators
- Error handling

### Settings (planned)
- Server URL configuration
- Model selection
- Theme customization
- Cache management

### Connectivity
- Auto-detect server connection
- Visual connection status
- Graceful offline handling

## Dependencies

### Core
- `react-native` - Framework
- `react-navigation` - Navigation (planned)
- `axios` - HTTP client

### UI
- `react-native-markdown-display` - Markdown rendering
- `react-native-vector-icons` - Icons

### Storage
- `@react-native-async-storage/async-storage` - Persistent storage

### Planned
- `react-native-qrcode-scanner` - QR scanning
- `react-native-camera` - Camera access

## Troubleshooting

### Android

**Build fails:**
```bash
cd android
./gradlew clean
cd ..
npm run android
```

**Metro bundler issues:**
```bash
npm start -- --reset-cache
```

**ADB not finding device:**
```bash
adb devices
adb kill-server
adb start-server
```

### iOS

**Pod install fails:**
```bash
cd ios
pod deintegrate
pod install
cd ..
```

**Build fails in Xcode:**
- Clean build folder: Product → Clean Build Folder
- Delete derived data
- Restart Xcode

**Simulator not working:**
```bash
# Reset simulator
xcrun simctl erase all
```

### Both Platforms

**App crashes on launch:**
- Check server URL is accessible
- Check logs: `npx react-native log-android` or `npx react-native log-ios`
- Verify API server is running

**Cannot connect to server:**
- Ensure server is on same network
- Use computer's IP address, not `localhost`
- Check firewall settings
- Test with: `curl http://YOUR_IP:8000/health`

## Testing

### Run on Device

**Android:**
```bash
# Enable USB debugging on device
# Connect via USB
adb devices  # Should list your device
npm run android
```

**iOS:**
```bash
# In Xcode, select your device from dropdown
# Ensure device is trusted
npm run ios --device
```

### Run on Emulator

**Android:**
```bash
# List available emulators
emulator -list-avds

# Start emulator
emulator -avd YOUR_AVD_NAME &

# Run app
npm run android
```

**iOS:**
```bash
# List simulators
xcrun simctl list devices

# Run on specific simulator
npm run ios --simulator="iPhone 15 Pro"
```

## Publishing

### Google Play Store

1. Create Google Play Developer account ($25 one-time)
2. Build signed AAB: `cd android && ./gradlew bundleRelease`
3. Go to [Google Play Console](https://play.google.com/console)
4. Create new app
5. Fill in store listing, content rating, pricing
6. Upload AAB to production or testing track
7. Submit for review

### Apple App Store

1. Enroll in Apple Developer Program ($99/year)
2. Create app in [App Store Connect](https://appstoreconnect.apple.com)
3. Archive app in Xcode (Product → Archive)
4. Upload to App Store Connect
5. Fill in app information, screenshots, privacy policy
6. Submit for review

## Development Tips

### Hot Reloading
- Shake device or press `Cmd+D` (iOS) / `Cmd+M` (Android)
- Select "Enable Hot Reloading"

### Debugging
- Use React Native Debugger
- Install: `brew install react-native-debugger` (macOS)
- Enable Debug JS Remotely in dev menu

### Performance
- Use Hermes engine (enabled by default)
- Profile with Flipper
- Monitor memory usage

## See Also

- [Main Documentation](../NATIVE_APPS_GUIDE.md)
- [React Native Docs](https://reactnative.dev/docs/getting-started)
- [Android Developer Guide](https://developer.android.com)
- [iOS Developer Guide](https://developer.apple.com/ios)

## Support

For issues, see the main project [GitHub Issues](https://github.com/your-repo/issues)
