# 📥 Installation Guide

Get AI Nexus running in just 5 minutes!

## ⚡ Quick Start (Recommended)

This is the **fastest way** to get started.

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

**That's it!** The script automatically:
- Creates a Python environment
- Installs all dependencies
- Starts your Desktop App at `http://localhost:8501`
- Starts your Mobile API at `http://localhost:8000`

---

## 📋 Prerequisites

Before you begin, make sure you have:

### Required
- **Python 3.10 or higher** ([Download](https://www.python.org/downloads/))
  - Check version: `python3 --version`
- **Ollama** ([Download](https://ollama.com/))
  - This runs the local AI "brain"
  - After installing, run: `ollama pull llama3`

### Optional
- **Node.js** - Only needed if building mobile app from source
- **Docker/Podman** - Alternative deployment method

---

## 🐳 Alternative: Docker/Podman

If you prefer containers:

```bash
# Clone the repository
git clone https://github.com/jimmymannekkattu/Multi-LLM-Aggregator.git
cd Multi-LLM-Aggregator

# Start with Docker
docker-compose up --build

# OR with Podman
podman-compose up --build
```

Access the app:
- Desktop: `http://localhost:8501`
- API: `http://localhost:8000`

---

## 🎨 Manual Setup (Advanced)

If you want full control:

### 1. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Start Backend (Terminal 1)
```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

### 4. Start Frontend (Terminal 2)
```bash
streamlit run app.py
```

---

## ✅ Verify Installation

1. Open `http://localhost:8501` in your browser
2. You should see the AI Nexus interface
3. Try asking a question like "What is AI?"

---

## 🔑 Adding API Keys (Optional)

AI Nexus works **without API keys** using free models. But for better performance, you can add:

1. In the app sidebar, go to **🔌 Online LLMs**
2. Expand any provider (OpenAI, Anthropic, etc.)
3. Paste your API key
4. Toggle **ON**

Keys are stored locally on your computer only.

---

## ⏭️ Next Steps

- **[User Guide](User-Guide)** - Learn all features
- **[Mobile App Setup](Mobile-App-Setup)** - Connect your phone
- **[Troubleshooting](Troubleshooting)** - If something doesn't work
