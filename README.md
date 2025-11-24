# 🤖 AI Nexus - Multi-AI Chat Platform

> **Query multiple AI models simultaneously and get synthesized answers** - All in one place!

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

## 🚀 Quick Start (3 Steps - 2 Minutes!)

### Step 1: Download

```bash
git clone https://github.com/jimmymannekkattu/Multi-LLM-Aggregator.git
cd Multi-LLM-Aggregator
```

### Step 2: Run

```bash
chmod +x run.sh
./run.sh
```

### Step 3: Start Chatting!

**Three Ways to Use AI Nexus:**

1. **🖥️ Desktop App** - Open browser: http://localhost:8501
2. **💬 Web Chat** - Open file: `examples/chat-full.html`  
3. **📱 Mobile App** - Scan QR code from desktop app

**That's it!** AI Nexus is now running with free models. No API keys needed to start!

---

## ✨ What is AI Nexus?

AI Nexus lets you:
- ✅ **Ask one question** → Get answers from **multiple AIs** (GPT, Claude, Gemini, etc.)
- ✅ **Use FREE models** → No API keys required (uses g4f)
- ✅ **Chat from anywhere** → Desktop, Web, or Mobile
- ✅ **Get smarter answers** → AI synthesizes multiple responses into one
- ✅ **Keep it private** → Everything runs on your computer

---

## 📋 Prerequisites

**Required:**
- ✅ **Python 3.10+** → [Download here](https://www.python.org/downloads/)
- ✅ **Ollama** → [Install here](https://ollama.com/) ← This runs the local "brain"

**Optional:**
- API keys for premium models (OpenAI, Anthropic, Google)
- Node.js (only for building mobile app from source)

### Installing Ollama

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Download a model (required for synthesis)
ollama pull llama3
```

---

## 💻 Usage Guide

### Option 1: Web Chat Interface (Recommended for Beginners)

1. **Start the server**: `./run.sh`
2. **Open the chat**: Double-click `examples/chat-full.html`
3. **Start chatting!**

**Features:**
- ✨ Beautiful modern UI
- 🎯 Select which AI models to use
- ⚙️ Configure API keys
- 💾 Settings saved automatically
- 📱 Mobile-responsive

### Option 2: Desktop App (Power Users)

1. **Start**: `./run.sh`
2. **Open**: http://localhost:8501
3. **Full features**: Discovery, Memory, Network Nodes

### Option 3: Mobile App

1. **Start backend**: Already running from `./run.sh`
2. **Open desktop app**: http://localhost:8501
3. **Go to Mobile tab**: Scan QR code with your phone
4. **Install Expo Go**: From App/Play Store
5. **Scan QR**: Connect instantly!

---

## 🎯 Key Features

### 1. **Multi-AI Querying**
Ask one question, get answers from:
- ChatGPT (OpenAI)
- Claude (Anthropic)  
- Gemini (Google)
- Perplexity
- Free Web Models (g4f)
- Local Ollama Models

### 2. **WebSocket & Streaming API**
- Real-time WebSocket chat at `/ws/chat`
- Server-sent events at `/stream/chat`
- Full REST API at `/chat`
- Interactive docs at http://localhost:8000/docs

### 3. **Global Model Discovery**
Search and add models from:
- g4f (free web models)
- OpenRouter (100+ models)
- Local Ollama instances

### 4. **Smart Memory System**
- Learns from online AI responses
- Builds local knowledge base
- Makes offline models smarter over time
- Export training data for fine-tuning

### 5. **Network Nodes**
- Connect multiple computers
- Share Ollama models across network
- Distributed AI processing

---

## 🔑 Adding API Keys (Optional)

AI Nexus works **without API keys** using free models. For better performance:

**In Desktop App:**
1. Sidebar → Expand provider (OpenAI, Anthropic, etc.)
2. Paste your API key
3. Toggle **ON**

**In Web Chat:**
1. Click **☰ Menu** → **Settings**
2. Enter your API keys
3. Click **💾 Save**

**Supported Providers:**
- OpenAI → `sk-...`
- Anthropic → `sk-ant-...`
- Google → `AIza...`
- Perplexity → `pplx-...`
- OpenRouter → `sk-or-...`

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_api.py -v
```

**Test Coverage:**
- ✅ API endpoints (4 tests)
- ✅ Model discovery (6 tests)
- ✅ Provider integrations (4 tests)
- ✅ WebSocket connections (3 tests)

---

## 📡 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check |
| `/models` | GET | List available models |
| `/chat` | POST | Standard chat request |
| `/ws/chat` | WS | WebSocket real-time chat |
| `/stream/chat` | POST | Streaming responses (SSE) |
| `/history` | GET | Chat history |
| `/docs` | GET | Interactive API documentation |

**Full API Documentation:** See [wiki/API-Documentation.md](wiki/API-Documentation.md)

---

## 🐳 Docker Deployment (Alternative)

```bash
# Build and run
docker-compose up --build

# Access
Desktop App: http://localhost:8501
API: http://localhost:8000
Ollama: http://localhost:11434
```

---

## 📁 Project Structure

```
Multi-LLM-Aggregator/
├── run.sh                  # One-click startup script
├── app.py                  # Streamlit desktop app
├── api.py                  # FastAPI backend
├── llm_providers.py        # AI model integrations
├── offline_model.py        # Synthesis engine
├── requirements.txt        # Python dependencies
├── examples/               # Example clients
│   ├── chat-full.html     # Full-featured web chat
│   ├── websocket_client.py # Python WebSocket example
│   └── stream_client.py   # Python streaming example
├── tests/                  # Test suite
├── agents/                 # Core logic
│   ├── discovery.py       # Model discovery
│   └── memory.py          # RAG memory system
├── mobile/                 # React Native mobile app
└── wiki/                   # Documentation
```

---

## 🆘 Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "Ollama 404" or "Model Not Found"
```bash
ollama serve          # Start Ollama
ollama pull llama3   # Download model
```

### "Port already in use"
```bash
# Kill process on port 8501 or 8000
lsof -ti:8501 | xargs kill  # Mac/Linux
```

### Mobile app won't connect
1. Same Wi-Fi network?
2. Firewall blocking port 8000?
3. Try: `sudo ufw allow 8000/tcp` (Linux)

**See full troubleshooting:** [wiki/Troubleshooting.md](wiki/Troubleshooting.md)

---

## 📚 Documentation

- **[User Guide](wiki/User-Guide.md)** - Complete feature walkthrough
- **[API Documentation](wiki/API-Documentation.md)** - Endpoint reference
- **[Mobile Setup](wiki/Mobile-App-Setup.md)** - Mobile app guide
- **[WebSocket Chat](WEBSOCKET_CHAT_GUIDE.md)** - Web chat interface
- **[Troubleshooting](wiki/Troubleshooting.md)** - Common issues
- **[Architecture](agents.md)** - Technical details

---

## 🎯 Common Use Cases

**1. Quick Question → One Answer**
- Select multiple models in web chat
- Ask your question
- Get synthesized answer in seconds

**2. Compare AI Perspectives**
- Enable multiple providers
- See how different AIs approach the problem
- Get comprehensive view

**3. Offline AI Assistant**
- Use only Ollama models
- No internet needed
- Complete privacy

**4. Build Your Own AI**
- Enable memory/learning
- Ask questions with online models
- Export training data
- Fine-tune your own model

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repo
2. Create a feature branch
3. Submit a pull request

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file

---

## 🙏 Acknowledgments

- [g4f](https://github.com/xtekky/gpt4free) - Free AI access
- [Ollama](https://ollama.com/) - Local model runtime
- [Streamlit](https://streamlit.io/) - Beautiful UI framework
- [FastAPI](https://fastapi.tiangolo.com/) - Modern API framework

---

## 💡 Need Help?

- 📖 **Check the Wiki**: [GitHub Wiki](https://github.com/jimmymannekkattu/Multi-LLM-Aggregator/wiki)
- 🐛 **Report Issues**: [GitHub Issues](https://github.com/jimmymannekkattu/Multi-LLM-Aggregator/issues)
- 💬 **Questions**: Open a discussion

---

**Made with ❤️ for the AI community**
