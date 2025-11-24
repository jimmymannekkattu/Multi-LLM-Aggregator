# 📱 Mobile App Setup

Connect your mobile device to AI Nexus and chat with your AI team on the go!

## 📋 Prerequisites

- **AI Nexus Backend**: Must be running on your computer
- **Same Network**: Phone and computer on same Wi-Fi
- **Expo Go App**: Install from App Store or Play Store

---

## 🚀 Quick Setup

### Step 1: Start Mobile Server

On your computer:
```bash
# Make sure backend is running
uvicorn api:app --host 0.0.0.0 --port 8000
```

### Step 2: Start Mobile App

```bash
cd mobile
npm install          # First time only
npx expo start       # Start the app
```

### Step 3: Connect Your Phone

**Option A: QR Code (Easiest)**
1. Install **Expo Go** on your phone
2. Open Expo Go app
3. Scan the QR code shown in terminal
4. App will load on your phone

**Option B: Manual URL**
1. In terminal, note the "exp://" URL
2. In Expo Go, tap "Enter URL manually"
3. Paste the URL

---

## 🔗 Connect to Backend

### Method 1: QR Code Pairing (Recommended)

1. **On Desktop App**:
   - Go to sidebar → **📱 Mobile**
   - You'll see a QR code with your API URL

2. **On Mobile App**:
   - Tap **Settings** (bottom)
   - Tap **📷 Scan QR Code**
   - Point camera at the QR code
   - ✅ Connected!

### Method 2: Manual Entry

1. **Find Your Computer's IP**:
   - **Windows**: Open Command Prompt → `ipconfig`
   - **Mac/Linux**: Open Terminal → `ifconfig`
   - Look for something like `192.168.1.X`

2. **Enter in Mobile App**:
   - Open mobile app → **Settings**
   - Enter: `http://192.168.1.X:8000`
   - Replace `X` with your actual IP

---

## ⚙️ Configure Models

Once connected, select which models to use:

### In Mobile App Settings

1. Tap **Settings** tab
2. Scroll to **Model Selection**
3. Toggle **Online Models**:
   - ChatGPT, Claude, Gemini, etc.
4. Toggle **Offline Models**:
   - Your local Ollama models

💡 **Tip**: Fewer models = faster responses

---

## 💬 Using the Mobile App

### Chat Tab
- Type your question
- Tap **Send**
- See the synthesized answer
- Swipe left on a message to delete

### History Tab
- View all past conversations
- Tap a conversation to see details
- Pull down to refresh

### Settings Tab
- Change server URL
- Select active models
- Scan new QR code

---

## 🔧 Troubleshooting Mobile

### "Cannot Connect to Server"

**Check Network**:
- Phone and computer on same Wi-Fi?
- Try pinging computer IP from phone

**Firewall**:
- Allow port 8000 in firewall
- **Windows**: `netsh advfirewall firewall add rule name="AI Nexus" dir=in action=allow protocol=TCP localport=8000`
- **Mac**: System Preferences → Security → Firewall → Allow

**Backend Running?**:
```bash
# Verify backend is active
curl http://localhost:8000/health
# Should return: {"status":"online"}
```

### "Expo Go Won't Load App"

**Clear Cache**:
- Shake phone → "Reload"
- Or restart Expo Go app

**Check Terminal**:
- Look for errors in `npx expo start` output
- Try: `npx expo start --clear`

### "No Models Available"

**On Desktop**:
- Ensure models are selected in desktop app
- Check Ollama is running: `ollama list`

**On Mobile**:
- Re-scan settings
- Try reconnecting to server

---

## 🎨 Building from Source (Advanced)

### iOS

```bash
cd mobile
npx expo prebuild
npx expo run:ios
```

### Android

```bash
cd mobile
npx expo prebuild
npx expo run:android
```

---

## 🔒 Security Notes

- **Local Network Only**: Mobile app connects via local network
- **No Cloud**: Your data never leaves your network
- **API Keys**: Stored on computer, not phone
- **HTTPS**: Use a reverse proxy for encrypted connections

---

## ⏭️ Next Steps

- **[User Guide](User-Guide)** - Learn all features
- **[Troubleshooting](Troubleshooting)** - More solutions
- **[API Documentation](API-Documentation)** - Understand the API
