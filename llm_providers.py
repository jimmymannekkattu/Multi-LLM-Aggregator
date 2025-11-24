import os
import httpx
import asyncio
import json
import g4f
from dotenv import load_dotenv

load_dotenv()

# Timeout for API calls
TIMEOUT = 30.0

async def fetch_g4f(query: str, model: str, provider_name: str):
    """
    Fallback to g4f (Free Web) if API key is missing.
    """
    try:
        # Resolve string name to g4f model object
        if hasattr(g4f.models, model):
            model_obj = getattr(g4f.models, model)
        else:
            # Fallback to gpt_4 if model not found
            model_obj = g4f.models.gpt_4
        
        response = await g4f.ChatCompletion.create_async(
            model=model_obj,
            messages=[{"role": "user", "content": query}],
        )
        return f"{response}\n\n*(Source: Free Web - {provider_name} via {model})*"
    except Exception as e:
        return f"Error ({provider_name} - Free Web): {str(e)}"

async def fetch_openai(query: str, client: httpx.AsyncClient):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return await fetch_g4f(query, "gpt-4o", "ChatGPT")
    
    try:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": "gpt-4o",
                "messages": [{"role": "user", "content": query}]
            },
            timeout=TIMEOUT
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error (OpenAI): {str(e)}"

async def fetch_anthropic(query: str, client: httpx.AsyncClient):
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return await fetch_g4f(query, "claude-3-opus", "Claude")
    
    try:
        response = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json={
                "model": "claude-3-opus-20240229",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": query}]
            },
            timeout=TIMEOUT
        )
        response.raise_for_status()
        return response.json()["content"][0]["text"]
    except Exception as e:
        return f"Error (Anthropic): {str(e)}"

async def fetch_gemini(query: str, client: httpx.AsyncClient):
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return await fetch_g4f(query, "gemini-pro", "Gemini")
    
    try:
        # Gemini API structure is slightly different, often uses URL params for key
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
        response = await client.post(
            url,
            headers={"Content-Type": "application/json"},
            json={
                "contents": [{"parts": [{"text": query}]}]
            },
            timeout=TIMEOUT
        )
        response.raise_for_status()
        # Parse response carefully
        data = response.json()
        if "candidates" in data and data["candidates"]:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        return "Error (Gemini): No content returned."
    except Exception as e:
        return f"Error (Gemini): {str(e)}"

async def fetch_perplexity(query: str, client: httpx.AsyncClient):
    api_key = os.getenv("PERPLEXITY_API_KEY")
    if not api_key:
        # Perplexity free web access via g4f might be limited, trying generic fallback or specific if available
        return await fetch_g4f(query, "llama-3-70b-chat", "Perplexity")
    
    try:
        response = await client.post(
            "https://api.perplexity.ai/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3-sonar-large-32k-online",
                "messages": [{"role": "user", "content": query}]
            },
            timeout=TIMEOUT
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error (Perplexity): {str(e)}"

async def fetch_ollama(query: str, model: str, client: httpx.AsyncClient):
    """
    Fetch response from local Ollama instance.
    """
    try:
        response = await client.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": query,
                "stream": False
            },
            timeout=60.0 # Longer timeout for local models
        )
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        return f"Error (Ollama - {model}): {str(e)}"

async def fetch_generic_openai_compatible(query: str, api_key: str, base_url: str, model: str, provider_name: str, client: httpx.AsyncClient):
    """
    Fetch response from any OpenAI-compatible API (Groq, OpenRouter, etc.)
    """
    try:
        # Ensure base_url ends with /v1/chat/completions or similar if not provided
        # But usually users provide the base URL like "https://api.groq.com/openai/v1"
        # We will append /chat/completions if it looks like a base root
        
        url = base_url
        if not url.endswith("/chat/completions"):
            if url.endswith("/"):
                url += "chat/completions"
            else:
                url += "/chat/completions"
                
        response = await client.post(
            url,
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": model,
                "messages": [{"role": "user", "content": query}]
            },
            timeout=TIMEOUT
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error ({provider_name}): {str(e)}"

async def get_all_responses(query: str, active_providers: list):
    """
    Fetch responses from selected providers.
    active_providers: List of dicts [{"name": "ChatGPT", "func": fetch_openai}, ...]
    """
    async with httpx.AsyncClient() as client:
        tasks = []
        provider_names = []
        
        for provider in active_providers:
            provider_names.append(provider["name"])
            if provider["type"] == "ollama":
                tasks.append(fetch_ollama(query, provider["model"], client))
            elif provider["name"] == "ChatGPT":
                tasks.append(fetch_openai(query, client))
            elif provider["name"] == "Claude":
                tasks.append(fetch_anthropic(query, client))
            elif provider["name"] == "Gemini":
                tasks.append(fetch_gemini(query, client))
            elif provider["name"] == "Perplexity":
                tasks.append(fetch_perplexity(query, client))
                
        results = await asyncio.gather(*tasks)
        
    return dict(zip(provider_names, results))
