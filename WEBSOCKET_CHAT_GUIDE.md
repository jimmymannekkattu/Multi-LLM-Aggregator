# 🌐 AI Nexus - WebSocket Chat Interface

## For End Users

### 🚀 Quick Start

**1. Make sure the server is running:**
```bash
./run.sh
```
You should see:
- ✅ Backend running on http://localhost:8000
- ✅ Frontend running on http://localhost:8501

**2. Open the Chat Interface:**
- Navigate to the `examples` folder
- Double-click `chat.html` to open it in your browser
- OR right-click → "Open with" → Choose your browser

**3. Start Chatting:**
- Wait for "✓ Connected" status
- Type your question in the input box
- Press Enter or click "Send"
- Watch as AI processes and responds!

---

## 📱 What You'll See

### Connection Status
- **🟢 ✓ Connected** - Ready to chat
- **🔴 ✗ Disconnected** - Server is offline

### Message Types
- **Your messages** - Purple bubbles on the right
- **AI responses** - White bubbles on the left
- **Status updates** - Yellow boxes in the center (e.g., "Processing query...")

### Real-Time Updates
As your question is being processed, you'll see:
1. ⏳ Processing query...
2. 🔍 Querying models...
3. 🧠 Synthesizing final answer...
4. 💬 Final AI response appears!

---

## 🔧 Customization

### Change Models
Open `chat.html` in a text editor and find this line (around line 200):
```javascript
const request = {
    query: query,
    online_models: [],           // Add: ["ChatGPT (OpenAI)"]
    offline_models: ["llama3"],  // Add more: ["llama3", "mistral"]
    use_memory: true
};
```

### Use Online Models
Add API keys first, then modify:
```javascript
online_models: ["ChatGPT (OpenAI)", "Claude (Anthropic)"],
```

---

## 🌍 Access from Other Devices

### Same Wi-Fi Network

**On Server Computer:**
1. Find your IP address:
   - **Windows**: `ipconfig` → Look for IPv4 Address
   - **Mac/Linux**: `ifconfig` → Look for inet 192.168.x.x

**On Other Device:**
1. Open `chat.html` in text editor
2. Change line 164:
   ```javascript
   const wsUrl = 'ws://Your.IP.Address.Here:8000/ws/chat';
   // Example: ws://192.168.1.100:8000/ws/chat
   ```
3. Save and open in browser

---

## ❓ Troubleshooting

### "Connection Error"
- ✅ Check server is running: `./run.sh`
- ✅ Verify URL is `http://localhost:8000`
- ✅ Check firewall isn't blocking port 8000

### "No valid responses"
- ✅ Start Ollama: `ollama serve`
- ✅ Pull a model: `ollama pull llama3`
- ✅ Or add online models with API keys

### Can't Find chat.html
- It's in: `Multi-LLM-Aggregator/examples/chat.html`
- Full path: `/media/.../Multi-LLM-Aggregator/examples/chat.html`

---

## 📊 For Developers

### WebSocket Protocol

**Connect:**
```javascript
ws = new WebSocket('ws://localhost:8000/ws/chat');
```

**Send Query:**
```javascript
ws.send(JSON.stringify({
    query: "Your question",
    online_models: ["ChatGPT (OpenAI)"],
    offline_models: ["llama3"],
    use_memory: true
}));
```

**Receive Updates:**
```javascript
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    // data.status: "processing" | "querying" | "response" | "complete" | "error"
    // data.final_answer: The synthesized result
};
```

---

## 🎯 Best Practices

1. **Start with Offline Models**: Faster, no API costs
2. **Enable Memory**: AI learns from previous conversations
3. **Use Multiple Models**: Get diverse perspectives
4. **Keep Sessions Short**: Reconnects automatically if disconnected

---

## 🔗 More Information

- **API Documentation**: `wiki/API-Documentation.md`
- **Full User Guide**: `wiki/User-Guide.md`
- **Examples**: See `examples/` folder

---

**Need Help?** 
- GitHub Issues: https://github.com/jimmymannekkattu/Multi-LLM-Aggregator/issues
- Check logs in terminal where you ran `./run.sh`
