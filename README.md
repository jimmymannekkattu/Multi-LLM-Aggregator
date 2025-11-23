# Multi-LLM Aggregator

This application queries multiple LLMs (ChatGPT, Claude, Gemini, Perplexity) and synthesizes their answers using a local offline model (Ollama).

## Prerequisites

1.  **Python 3.10+**: Ensure Python is installed and added to your PATH.
2.  **Ollama**: Install [Ollama](https://ollama.com/) and pull a model:
    ```bash
    ollama pull llama3
    ```
    (Or change `MODEL_NAME` in `offline_model.py` to match your pulled model).

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure API Keys**:
    Create a `.env` file in this directory with your keys:
    ```env
    OPENAI_API_KEY=sk-...
    ANTHROPIC_API_KEY=sk-ant-...
    GOOGLE_API_KEY=...
    PERPLEXITY_API_KEY=pplx-...
    ```

## Deployment (Web)

This app is ready for **Streamlit Cloud**.

1.  **Push to GitHub**:
    - Create a new repository on GitHub.
    - Push this code:
      ```bash
      git remote add origin <your-repo-url>
      git push -u origin main
      ```

2.  **Deploy on Streamlit Cloud**:
    - Go to [share.streamlit.io](https://share.streamlit.io/).
    - Connect your GitHub repo.
    - In "Advanced Settings", add your secrets (API Keys) exactly as they are in your `.env` file.

### ☁️ Cloud Fallback
Since standard web hosts cannot run **Ollama**, the app automatically detects this.
- **Local**: Uses Ollama (Free, Private).
- **Web**: Falls back to `gpt-4o-mini` (OpenAI) for synthesis.

## Running Locally

Run the Streamlit app:
```bash
streamlit run app.py
```
