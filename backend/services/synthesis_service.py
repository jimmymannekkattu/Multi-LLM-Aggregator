import httpx
import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3" # Or 'mistral', 'llama2', etc.

async def synthesize_responses(query: str, responses: dict):
    """
    Synthesizes multiple LLM responses into a single coherent answer using a local Ollama model.
    """
    
    # Construct a prompt that includes all the responses
    context_text = ""
    for provider, response in responses.items():
        if not response.startswith("Error"):
            context_text += f"\n\n--- {provider} Response ---\n{response}"
    
    if not context_text:
        return "Error: No valid responses received from online providers to synthesize."

    prompt = f"""
    You are an expert synthesizer. 
    User Question: "{query}"
    
    Below are responses from multiple advanced AI models:
    {context_text}
    
    Task:
    1. Analyze these responses.
    2. Identify the most accurate and comprehensive information.
    3. Synthesize a single, high-quality, detailed answer for the user.
    4. Resolve any conflicts between the models if possible.
    5. Do not explicitly mention "Model A said this", just give the final answer.
    
    Final Answer:
    """

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                OLLAMA_URL,
                json={
                    "model": MODEL_NAME,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60.0
            )
            response.raise_for_status()
            return response.json()["response"]
    except Exception as e:
        # Fallback to Cloud Model (OpenAI) if Ollama is offline
        print(f"Ollama offline ({str(e)}). Switching to Cloud Fallback...")
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
             return f"Error: Ollama is offline and OPENAI_API_KEY not found for fallback. Details: {str(e)}"
             
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}"},
                    json={
                        "model": "gpt-4o-mini", # Lightweight fallback
                        "messages": [
                            {"role": "system", "content": "You are an expert synthesizer. Summarize the provided AI responses into one comprehensive answer."},
                            {"role": "user", "content": prompt}
                        ]
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                return f"**(Synthesized via Cloud Fallback)**\n\n{response.json()['choices'][0]['message']['content']}"
        except Exception as cloud_e:
            return f"Error: Both Ollama and Cloud Fallback failed. Ollama: {str(e)}. Cloud: {str(cloud_e)}"
