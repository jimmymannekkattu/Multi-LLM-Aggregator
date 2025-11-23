import os
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv()

# Timeout for API calls
TIMEOUT = 30.0

async def fetch_openai(query: str, client: httpx.AsyncClient):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "Error: OPENAI_API_KEY not found."
    
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
        return "Error: ANTHROPIC_API_KEY not found."
    
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
        return "Error: GOOGLE_API_KEY not found."
    
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
        return "Error: PERPLEXITY_API_KEY not found."
    
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
