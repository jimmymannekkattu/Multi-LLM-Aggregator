import g4f
import httpx
import asyncio

# Popular free models that are generally reliable
POPULAR_FREE_MODELS = [
    {"name": "gpt-4", "provider": "g4f", "display": "GPT-4 (Free)"},
    {"name": "gpt-3.5-turbo", "provider": "g4f", "display": "GPT-3.5 Turbo (Free)"},
    {"name": "llama-3-70b-chat", "provider": "g4f", "display": "Llama 3 70B (Free)"},
    {"name": "mixtral-8x7b", "provider": "g4f", "display": "Mixtral 8x7B (Free)"},
    {"name": "claude-3-opus", "provider": "g4f", "display": "Claude 3 Opus (Free)"},
    {"name": "gemini-pro", "provider": "g4f", "display": "Gemini Pro (Free)"},
]

async def get_g4f_models():
    """Returns a list of popular free models."""
    # In the future, we could dynamically scan g4f.models, but for now a curated list is safer
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

async def verify_model(model_name: str, provider_type: str, api_key: str = None, base_url: str = None):
    """Verifies if a model is working by generating a short response."""
    test_query = "Say 'Hello'"
    
    try:
        if provider_type == "g4f":
            # Map string name to g4f model object if possible, or pass string
            # g4f.ChatCompletion handles strings usually
            response = await g4f.ChatCompletion.create_async(
                model=model_name,
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
                    
        return False, "Unknown Provider"
        
    except Exception as e:
        return False, str(e)
