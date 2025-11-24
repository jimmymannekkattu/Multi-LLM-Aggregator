import asyncio
import httpx
from agents.discovery import verify_model

async def test_ollama_discovery():
    print("Testing Ollama Discovery Logic...")
    
    # 1. Test Verification
    print("\n1. Testing Verification (verify_model)...")
    # Assuming Ollama is running on localhost:11434
    # We need a valid model name. Let's try to fetch one first.
    try:
        tags = httpx.get("http://localhost:11434/api/tags").json()["models"]
        if tags:
            model_name = tags[0]["name"]
            print(f"Found local model: {model_name}")
            
            success, msg = await verify_model(model_name, "Ollama", base_url="http://localhost:11434")
            if success:
                print(f"✅ Verification Successful: {msg[:50]}...")
            else:
                print(f"❌ Verification Failed: {msg}")
        else:
            print("⚠️ No local Ollama models found to test verification.")
    except Exception as e:
        print(f"⚠️ Could not connect to Ollama: {e}")

if __name__ == "__main__":
    asyncio.run(test_ollama_discovery())
