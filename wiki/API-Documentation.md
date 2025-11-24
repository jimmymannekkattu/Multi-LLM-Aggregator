# 🔌 API Documentation

Technical documentation for developers integrating with AI Nexus.

## 📡 Base URL

When running locally:
```
http://localhost:8000
```

When connecting from mobile on local network:
```
http://<YOUR_IP>:8000
```

---

## 🔑 Endpoints

### `GET /`
Root endpoint with API information.

**Response**:
```json
{
  "message": "Welcome to AI Nexus API",
  "endpoints": {
    "health": "/health",
    "models": "/models",
    "history": "/history",
    "chat": "/chat",
    "docs": "/docs"
  }
}
```

---

### `GET /health`
Health check endpoint.

**Response**:
```json
{
  "status": "online",
  "service": "AI Nexus API"
}
```

---

### `GET /models`
List available online and offline models.

**Response**:
```json
{
  "online": [
    "ChatGPT (OpenAI)",
    "Claude (Anthropic)",
    "Gemini (Google)",
    "Perplexity"
  ],
  "offline": [
    "llama3",
    "codegemma:2b",
    "mistral"
  ]
}
```

---

### `POST /chat`
Send a query to multiple AI models.

**Request Body**:
```json
{
  "query": "What is machine learning?",
  "online_models": ["ChatGPT (OpenAI)", "Claude (Anthropic)"],
  "offline_models": ["llama3"],
  "use_memory": true,
  "synthesizer_model": "llama3"
}
```

**Parameters**:
- `query` (string, required): The question to ask
- `online_models` (array, optional): List of online models to query
- `offline_models` (array, optional): List of offline models to query
- `use_memory` (boolean, optional): Whether to use RAG memory. Default: `true`
- `synthesizer_model` (string, optional): Model to synthesize responses. Default: `llama3`

**Response**:
```json
{
  "final_answer": "Machine learning is a subset of artificial intelligence...",
  "individual_responses": {
    "ChatGPT": "Machine learning is...",
    "Claude": "ML is a field of AI...",
    "llama3": "Machine learning involves..."
  }
}
```

---

### `GET /history`
Retrieve chat history from memory.

**Response**:
```json
{
  "history": [
    {
      "id": "abc123",
      "query": "What is AI?",
      "answer": "Artificial Intelligence is...",
      "type": "Synthesized",
      "timestamp": "2024-01-15T10:30:00"
    }
  ]
}
```

---

## 🔧 Discovery API

These endpoints are used by the Discovery feature.

### Search Models
```python
from agents.discovery import search_models

# Search across g4f and OpenRouter
results = await search_models(
    query="llama",
    openrouter_key="sk-or-..."  # Optional
)
```

### Verify Model
```python
from agents.discovery import verify_model

# Test if a model works
success, response = await verify_model(
    model_name="gpt_4",
    provider_type="g4f"
)
```

---

## 🐍 Python Client Example

```python
import httpx
import asyncio

async def query_ai_nexus():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/chat",
            json={
                "query": "Explain quantum computing",
                "online_models": ["ChatGPT (OpenAI)"],
                "offline_models": ["llama3"],
                "use_memory": True
            },
            timeout=60.0
        )
        
        data = response.json()
        print(data["final_answer"])

asyncio.run(query_ai_nexus())
```

---

## 📱 Mobile Integration

### React Native Example

```javascript
const sendMessage = async (query) => {
  const response = await fetch(`${serverUrl}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query: query,
      online_models: selectedOnline,
      offline_models: selectedOffline,
      use_memory: true
    })
  });
  
  const data = await response.json();
  return data.final_answer;
};
```

---

## 🔒 Security Considerations

### Local Network Only
- API is not designed for public internet exposure
- No authentication by default
- Use reverse proxy with HTTPS for remote access

### API Keys
- Never send API keys in responses
- Store securely on backend only
- Use environment variables

### Rate Limiting
- Not implemented by default
- Add middleware if exposing publicly

---

## 🔌 WebSocket API

### `WS /ws/chat`
Real-time bidirectional communication for chat.

**Connection**: `ws://localhost:8000/ws/chat`

**Client Sends**:
```json
{
  "query": "What is AI?",
  "online_models": ["ChatGPT (OpenAI)"],
  "offline_models": ["llama3"],
  "use_memory": true,
  "synthesizer_model": "llama3"
}
```

**Server Streams**:
```json
// Processing status
{"status": "processing", "message": "Processing query..."}

// Model querying
{"status": "querying", "model": "ChatGPT"}

// Individual response
{"status": "response", "model": "ChatGPT", "content": "AI is..."}

// Synthesizing
{"status": "synthesizing", "message": "Synthesizing final answer..."}

// Final response
{
  "status": "complete",
  "final_answer": "Artificial Intelligence is...",
  "individual_responses": {...}
}

// Error
{"status": "error", "error": "Error message"}
```

### Python Example
```python
import asyncio
import websockets
import json

async def chat():
    async with websockets.connect("ws://localhost:8000/ws/chat") as ws:
        await ws.send(json.dumps({
            "query": "Hello!",
            "offline_models": ["llama3"]
        }))
        
        async for message in ws:
            data = json.loads(message)
            if data["status"] == "complete":
                print(data["final_answer"])
                break

asyncio.run(chat())
```

### JavaScript Example
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/chat');

ws.onopen = () => {
    ws.send(JSON.stringify({
        query: "Hello!",
        offline_models: ["llama3"]
    }));
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.status === 'complete') {
        console.log(data.final_answer);
    }
};
```

---

## 📡 Streaming API (Server-Sent Events)

### `POST /stream/chat`
Stream responses progressively using SSE.

**Request**: Same as `/chat` endpoint

**Response**: Server-Sent Events stream

**Event Types**:
- `status` - Processing updates
- `model` - Model being queried
- `response` - Individual model response
- `error` - Error from a model
- `complete` - Final synthesized answer

### Python Example
```python
import httpx
import json

with httpx.stream("POST", "http://localhost:8000/stream/chat",
                  json={"query": "Test", "offline_models": ["llama3"]},
                  timeout=120) as response:
    for line in response.iter_lines():
        if line.startswith("data:"):
            data = json.loads(line[5:])
            if "final_answer" in data:
                print(data["final_answer"])
```

### JavaScript Example
```javascript
const eventSource = new EventSource('/stream/chat');

eventSource.addEventListener('complete', (event) => {
    const data = JSON.parse(event.data);
    console.log(data.final_answer);
});
```

---

## 🔧 Testing the API

### Using curl

```bash
# Health check
curl http://localhost:8000/health

# List models
curl http://localhost:8000/models

# Send query
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Hello, AI!",
    "offline_models": ["llama3"]
  }'
```

### Using Python Requests

```python
import requests

# Simple query
response = requests.post(
    "http://localhost:8000/chat",
    json={"query": "Test", "offline_models": ["llama3"]}
)

print(response.json()["final_answer"])
```

---

## 📊 Response Times

Typical response times (local network):
- **Health check**: < 10ms
- **Models list**: < 50ms
- **Chat (1 model)**: 2-10 seconds
- **Chat (5 models)**: 10-30 seconds

Times vary based on:
- Model complexity
- Network speed (for online models)
- Hardware (CPU/GPU)

---

## 🔄 Error Handling

All endpoints return standard HTTP status codes:

- `200`: Success
- `400`: Bad request (invalid parameters)
- `500`: Internal server error

**Error Response Format**:
```json
{
  "detail": "Error message here"
}
```

---

## 📚 Interactive Documentation

FastAPI provides automatic interactive docs:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These show all endpoints with:
- Request/response schemas
- Try-it-out functionality
- Example requests

---

## ⏭️ Next Steps

- **[User Guide](User-Guide)** - Learn the features
- **[Installation Guide](Installation-Guide)** - Set up the API
- **[Troubleshooting](Troubleshooting)** - Fix issues
