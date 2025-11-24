import g4f
import httpx
import asyncio

# Popular free models that are generally reliable
POPULAR_FREE_MODELS = [
    {"name": "gpt_4", "provider": "g4f", "display": "GPT-4 (Free Web)"},
    # Add others only if verified to work without auth
]

async def get_g4f_models():
    """Returns a list of popular free models."""
    return POPULAR_FREE_MODELS

async def get_openrouter_models(api_key: str):
    """Fetches available models from OpenRouter."""
    url = "https://openrouter.ai/api/v1/models"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=10.0)
            if response.status_code == 200:
                data = response.json()["data"]
                models = []
                for m in data:
                    models.append({
                        "name": m["id"],
                        "provider": "OpenRouter",
                        "display": f"{m['name']} ({m['pricing']['prompt']}/1M)",
                        "context": m["context_length"],
                        "cost_prompt": m["pricing"]["prompt"],
                        "cost_completion": m["pricing"]["completion"]
                    })
                return models
            else:
                return {"error": f"Failed to fetch: {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}

async def search_models(query: str, openrouter_key: str = None):
    """
    Searches for models across available providers (g4f, OpenRouter).
    """
    results = []
    query_lower = query.lower()

    # 1. Search g4f (Free Web)
    # Dynamically inspect g4f.models
    try:
        for attr_name in dir(g4f.models):
            # Filter out internal attributes and classes that aren't models
            if attr_name.startswith("_"):
                continue
            
            # Simple heuristic: if it's in the models module and matches query
            if query_lower in attr_name.lower():
                # We could verify if it's a Model class, but string matching is faster for discovery
                results.append({
                    "name": attr_name,
                    "provider": "g4f",
                    "display": f"{attr_name} (Free Web)",
                    "source": "g4f"
                })
    except Exception as e:
        print(f"Error searching g4f: {e}")

    # 2. Search OpenRouter (if key provided)
    if openrouter_key:
        or_models = await get_openrouter_models(openrouter_key)
        if isinstance(or_models, list):
            for m in or_models:
                if query_lower in m["name"].lower() or query_lower in m["display"].lower():
                    results.append({
                        "name": m["name"],
                        "provider": "OpenRouter",
                        "display": m["display"],
                        "source": "OpenRouter",
                        "context": m.get("context", "Unknown"),
                        "cost_prompt": m.get("cost_prompt", 0),
                        "cost_completion": m.get("cost_completion", 0)
                    })
    
    return results

async def verify_model(model_name: str, provider_type: str, api_key: str = None, base_url: str = None):
    """Verifies if a model is working by generating a short response."""
    test_query = "Say 'Hello'"
    
    try:
        if provider_type == "g4f":
            # Resolve string name to g4f model object
            if hasattr(g4f.models, model_name):
                model_obj = getattr(g4f.models, model_name)
            else:
                return False, f"Model '{model_name}' not found in g4f.models"

            response = await g4f.ChatCompletion.create_async(
                model=model_obj,
                messages=[{"role": "user", "content": test_query}]
            )
            return True, response
            
        elif provider_type == "OpenRouter":
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}"},
                    json={
                        "model": model_name,
                        "messages": [{"role": "user", "content": test_query}]
                    },
                    timeout=10.0
                )
                if resp.status_code == 200:
                    return True, resp.json()["choices"][0]["message"]["content"]
                else:
                    return False, f"Status: {resp.status_code}"

        elif provider_type == "Ollama":
            async with httpx.AsyncClient() as client:
                # base_url should be the full generate endpoint or we construct it
                # Usually passed as "http://localhost:11434/api/generate" or similar base
                # Let's assume base_url is the root like "http://localhost:11434"
                url = f"{base_url}/api/generate"
                resp = await client.post(
                    url,
                    json={
                        "model": model_name,
                        "prompt": test_query,
                        "stream": False
                    },
                    timeout=120.0
                )
                if resp.status_code == 200:
                    return True, resp.json()["response"]
                else:
                    return False, f"Status: {resp.status_code} - {resp.text[:50]}"
                    
        return False, "Unknown Provider"
        
    except Exception as e:
        return False, f"{type(e).__name__}: {str(e)}"
