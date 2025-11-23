import httpx
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3" # Or 'mistral', 'llama2', etc.

async def synthesize_responses(query: str, responses: dict, context: str = "", target_url: str = OLLAMA_URL, target_model: str = MODEL_NAME):
    """
    Synthesizes multiple LLM responses into a single coherent answer using a local or remote Ollama model.
    """
    
    # Construct a prompt that includes all the responses
    context_text = ""
    for provider, response in responses.items():
        if not response.startswith("Error"):
            context_text += f"\n\n--- {provider} Response ---\n{response}"
    
    if not context_text:
        return "Error: No valid responses received from online providers to synthesize."

    # Add retrieved memory context if available
    memory_section = ""
    if context:
        memory_section = f"\n\n--- RELEVANT KNOWLEDGE FROM MEMORY ---\n{context}\n--------------------------------------\n"

    prompt = f"""
    You are an expert synthesizer. 
    User Question: "{query}"
    
    {memory_section}
    
    Below are responses from multiple advanced AI models:
    {context_text}
    
    Task:
    1. Analyze these responses.
    2. Identify the most accurate and comprehensive information.
    3. Synthesize a single, high-quality, detailed answer for the user.
    4. Resolve any conflicts between the models if possible.
    5. Do not explicitly mention "Model A said this", just give the final answer.
    6. If 'RELEVANT KNOWLEDGE FROM MEMORY' is provided, use it to improve accuracy and confidence.
    
    Final Answer:
    """

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                target_url,
                json={
                    "model": target_model,
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
        
        import os
        api_key = os.getenv("OPENAI_API_KEY")
        
        # 1. Try OpenAI if key exists
        if api_key:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers={"Authorization": f"Bearer {api_key}"},
                        json={
                            "model": "gpt-4o-mini", 
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
                print(f"OpenAI Fallback failed: {cloud_e}")
                # Fall through to g4f
        
        # 2. Try Free Web Fallback (g4f)
        try:
            import g4f
            # Use gpt_4 as it is verified stable
            response = await g4f.ChatCompletion.create_async(
                model=g4f.models.gpt_4,
                messages=[
                    {"role": "system", "content": "You are an expert synthesizer. Summarize the provided AI responses into one comprehensive answer."},
                    {"role": "user", "content": prompt}
                ],
            )
            return f"**(Synthesized via Free Web Fallback)**\n\n{response}"
        except Exception as g4f_e:
             return f"Error: All synthesis methods failed.\nOllama: {str(e)}\nOpenAI: Key missing or failed\nFree Web: {str(g4f_e)}"
