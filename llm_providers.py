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
        # Map our internal model names to available g4f models
        # Note: gpt_4 is the most stable free model currently verified
        g4f_model = g4f.models.gpt_4
        
        # We use gpt_4 for ALL providers as a fallback because other models (gpt_4o, llama_3)
        # are currently failing with permission or key errors.
        # The goal is to provide *some* answer rather than an error.

        response = await g4f.ChatCompletion.create_async(
            model=g4f_model,
            messages=[{"role": "user", "content": query}],
        )
        return f"{response}\n\n*(Source: Free Web - {provider_name} via {g4f_model.name})*"
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
