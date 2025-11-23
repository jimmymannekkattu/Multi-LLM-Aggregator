# 🤖 AI Nexus

**The Ultimate AI Swarm Intelligence System**

AI Nexus is a powerful, distributed AI platform that aggregates intelligence from multiple top-tier LLMs (ChatGPT, Claude, Gemini, Perplexity) and synthesizes them into a single, expert answer using your local AI.

**✨ Key Features:**
- **Free Web Access**: Uses [g4f](https://github.com/xtekky/gpt4free) to query top models without API keys.
- **🔍 Dynamic Model Discovery**: Find and add 100+ models from OpenRouter or free web sources.
- **📱 QR Code Pairing**: Instant mobile connection via QR code scanning.
- **🧠 Knowledge Distillation**: Your local AI "learns" from online experts via a RAG memory system.
- **🌐 Distributed Computing**: Connect multiple computers to form a unified local AI fleet.
- **📱 Mobile App**: Chat with your Swarm from Android or iOS.
- **Privacy First**: Runs locally on your machine.

---

## 🚀 Getting Started

### 1. Prerequisites
- **Python 3.10+**: [Download Here](https://www.python.org/downloads/)
- **Node.js** (for Mobile App): [Download Here](https://nodejs.org/)
- **Ollama** (Optional, for local AI): [Download Here](https://ollama.com/)

### 2. Installation

Clone the repository and set up the environment:

```bash
# 1. Clone the repo
git clone https://github.com/jimmymannekkattu/Multi-LLM-Aggregator.git
cd Multi-LLM-Aggregator

# 2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

### 3. Running the Desktop App

This is the main control center.

```bash
streamlit run app.py
```
- **Access**: Open `http://localhost:8501` in your browser.
- **Usage**:
    - Select models from the sidebar.
    - Type your question.
    - Watch as multiple AIs answer and your local model synthesizes the result!

---

## 📱 Mobile App Setup (Android & iOS)

Access your AI Swarm from your phone!

### Step 1: Start the Backend API
The mobile app needs a server to talk to. Run this in a **new terminal** (keep the Streamlit app running if you want both):

```bash
source venv/bin/activate
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```
*You should see: `Uvicorn running on http://0.0.0.0:8000`*

### Step 2: Start the Mobile Client
1.  Open a **third terminal**.
2.  Navigate to the mobile folder:
    ```bash
    cd mobile
    ```
3.  Install dependencies (first time only):
    ```bash
    npm install
    ```
4.  Start the app:
    ```bash
    npx expo start
    ```
5.  **Scan the QR Code**:
    - Install **Expo Go** from the App Store (iOS) or Play Store (Android).
    - Scan the QR code shown in the terminal.

### Step 3: Connect Your Mobile App

**Option 1: QR Code Pairing (Easiest)**
1.  In the **Desktop App**, go to the Sidebar → **📱 Mobile** tab.
2.  A QR code showing your API URL will be displayed.
3.  In the **Mobile App**, go to **Settings** → tap **"📷 Scan QR Code"**.
4.  Point your phone at the QR code on your screen.
5.  The app will automatically connect!

**Option 2: Manual Entry**
1.  In the mobile app, go to the **Settings** tab.
2.  Enter your PC's Local IP Address:
    - Windows: Run `ipconfig` (look for IPv4 Address).
    - Mac/Linux: Run `ifconfig` (look for inet 192.168...).
    - Enter: `http://YOUR_IP_ADDRESS:8000` (e.g., `http://192.168.1.15:8000`).
3.  Go to **Chat** and start asking questions!

---

## 🧠 Knowledge Distillation (Memory)

AI Nexus makes your local models smarter over time.

1.  **Enable Learning**: In the Sidebar > Knowledge Base, toggle "Enable Learning".
2.  **Teach**: Ask questions with Online Models (ChatGPT, Claude) enabled.
3.  **Learn**: The system saves the high-quality answers to a local vector database.
4.  **Recall**: When you ask a similar question later (even offline!), the system retrieves this memory to help your local model answer correctly.
5.  **Export**: Click "Export Training Data" to get a `.jsonl` file for fine-tuning.

---

## 🔍 Dynamic Model Discovery

Expand your AI fleet with 100+ models!

### Free Web Models (g4f)
1.  Go to Sidebar → **🔍 Discovery**.
2.  Select **"Free Web (g4f)"**.
3.  Click **"Scan for Models"**.
4.  Click **"Test & Add"** on any model (e.g., Llama 3, Mixtral).
5.  The model will be verified and added to your active fleet!

### OpenRouter (100+ Premium Models)
1.  Go to Sidebar → **🔍 Discovery**.
2.  Select **"OpenRouter (API)"**.
3.  Enter your OpenRouter API Key.
4.  Click **"Fetch Models"**.
5.  Search for any model (e.g., "falcon", "vicuna", "deepseek").
6.  Click **"Add to Fleet"** to make it available instantly!

---

## 🌐 Distributed Network Nodes

Combine the power of multiple computers!

1.  **Prepare Nodes**: Install Ollama on other computers and run `ollama serve`.
    - *Note: You may need to set `OLLAMA_HOST=0.0.0.0` on those machines to allow external connections.*
2.  **Add Node**:
    - In the Desktop App Sidebar > Offline & Network > Manage Network Nodes.
    - Enter Name (e.g., "Gaming PC") and URL (e.g., `http://192.168.1.20:11434`).
3.  **Use**: You can now select models running on those remote machines!

---

## 📁 Project Structure

```
AI-Nexus/
├── app.py                  # Desktop App (Streamlit)
├── api.py                  # Mobile Backend (FastAPI)
├── mobile/                 # Mobile App (React Native)
├── agents/                 # Core Logic
│   └── memory.py           # RAG/Memory System
├── llm_providers.py        # Online Model Integrations
├── offline_model.py        # Synthesis Logic
├── requirements.txt        # Python Dependencies
└── README.md              # This Guide
```

## 📄 License
MIT License. Free to use and modify.

## ⚠️ Disclaimer
This project uses `g4f` for free web access. Availability of free models depends on external services and may vary. For production stability, add your own API keys in the Provider Manager.

## ✨ Features

- **Multi-LLM Querying**: Get responses from ChatGPT, Claude, Gemini, and Perplexity simultaneously
- **Free Web Access**: Uses [g4f](https://github.com/xtekky/gpt4free) to access LLMs without API keys
- **🧠 Knowledge Distillation**:
  - **Memory System**: Automatically learns from online experts (RAG).
  - **Instant Training**: Offline models instantly get smarter by accessing the shared memory.
  - **Dataset Export**: Export Q&A pairs to JSONL for fine-tuning.
- **🌐 Distributed Computing**:
  - **Network Nodes**: Connect multiple computers running Ollama.
  - **Unified Fleet**: Query models across your entire local network.
  - **Distributed Brain**: Any node can act as the synthesizer using the central memory.
- **Intelligent Synthesis**: Combines multiple responses into one comprehensive answer
- **Flexible Fallbacks**: 
  - Local synthesis with Ollama (if installed)
  - Cloud synthesis with OpenAI API (if key provided)
  - Free web synthesis with g4f (no keys needed)
- **Beautiful UI**: Modern Streamlit interface with dark theme

## 🚀 Quick Start (No API Keys Needed!)

### Prerequisites

- **Python 3.10+**: Ensure Python is installed and added to your PATH.
- **Virtual Environment**: Recommended for dependency isolation.

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/jimmymannekkattu/Multi-LLM-Aggregator.git
    cd Multi-LLM-Aggregator
    ```

2.  **Create virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    # Install vector DB support
    pip install chromadb sentence-transformers
    ```

4.  **Run the app**:
    ```bash
    streamlit run app.py
    ```

5.  **Open in browser**: Navigate to `http://localhost:8501`

That's it! The app will work without any API keys using the free web access.

## 🔑 Optional: API Keys (For Better Performance)

While the app works without API keys, you can optionally add them for:
- Faster responses
- More reliable access
- Higher rate limits

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...
PERPLEXITY_API_KEY=pplx-...
```

If an API key is present, the app will use the official API. If missing, it automatically falls back to free web access.

## 🤖 Optional: Ollama (For Local Synthesis)

For completely offline synthesis, install [Ollama](https://ollama.com/):

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull llama3
```

The app will automatically detect and use Ollama if available. Otherwise, it falls back to free web synthesis.

## 📦 How It Works

1. **Query Phase**: User enters a question
2. **Multi-LLM Response**: 
   - Checks for API keys for each provider (OpenAI, Anthropic, Google, Perplexity)
   - If key exists → Uses official API
   - If key missing → Uses g4f free web access
3. **Synthesis Phase**:
   - First tries: Ollama (if installed locally)
   - Then tries: OpenAI API (if key exists)
   - Finally uses: g4f free web synthesis
4. **Display**: Shows individual responses + synthesized answer

## 🌐 Deployment

### Streamlit Cloud

1.  **Push to GitHub** (already done)

2.  **Deploy on Streamlit Cloud**:
    - Go to [share.streamlit.io](https://share.streamlit.io/)
    - Connect your GitHub repo
    - In "Advanced Settings", add your secrets (API Keys) if you have them
    - Deploy!

The app will work on Streamlit Cloud even without API keys, using the free web access.

## 📁 Project Structure

```
Multi-LLM-Aggregator/
├── app.py                  # Main Streamlit application
├── llm_providers.py        # LLM provider logic with g4f fallbacks
├── offline_model.py        # Synthesis logic with fallbacks
├── requirements.txt        # Python dependencies
├── .env                    # API keys (optional, not committed)
├── README.md              # This file
├── agents.md              # Detailed agent documentation
├── backend/               # Backend services (optional)
└── frontend/              # Frontend files (optional)
```

## 🛠 Technologies

- **Streamlit**: Web UI framework
- **g4f (GPT4Free)**: Free web access to LLMs
- **Ollama**: Local LLM runtime (optional)
- **Official APIs**: OpenAI, Anthropic, Google, Perplexity (optional)

## 📖 Documentation

See [agents.md](agents.md) for detailed documentation on:
- Architecture
- Provider system
- Synthesis system
- Fallback mechanisms
- Customization

## 📱 Mobile App (Android & iOS)

AI Nexus includes a React Native mobile app that connects to your PC.

### 1. Start the Backend API (on PC)
Run this alongside the Streamlit app:
```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

### 2. Run the Mobile App
1.  Navigate to the mobile folder: `cd mobile`
2.  Install dependencies: `npm install`
3.  Start Expo: `npx expo start`
4.  Scan the QR code with the **Expo Go** app on your phone.

### 3. Configure App
- In the app, go to **Settings**.
- Enter your PC's IP address (e.g., `http://192.168.1.5:8000`).
- Select your models and start chatting!

### Features
- **💬 Chat**: Full access to the Swarm.
- **📜 History**: View all past queries and answers (synced with PC).
- **⚙️ Settings**: Toggle Online/Offline models remotely.

## 📄 License

This project is open source and available under the MIT License.

## ⚠️ Disclaimer

This project uses g4f to provide free access to LLMs. Please note:
- Free web access may be slower or less reliable than official APIs
- Some providers may implement rate limits or blocking
- For production use, official API keys are recommended

## 🙏 Acknowledgments

- [g4f](https://github.com/xtekky/gpt4free) for free LLM access
- [Streamlit](https://streamlit.io/) for the amazing UI framework
- [Ollama](https://ollama.com/) for local model support
