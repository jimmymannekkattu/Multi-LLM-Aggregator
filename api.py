from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import asyncio
import httpx
import os
from llm_providers import fetch_openai, fetch_anthropic, fetch_gemini, fetch_perplexity, fetch_ollama, fetch_generic_openai_compatible
from offline_model import synthesize_responses

# Initialize FastAPI
app = FastAPI(title="AI Nexus API", description="Backend for AI Nexus Mobile App")

# --- Data Models ---
class ChatRequest(BaseModel):
    query: str
    online_models: List[str] = []
    offline_models: List[str] = [] # List of model names (assumed local for now)
    use_memory: bool = True
    synthesizer_model: Optional[str] = None # Name of model to use for synthesis

class ChatResponse(BaseModel):
    final_answer: str
    individual_responses: Dict[str, str]

# --- Memory Integration ---
MEMORY_AVAILABLE = False
try:
    from agents.memory import add_to_memory, retrieve_context, export_dataset
    import chromadb
    MEMORY_AVAILABLE = True
except ImportError:
    pass

# --- Endpoints ---

@app.get("/")
def root():
    return {
        "message": "Welcome to AI Nexus API",
        "endpoints": {
            "health": "/health",
            "models": "/models",
            "history": "/history",
            "chat": "/chat",
            "docs": "/docs"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "online", "service": "AI Nexus API"}

@app.get("/models")
async def get_models():
    """Fetch available models (Online & Local Ollama)"""
    online = ["ChatGPT (OpenAI)", "Claude (Anthropic)", "Gemini (Google)", "Perplexity"]
    
    offline = []
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get("http://localhost:11434/api/tags", timeout=2.0)
            if resp.status_code == 200:
                offline = [m["name"] for m in resp.json()["models"]]
    except:
        pass
        
    return {"online": online, "offline": offline}

@app.get("/history")
def get_history():
    """Retrieve full chat history from Memory (ChromaDB)"""
    if not MEMORY_AVAILABLE:
        return {"error": "Memory module not available"}
    
    try:
        # We need to access the collection directly to get all items
        # This is a bit of a hack since agents/memory.py abstracts it, 
        # but for a full history dump we need raw access or a new function.
        # Let's try to read the JSONL export if it exists, or query the DB.
        # For simplicity/robustness, let's add a 'get_all_memories' to memory.py later.
        # For now, we'll return a placeholder or try to read the DB if possible.
        
        # Better approach: Let's assume we update memory.py to support this.
        # But since I can't edit memory.py in this single tool call, I'll implement a read here.
        
        client = chromadb.PersistentClient(path="./memory_db")
        collection = client.get_or_create_collection(name="knowledge_base")
        
        # Get all items
        results = collection.get()
        
        history = []
        if results["ids"]:
            for i in range(len(results["ids"])):
                # Metadatas contains the answer and type
                meta = results["metadatas"][i]
                doc = results["documents"][i] # The query
                
                history.append({
                    "id": results["ids"][i],
                    "query": doc,
                    "answer": meta.get("answer", "No answer stored"),
                    "type": meta.get("type", "Unknown"),
                    "timestamp": meta.get("timestamp", "")
                })
        
        # Sort by timestamp if possible, otherwise reverse
        return {"history": history[::-1]} # Newest first
        
    except Exception as e:
        return {"error": str(e)}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Unified Chat Endpoint"""
    
    # 1. Retrieve Context
    context = ""
    if MEMORY_AVAILABLE and request.use_memory:
        try:
            context = retrieve_context(request.query)
        except:
            pass

    # 2. Query Providers
    responses = {}
    async with httpx.AsyncClient() as client:
        tasks = []
        
        # Online
        if "ChatGPT (OpenAI)" in request.online_models:
            tasks.append(("ChatGPT", fetch_openai(request.query, client)))
        if "Claude (Anthropic)" in request.online_models:
            tasks.append(("Claude", fetch_anthropic(request.query, client)))
        if "Gemini (Google)" in request.online_models:
            tasks.append(("Gemini", fetch_gemini(request.query, client)))
        if "Perplexity" in request.online_models:
            tasks.append(("Perplexity", fetch_perplexity(request.query, client)))
            
        # Offline
        for model in request.offline_models:
            tasks.append((f"Ollama ({model})", fetch_ollama(request.query, model, client)))
            
        # Execute
        for name, coro in tasks:
            try:
                res = await coro
                responses[name] = res
            except Exception as e:
                responses[name] = f"Error: {str(e)}"
    
    # 3. Synthesize
    target_model = request.synthesizer_model if request.synthesizer_model else "llama3"
    # Check if target model is in offline list or default
    
    final_answer = await synthesize_responses(
        request.query, 
        responses, 
        context=context,
        target_model=target_model
    )
    
    # 4. Save to Memory
    if MEMORY_AVAILABLE and request.use_memory:
        try:
            add_to_memory(request.query, final_answer, "Mobile-Synthesized")
        except:
            pass
            
    return ChatResponse(final_answer=final_answer, individual_responses=responses)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
