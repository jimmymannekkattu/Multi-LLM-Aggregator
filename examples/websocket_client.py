#!/usr/bin/env python3
"""
WebSocket Client Example for AI Nexus
"""
import asyncio
import websockets
import json

async def chat_with_ai():
    uri = "ws://localhost:8000/ws/chat"
    
    async with websockets.connect(uri) as websocket:
        print("Connected to AI Nexus WebSocket!")
        
        # Send query
        query_data = {
            "query": "What is artificial intelligence?",
            "online_models": [],
            "offline_models": ["llama3"],
            "use_memory": True
        }
        
        print(f"\n📤 Sending: {query_data['query']}")
        await websocket.send(json.dumps(query_data))
        
        # Receive responses
        print("\n📥 Receiving responses...\n")
        async for message in websocket:
            data = json.loads(message)
            status = data.get("status")
            
            if status == "processing":
                print(f"⏳ {data.get('message')}")
            
            elif status == "querying":
                print(f"🔍 Querying {data.get('model')}...")
            
            elif status == "response":
                model = data.get("model")
                content = data.get("content", "")[:100]  # First 100 chars
                print(f"✅ {model}: {content}...")
            
            elif status == "synthesizing":
                print(f"🧠 {data.get('message')}")
            
            elif status == "complete":
                print(f"\n🎯 Final Answer:\n{data.get('final_answer')}\n")
                break
            
            elif status == "error":
                print(f"❌ Error: {data.get('error')}")
                break

if __name__ == "__main__":
    asyncio.run(chat_with_ai())
