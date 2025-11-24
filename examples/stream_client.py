#!/usr/bin/env python3
"""
Streaming Client Example for AI Nexus (Server-Sent Events)
"""
import httpx
import json

def stream_chat():
    url = "http://localhost:8000/stream/chat"
    data = {
        "query": "Explain quantum computing in simple terms",
        "online_models": [],
        "offline_models": ["llama3"],
        "use_memory": True
    }
    
    print(f"📤 Query: {data['query']}\n")
    print("📥 Streaming responses...\n")
    
    with httpx.stream("POST", url, json=data, timeout=120.0) as response:
        for line in response.iter_lines():
            if line.startswith("data:"):
                # Parse SSE data
                json_data = line[5:].strip()  # Remove "data:" prefix
                try:
                    event_data = json.loads(json_data)
                    
                    if "message" in event_data:
                        print(f"⏳ {event_data['message']}")
                    
                    elif "model" in event_data and "content" in event_data:
                        model = event_data["model"]
                        content = event_data["content"][:100]
                        print(f"✅ {model}: {content}...")
                    
                    elif "final_answer" in event_data:
                        print(f"\n🎯 Final Answer:\n{event_data['final_answer']}\n")
                    
                except json.JSONDecodeError:
                    pass

if __name__ == "__main__":
    stream_chat()
