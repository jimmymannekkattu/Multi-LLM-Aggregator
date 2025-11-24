# 📖 User Guide

Learn how to use all of AI Nexus's powerful features.

## 🎯 Basic Usage

### 1. Asking Questions

1. Type your question in the main text box
2. Select which AI models to use:
   - **Online**: ChatGPT, Claude, Gemini, etc.
   - **Offline**: Local Ollama models
3. Click **Submit** or press `Ctrl+Enter`
4. Wait for your synthesized answer!

**💡 Tip**: Use multiple models for complex questions to get diverse perspectives.

---

## 🔍 Model Discovery

Discover and add new AI models to your fleet!

### Global Search
Search across all available sources at once:

1. Go to **🔍 Discovery** tab
2. Select **Global Search**
3. Enter a model name (e.g., "llama", "mistral", "gpt")
4. *Optional*: Add OpenRouter API key for premium results
5. Click **Search**
6. Click **Test & Add** on any model

### Free Web Models
Add models from the free web:

1. Go to **🔍 Discovery** → **Free Web (g4f)**
2. Click **Scan for Models**
3. Browse available models
4. Click **Test & Add** to verify and add

### Local Ollama Models
Add your local AI models:

1. Make sure Ollama is running
2. Go to **🔍 Discovery** → **Local/Network (Ollama)**
3. Click **Scan Network**
4. Your local models will appear
5. Click **Test & Add** to enable them

---

## 🧠 Memory & Learning

Make your local AI smarter over time!

### Enable Learning
1. Go to sidebar → **🧠 Brain**
2. Toggle **Enable Learning** ON
3. Ask questions with online models enabled
4. The system saves high-quality answers

### How It Works
- **Automatic**: Every answer is saved to local memory
- **Context-Aware**: Future questions retrieve relevant past answers
- **Offline Benefits**: Your local AI gets smarter without internet

### Export Training Data
1. Go to **🧠 Brain** section
2. Click **Export Training Data**
3. Get a `.jsonl` file for fine-tuning
4. Use it to train your own models

---

## 🌐 Network Nodes

Connect multiple computers to share AI power!

### Add a Network Node
1. Install Ollama on another computer
2. Run `ollama serve` on that computer
3. In AI Nexus sidebar → **💻 Offline**
4. Expand **Manage Network Nodes**
5. Enter:
   - **Name**: e.g., "Gaming PC"
   - **URL**: e.g., `http://192.168.1.20:11434`
6. Click **Add Node**

### Use Network Models
- Network models appear in your offline model list
- They're marked with their node name
- Select and use them like local models

---

## 📱 Mobile Connection

Use AI Nexus from your phone!

### QR Code Method (Easiest)
1. In desktop app, go to **📱 Mobile** tab
2. Scan the QR code with the mobile app
3. Done! You're connected

### Manual Connection
1. Find your computer's IP address:
   - **Windows**: Run `ipconfig`
   - **Mac/Linux**: Run `ifconfig`
2. In mobile app → **Settings**
3. Enter: `http://YOUR_IP:8000`

See **[Mobile App Setup](Mobile-App-Setup)** for full guide.

---

## ⚙️ Settings & Configuration

### Provider Management
- **Add API Keys**: For better performance
- **Toggle Providers**: Enable/disable specific AIs
- **Custom Providers**: Add your own OpenAI-compatible APIs

### Synthesizer Settings
- **Choose Brain**: Select which model synthesizes answers
- **Temperature**: Control creativity (higher = more creative)

---

## 💡 Pro Tips

1. **Combine Free & Paid**: Use free models for simple queries, paid for complex ones
2. **Use Memory**: Enable learning to build a knowledge base over time
3. **Network Power**: Connect multiple PCs to distribute workload
4. **Mobile Sync**: Use mobile app when away from desk
5. **Export Data**: Regularly export training data for backups

---

## ⏭️ Next Steps

- **[Mobile App Setup](Mobile-App-Setup)** - Full mobile guide
- **[Troubleshooting](Troubleshooting)** - Common issues
- **[API Documentation](API-Documentation)** - For developers
