# Mobile Test Checklist for AI Nexus

Use this checklist to verify the mobile experience on your device.

## 1. Connection & Setup
- [ ] **Network Check**: Ensure your mobile device is on the same Wi-Fi network as your computer.
- [ ] **Access**: Open the browser on your mobile and navigate to the URL shown by `diagnose_network.py` (e.g., `http://192.168.1.5:8501`).
- [ ] **Landing Page**: Verify the AI Nexus landing page loads with the "Launch Web Chat" button.

## 2. Web Chat Interface
- [ ] **Launch**: Tap "Launch Web Chat". The chat interface should open.
- [ ] **Sidebar**: 
    - [ ] Verify the sidebar is hidden by default on mobile.
    - [ ] Tap the hamburger menu (☰) to open the sidebar.
    - [ ] Tap the overlay (dark background) to close the sidebar.
- [ ] **Settings**:
    - [ ] Open Sidebar > Settings.
    - [ ] Verify "Server URL" matches your computer's IP (e.g., `http://192.168.1.5:8000`).
    - [ ] If it says `localhost`, refresh the page (the auto-fix should update it).

## 3. Chat Functionality
- [ ] **Model Selection**:
    - [ ] Open Sidebar > Models.
    - [ ] Select "Free Web (g4f)".
- [ ] **Messaging**:
    - [ ] Type "Hello" in the input box.
    - [ ] Tap "Send".
    - [ ] Verify a "Thinking..." status appears.
    - [ ] Verify a response is received from the AI.
- [ ] **Scrolling**:
    - [ ] Verify you can scroll through the chat history.
    - [ ] Verify the input box stays at the bottom of the screen.

## 4. Troubleshooting
- [ ] **Toast Notifications**: Do you see "Connected & Ready" or error messages?
- [ ] **Keyboard**: Does the keyboard cover the input box? (It shouldn't).
