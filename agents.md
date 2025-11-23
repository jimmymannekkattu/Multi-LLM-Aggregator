# Agents Documentation

This document provides detailed technical documentation for the AI Nexus agent system.

## Overview

The AI Nexus uses a modular architecture with intelligent fallback systems to ensure the application works in various environments (local, cloud, with/without API keys).

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                       User Interface                         │
│                     (Streamlit UI)                          │
└───────────┬───────────────────────────────────┬─────────────┘
            │                                   │
            ▼                                   ▼
┌───────────────────────────┐       ┌────────────────────────────┐
│    Query Orchestrator     │       │      Memory Agent          │
│         (app.py)          │◄─────►│      (memory.py)           │
└───────────┬───────────────┘       │   (ChromaDB + Embeddings)  │
            │                       └────────────────────────────┘
            ▼
┌───────────────────────────┐    ┌────────────────────────────┐
│   LLM Provider System     │    │   Synthesis System         │
│   (llm_providers.py)      │    │   (offline_model.py)       │
│                           │    │                            │
│  ┌─────────────────────┐  │    │  ┌──────────────────────┐  │
│  │ Online (OpenAI/g4f) │  │    │  │ Local Synthesizer    │  │
│  └─────────────────────┘  │    │  └──────────────────────┘  │
│  ┌─────────────────────┐  │    │  ┌──────────────────────┐  │
│  │ Network Nodes (IPs) │  │    │  │ Remote Synthesizer   │  │
│  └─────────────────────┘  │    │  └──────────────────────┘  │
└───────────────────────────┘    └────────────────────────────┘
```

## Core Components

### 1. Main Application (`app.py`)

**Purpose**: Orchestrates the entire query and synthesis flow.

**Key Functions**:
- `run_process()`: Async function that coordinates querying and synthesis
  - Queries all LLM providers
  - Passes responses to synthesis
  - Handles errors gracefully

**UI Components**:
- Question input area
- "Ask the Swarm" button
- Status indicators
- Final answer display (highlighted card)
- Individual provider responses (4-panel grid)

**Flow**:
```python
User Input → get_all_responses() → synthesize_responses() → Display
```

### 2. LLM Provider System (`llm_providers.py`)

**Purpose**: Manages connections to different LLM providers with intelligent fallbacks.

#### Provider Functions

Each provider (OpenAI, Anthropic, Gemini, Perplexity) has its own function:

```python
async def fetch_openai(query: str, client: httpx.AsyncClient):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return await fetch_g4f(query, "gpt-4o", "ChatGPT")
    # ... official API call
```

**Fallback Logic**:
1. Check for API key in environment
2. If key exists → Use official API
3. If key missing → Use `fetch_g4f()` for free web access

#### Free Web Fallback (`fetch_g4f`)

**Purpose**: Provides free access to LLMs without API keys.

**Technology**: Uses [g4f](https://github.com/xtekky/gpt4free) library

**Implementation**:
```python
async def fetch_g4f(query: str, model: str, provider_name: str):
    g4f_model = g4f.models.gpt_4  # Most stable model
    response = await g4f.ChatCompletion.create_async(
        model=g4f_model,
        messages=[{"role": "user", "content": query}],
    )
    return f"{response}\n\n*(Source: Free Web - {provider_name} via {g4f_model.name})*"
```

**Model Selection**:
- Currently uses `gpt_4` for all providers (most stable)
- Tested alternatives: `gpt_4o` (permission errors), `llama_3_70b` (requires keys)

#### Orchestrator (`get_all_responses`)

**Purpose**: Queries all providers concurrently.

```python
async def get_all_responses(query: str):
    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(
            fetch_openai(query, client),
            fetch_anthropic(query, client),
            fetch_gemini(query, client),
            fetch_perplexity(query, client)
        )
    return {
        "ChatGPT": results[0],
        "Claude": results[1],
        "Gemini": results[2],
        "Perplexity": results[3]
    }
```

**Benefits**:
- Concurrent execution (faster)
- Automatic error handling per provider
- Returns all results even if some fail

### 3. Memory Agent (`memory.py`)

**Purpose**: Implements Knowledge Distillation by storing and retrieving expert answers.

**Technology**:
- **Vector DB**: ChromaDB (local persistence)
- **Embeddings**: `all-MiniLM-L6-v2` (via `sentence-transformers`)

**Functions**:
- `add_to_memory(query, answer)`: Embeds and saves Q&A pairs.
- `retrieve_context(query)`: Finds semantically similar past Q&A pairs.
- `export_dataset()`: Dumps memory to JSONL for fine-tuning.

**Workflow**:
1. **Learning**: When Online models answer, the result is saved to memory.
2. **Recall**: When a new query arrives, relevant memory is retrieved.
3. **Distillation**: The Offline model receives this memory as context, allowing it to answer "expertly" without external help.

### 4. Synthesis System (`offline_model.py`)

**Purpose**: Combines multiple LLM responses into a single, coherent answer.

#### Synthesis Flow

```
┌─────────────────┐
│ Try Ollama      │ ← Fastest, completely free & offline
│ (Local)         │
└────────┬────────┘
         │ Fails
         ▼
┌─────────────────┐
│ Try OpenAI API  │ ← Best quality, requires key
│ (Cloud)         │
└────────┬────────┘
         │ Fails
         ▼
┌─────────────────┐
│ Try g4f         │ ← Free fallback, works always
│ (Free Web)      │
└─────────────────┘
```

#### Implementation

```python
async def synthesize_responses(query: str, responses: dict):
    # Build context from all responses
    context_text = ""
    for provider, response in responses.items():
        if not response.startswith("Error"):
            context_text += f"\n\n--- {provider} Response ---\n{response}"
    
    # Create synthesis prompt
    prompt = f"""
    User Question: "{query}"
    
    Below are responses from multiple AI models:
    {context_text}
    
    Task: Synthesize a single, high-quality answer.
    """
    
    # Try 1: Ollama (local)
    try:
        response = await client.post(OLLAMA_URL, json={...})
        return response.json()["response"]
    except:
        pass
    
    # Try 2: OpenAI API (if key exists)
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            response = await client.post(...OpenAI API...)
            return f"**(Synthesized via Cloud Fallback)**\n\n{response}"
        except:
            pass
    
    # Try 3: g4f (free web)
    try:
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.gpt_4,
            messages=[...synthesis prompt...]
        )
        return f"**(Synthesized via Free Web Fallback)**\n\n{response}"
    except Exception as e:
        return f"Error: All synthesis methods failed."
```

## Configuration

### Environment Variables

Create a `.env` file (optional):

```env
# OpenAI
OPENAI_API_KEY=sk-...

# Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# Google
GOOGLE_API_KEY=...

# Perplexity
PERPLEXITY_API_KEY=pplx-...
```

**Note**: All keys are optional. Missing keys trigger free web fallback.

### Ollama Configuration

In `offline_model.py`:

```python
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"  # Change to your preferred model
```

**Supported Models**: Any model pulled via `ollama pull <model>`

## Error Handling

### Provider Errors

Each provider function wraps its logic in try-except:

```python
try:
    # API call
    response = await client.post(...)
    return response.json()[...]
except Exception as e:
    return f"Error (Provider Name): {str(e)}"
```

**User Experience**: Individual provider errors don't block the app. Other providers still return results.

### Synthesis Errors

The synthesis has 3 fallback levels:

1. **Ollama fails** → Try OpenAI
2. **OpenAI fails** → Try g4f
3. **g4f fails** → Return detailed error message

**Error Message Format**:
```
Error: All synthesis methods failed.
Ollama: [error details]
OpenAI: Key missing or [error details]
Free Web: [error details]
```

## Customization Guide

### Adding a New Provider

1. **Create provider function** in `llm_providers.py`:

```python
async def fetch_newprovider(query: str, client: httpx.AsyncClient):
    api_key = os.getenv("NEWPROVIDER_API_KEY")
    if not api_key:
        return await fetch_g4f(query, "model-name", "NewProvider")
    
    try:
        response = await client.post(
            "https://api.newprovider.com/...",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"model": "...", "messages": [{"role": "user", "content": query}]}
        )
        return response.json()["..."]
    except Exception as e:
        return f"Error (NewProvider): {str(e)}"
```

2. **Add to orchestrator**:

```python
async def get_all_responses(query: str):
    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(
            fetch_openai(query, client),
            fetch_anthropic(query, client),
            fetch_gemini(query, client),
            fetch_perplexity(query, client),
            fetch_newprovider(query, client)  # Add here
        )
    return {
        "ChatGPT": results[0],
        "Claude": results[1],
        "Gemini": results[2],
        "Perplexity": results[3],
        "NewProvider": results[4]  # Add here
    }
```

3. **Update UI** in `app.py` to display the new provider's results.

### Changing g4f Model

In `llm_providers.py`:

```python
async def fetch_g4f(query: str, model: str, provider_name: str):
    g4f_model = g4f.models.gpt_4  # Change to any available model
    # Available: gpt_4, llama_3_70b, mistral_7b, etc.
    # Check with: print(dir(g4f.models))
```

### Customizing Synthesis Prompt

In `offline_model.py`, modify the `prompt` variable:

```python
prompt = f"""
You are a [custom role].
User Question: "{query}"

Responses:
{context_text}

Task:
1. [Custom instruction 1]
2. [Custom instruction 2]

Final Answer:
"""
```

## Performance Considerations

### Timeouts

```python
TIMEOUT = 30.0  # seconds for API calls
```

Adjust in `llm_providers.py` for slower connections.

### Concurrent Execution

All providers are queried concurrently using `asyncio.gather()`:
- **Pros**: Faster (parallel execution)
- **Cons**: Higher memory usage

### Caching (Not Implemented)

**Future Enhancement**: Add response caching to avoid re-querying for identical questions.

## Security Best Practices

1. **Never commit `.env`**: Already in `.gitignore`
2. **Use environment variables**: Don't hardcode keys
3. **Validate inputs**: Streamlit handles basic validation
4. **Rate limiting**: Consider adding for production use
5. **API key rotation**: Regularly rotate keys if using official APIs

## Troubleshooting

### "har_and_cookies dir is not readable"

**Cause**: Certain g4f models (e.g., `gpt_4o`) have permission issues.

**Solution**: Use `gpt_4` model instead (already implemented).

### "Add a 'api_key'" error

**Cause**: Some g4f models (e.g., `llama_3_70b`) require keys even for free access.

**Solution**: Use `gpt_4` for all providers (already implemented).

### Synthesis fails

**Cause**: All three synthesis methods failed.

**Solutions**:
1. Install Ollama: `curl -fsSL https://ollama.com/install.sh | sh`
2. Add OpenAI API key to `.env`
3. Check g4f service status

### Slow responses

**Cause**: Free web access can be slower than official APIs.

**Solutions**:
1. Add official API keys for faster responses
2. Increase timeout values
3. Use local Ollama for synthesis

## Testing

### Manual Testing

```bash
# Test individual providers
python test_models.py

# Test g4f inspection
python inspect_g4f.py

# Test basic g4f functionality
python test_g4f.py
```

### Unit Tests (To Be Added)

Future enhancement: Add pytest-based unit tests.

## Deployment Notes

### Local Deployment

Works out of the box. Just run:
```bash
streamlit run app.py
```

### Cloud Deployment (Streamlit Cloud)

1. **Ollama won't work** (no Docker support)
2. **Solution**: App automatically uses free web fallback
3. **Optional**: Add API keys in Streamlit secrets for better performance

### Docker Deployment (Future)

Not yet implemented. Would require:
- Dockerfile
- Ollama in separate container
- docker-compose for orchestration

## Future Enhancements

1. **Response Caching**: Cache responses for identical queries
2. **User Sessions**: Track query history
3. **Export Results**: Save responses as PDF/JSON
4. **Custom Models**: Allow users to select specific models per provider
5. **Streaming Responses**: Show responses as they arrive
6. **Analytics**: Track usage patterns
7. **Multi-language Support**: Translate UI and responses

## Support

For issues or questions:
- GitHub Issues: [Multi-LLM-Aggregator Issues](https://github.com/jimmymannekkattu/Multi-LLM-Aggregator/issues)
- Documentation: This file and README.md

## Version History

- **v1.0** (Initial): Basic multi-LLM querying with Ollama synthesis
- **v1.1** (Current): Added g4f free web access and intelligent fallbacks
