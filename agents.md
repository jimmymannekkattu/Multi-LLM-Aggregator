# 🧠 AI Nexus - Technical Architecture

> **Developer guide to understanding how AI Nexus works under the hood**

---

## 📖 Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Core Components](#core-components)
4. [API Reference](#api-reference)
5. [Data Flow](#data-flow)
6. [Provider System](#provider-system)
7. [Memory Agent](#memory-agent)
8. [Mobile App](#mobile-app)
9. [Testing](#testing)

---

## System Overview

AI Nexus is a **multi-AI aggregation platform** that:
- Queries multiple AI providers in parallel
- Synthesizes responses into a coherent answer
- Provides memory/learning capabilities
- Supports offline and distributed processing

**Key Design Principles:**
- ✅ **Fallback-first**: Works without API keys (uses g4f)
- ✅ **Async-native**: All I/O operations are asynchronous
- ✅ **Modular**: Easy to add new providers
- ✅ **Type-safe**: Uses Pydantic models

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACES                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────────┐ │
│  │ Desktop  │  │ Web Chat │  │ Mobile   │  │  REST API   │ │
│  │(Streamlit│  │  (HTML)  │  │  (RN)    │  │  Clients    │ │
│  └─────┬────┘  └─────┬────┘  └─────┬────┘  └─────┬───────┘ │
└────────┼─────────────┼──────────────┼──────────────┼─────────┘
         │             │              │              │
         └─────────────┴──────────────┴──────────────┘
                              │
         ┌────────────────────┴────────────────────┐
         │         API LAYER (FastAPI)             │
         │  /chat, /ws/chat, /stream/chat, /docs   │
         └────────────┬────────────────────────────┘
                      │
         ┌────────────┴────────────────────────────┐
         │      QUERY ORCHESTRATOR                 │
         │       (llm_providers.py)                │
         └──┬──────────┬──────────┬─────────────┬──┘
            │          │          │             │
   ┌────────┴──┐  ┌───┴────┐ ┌───┴────┐   ┌───┴────────┐
   │ OpenAI    │  │ g4f    │ │ Ollama │   │ Anthropic  │
   │ Claude    │  │(Free)  │ │(Local) │   │ Google     │
   └───────────┘  └────────┘ └────────┘   └────────────┘
                      │
         ┌────────────┴────────────────────────────┐
         │      SYNTHESIS ENGINE                   │
         │      (offline_model.py)                 │
         │  Ollama → OpenAI → g4f (fallbacks)      │
         └────────────┬────────────────────────────┘
                      │
         ┌────────────┴────────────────────────────┐
         │         MEMORY AGENT                    │
         │    (ChromaDB + Embeddings)              │
         │  Stores Q&A, Enables RAG, Export Data   │
         └─────────────────────────────────────────┘
```

---

## Core Components

### 1. Main Application (`app.py`)

**Purpose**: Streamlit-based desktop interface

**Key Functions:**

```python
async def run_process(question):
    """
    Main orchestration function
    1. Query all enabled providers
    2. Retrieve relevant memories (if enabled)
    3. Synthesize final answer
    4. Store to memory (if learning enabled)
    """
```

**UI Structure:**
- Sidebar: Provider toggles, API keys, settings
- Main area: Query input, results display
- Tabs: Chat, Discovery, Mobile, Memory

### 2. API Server (`api.py`)

**Purpose**: FastAPI backend for external clients

**Endpoints:**

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check |
| `/models` | GET | List available models |
| `/chat` | POST | Standard request/response |
| `/ws/chat` | WebSocket | Real-time streaming |
| `/stream/chat` | POST | Server-sent events |
| `/history` | GET | Chat history |

**Request Model:**
```python
class ChatRequest(BaseModel):
    query: str
    online_models: List[str] = []
    offline_models: List[str] = []
    use_memory: bool = False
    synthesizer_model: Optional[str] = None
```

**Response Model:**
```python
class ChatResponse(BaseModel):
    final_answer: str
    individual_responses: Dict[str, str]
```

### 3. Provider System (`llm_providers.py`)

**Purpose**: Unified interface for all AI providers

**Providers Supported:**

```python
# Online (API-based)
async def fetch_openai(query, client)      # GPT models
async def fetch_anthropic(query, client)   # Claude
async def fetch_gemini(query, client)      # Gemini
async def fetch_perplexity(query, client)  # Perplexity

# Free fallback
async def fetch_g4f(query, model, name)    # g4f (no key needed)

# Offline
async def fetch_ollama(query, model, client)  # Local models
```

**Provider Pattern:**
```python
async def fetch_provider(query: str, client: httpx.AsyncClient) -> str:
    """
    Standard provider interface:
    - Takes query and HTTP client
    - Returns string response or error message
    - Handles all exceptions internally
    """
```

### 4. Synthesis Engine (`offline_model.py`)

**Purpose**: Combines multiple AI responses into one answer

**Fallback Chain:**
```python
1. Try: Ollama (local, fast, private)
   ↓ (if unavailable)
2. Try: OpenAI API (requires key)
   ↓ (if no key)
3. Use: g4f (free web fallback)
```

**Synthesis Function:**
```python
async def synthesize_responses(
    responses: Dict[str, str],
    synthesizer_model: str = "llama3"
) -> str:
    """
    Combines multiple AI responses
    Returns: Single coherent answer
    """
```

### 5. Memory Agent (`agents/memory.py`)

**Purpose**: RAG-based learning and knowledge retention

**Technology Stack:**
- **Vector DB**: ChromaDB
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2`
- **Persistence**: Local `./chroma_db` directory

**Key Functions:**

```python
def add_to_vectordb(question, answer, metadata):
    """Store Q&A pair with embeddings"""

def search_memory(query, top_k=3):
    """Retrieve relevant past Q&A"""

def export_training_data():
    """Export to JSONL for fine-tuning"""
```

**Memory Workflow:**
```
Query → Search similar past Q&A → Include in context → 
Get Answer → Store new Q&A → Update embeddings
```

### 6. Discovery Agent (`agents/discovery.py`)

**Purpose**: Find and test new models

**Features:**
- Search g4f models by name
- Fetch all OpenRouter models
- Scan local/network Ollama instances
- Test model availability before adding

**Key Functions:**

```python
def get_g4f_models() -> List[str]:
    """List all g4f model names"""

def search_models(query: str, openrouter_key: Optional[str]) -> Dict:
    """Search across providers"""

async def verify_model(provider: str, model: str, **kwargs) -> Dict:
    """Test if model is accessible"""
```

---

## API Reference

### REST API

#### POST `/chat`

**Request:**
```json
{
  "query": "What is AI?",
  "online_models": ["ChatGPT (OpenAI)"],
  "offline_models": ["llama3"],
  "use_memory": true
}
```

**Response:**
```json
{
  "final_answer": "AI is...",
  "individual_responses": {
    "ChatGPT (OpenAI)": "...",
    "Ollama (llama3)": "..."
  }
}
```

### WebSocket API

#### WS `/ws/chat`

**Connect:**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/chat');
```

**Send:**
```json
{
  "query": "Hello",
  "online_models": ["Free Web (g4f)"],
  "offline_models": [],
  "use_memory": true
}
```

**Receive (progressive):**
```json
{"status": "processing", "message": "Processing query..."}
{"status": "querying", "model": "GPT-4 (Free)"}
{"status": "response", "model": "GPT-4 (Free)", "content": "..."}
{"status": "synthesizing", "message": "Synthesizing..."}
{"status": "complete", "final_answer": "...", "individual_responses": {...}}
```

### Streaming API

#### POST `/stream/chat`

**Request:** Same as `/chat`

**Response:** Server-Sent Events (SSE)
```
data: {"status": "processing", "message": "..."}

data: {"status": "querying", "model": "..."}

data: {"status": "complete", "final_answer": "..."}
```

---

## Data Flow

### Query Processing Flow

```
1. User submits query
   ↓
2. API receives request (FastAPI)
   ↓
3. Query Orchestrator spawns parallel tasks
   ├─→ OpenAI API
   ├─→ Claude API
   ├─→ g4f (free)
   └─→ Ollama (local)
   ↓
4. Responses collected (with timeouts)
   ↓
5. Memory search for relevant context (optional)
   ↓
6. Synthesis Engine combines responses
   ├─→ Try Ollama first
   ├─→ Fallback to OpenAI
   └─→ Fallback to g4f
   ↓
7. Store Q&A to memory (if enabled)
   ↓
8. Return final answer to user
```

### Memory-Enhanced Query Flow

```
Query → Memory Search → Inject context → Query LLMs →
Synthesize → Store new Q&A → Return answer
```

**Context Injection:**
```python
enriched_query = f"""
Context from memory:
{past_qa_1}
{past_qa_2}

User question: {query}
"""
```

---

## Provider System

### Adding a New Provider

1. **Create fetch function** in `llm_providers.py`:
```python
async def fetch_newprovider(query: str, client: httpx.AsyncClient) -> str:
    try:
        # Make API call
        response = await client.post(
            "https://api.newprovider.com/chat",
            json={"message": query}
        )
        return response.json()["text"]
    except Exception as e:
        return f"Error (NewProvider): {str(e)}"
```

2. **Add to orchestrator** in `api.py`:
```python
if "NewProvider" in online_models:
    tasks.append(("NewProvider", fetch_newprovider(query, client)))
```

3. **Add UI toggle** in `app.py`

### Provider Testing

```python
# Test individual provider
pytest tests/test_providers.py::test_fetch_newprovider -v
```

---

## Memory Agent

### ChromaDB Schema

**Collection:** `chat_history`

**Document Structure:**
```python
{
    "id": "uuid",
    "documents": ["Q: ... A: ..."],
    "metadatas": [{
        "question": "...",
        "answer": "...",
        "timestamp": "...",
        "models_used": "..."
    }],
    "embeddings": [[0.1, 0.2, ...]]  # 384-dim vectors
}
```

### Similarity Search

```python
# Find top 3 similar Q&A pairs
results = collection.query(
    query_texts=[query],
    n_results=3
)
```

### Export Format (JSONL)

```json
{"prompt": "Q: ... A: ...", "completion": "..."}
{"prompt": "Q: ... A: ...", "completion": "..."}
```

---

## Mobile App

### Architecture

```
React Native (Expo)
  ↓
Axios HTTP Client
  ↓
FastAPI Backend (localhost:8000)
```

### Key Components

- **ChatScreen**: Main chat interface
- **HistoryScreen**: View past conversations
- **SettingsScreen**: Configure server URL, models

### Connection Flow

1. User opens mobile app
2. Scans QR code from desktop app (contains server URL)
3. Or manually enters: `http://192.168.1.x:8000`
4. App validates connection via `/health`
5. Fetches available models via `/models`
6. Ready to chat via `/chat`

---

## Testing

### Test Structure

```
tests/
├── test_api.py         # API endpoints
├── test_providers.py   # Provider functions
├── test_discovery.py   # Discovery agent
└── test_websocket.py   # WebSocket/streaming
```

### Running Tests

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_api.py -v

# Specific test
pytest tests/test_api.py::test_health_check -v

# With coverage
pytest tests/ --cov=. --cov-report=html
```

### Test Coverage

- ✅ API endpoints (health, models, chat)
- ✅ Provider integrations (mocked)
- ✅ Discovery (g4f, OpenRouter, Ollama)
- ✅ WebSocket connections
- ✅ Streaming responses

---

## Configuration

### Environment Variables

```bash
# API Keys (optional)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AIza...
PERPLEXITY_API_KEY=pplx-...

# Ollama (for Docker)
OLLAMA_HOST=http://ollama:11434
```

### Runtime Configuration

**Streamlit** (`app.py`):
- Provider toggles in sidebar
- Model selection
- Memory enable/disable

**API** (URL parameters):
- Model selection in request body
- Synthesizer model choice
- Memory usage toggle

---

## Performance

### Optimization Strategies

1. **Parallel Execution**: All providers queried simultaneously
2. **Timeouts**: Failed providers don't block others
3. **Caching**: ChromaDB indexes for fast search
4. **Async I/O**: No blocking operations

### Typical Response Times

- **Single provider**: 1-3 seconds
- **Multi-provider (3)**: 3-5 seconds (limited by slowest)
- **With synthesis**: +1-2 seconds
- **Memory search**: <100ms

---

## Security Considerations

### Current Design (Local/Trusted Network)

- ✅ No authentication (assumes local use)
- ✅ API keys stored in `.env` or session state
- ✅ No data sent to external servers (except provider APIs)

### Production Deployment

**If exposing to internet**, add:
- 🔒 API key authentication
- 🔒 HTTPS/WSS
- 🔒 Rate limiting
- 🔒 Input validation/sanitization
- 🔒 CORS configuration

---

## Troubleshooting

### Common Issues

**"Ollama 404":**
```bash
ollama serve
ollama pull llama3
```

**"No module named 'chromadb'":**
```bash
pip install -r requirements.txt
```

**WebSocket connection failed:**
- Check firewall rules
- Ensure API is running: `curl http://localhost:8000/health`

---

## Contributing

### Code Style

- Use `async`/`await` for I/O operations
- Type hints on all function signatures
- Docstrings for public functions
- Error handling with try/except

### Pull Request Checklist

- [ ] Tests pass (`pytest tests/`)
- [ ] New features have tests
- [ ] Documentation updated
- [ ] Code formatted (`black`, `isort`)

---

## Roadmap

**Planned Features:**
- [ ] Voice input/output
- [ ] Image generation support
- [ ] Plugin system for custom providers
- [ ] Multi-user support
- [ ] Conversation branching
- [ ] Model fine-tuning integration

---

**Questions?** Open an issue on [GitHub](https://github.com/jimmymannekkattu/Multi-LLM-Aggregator/issues)
