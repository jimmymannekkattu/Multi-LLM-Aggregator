# AI Nexus

A powerful application that queries multiple LLMs (ChatGPT, Claude, Gemini, Perplexity) and synthesizes their answers using AI models. **No API keys required** - works completely free using web access!

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

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

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
