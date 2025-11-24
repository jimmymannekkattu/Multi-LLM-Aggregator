import pytest
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket
from unittest.mock import AsyncMock, patch, MagicMock
from api import app
import json

client = TestClient(app)

def test_websocket_connect():
    """Test WebSocket can be established"""
    with client.websocket_connect("/ws/chat") as websocket:
        # Connection should be successful
        assert websocket is not None

def test_websocket_query():
    """Test sending a query via WebSocket"""
    with patch("api.fetch_ollama", new_callable=AsyncMock) as mock_fetch:
        with patch("api.synthesize_responses", new_callable=AsyncMock) as mock_synth:
            mock_fetch.return_value = "Ollama response"
            mock_synth.return_value = "Final synthesized answer"
            
            with client.websocket_connect("/ws/chat") as websocket:
                # Send query
                query_data = {
                    "query": "Test query",
                    "online_models": [],
                    "offline_models": ["llama3"],
                    "use_memory": False
                }
                websocket.send_json(query_data)
                
                # Receive responses
                messages = []
                for _ in range(5):  # Receive a few messages
                    try:
                        msg = websocket.receive_json()
                        messages.append(msg)
                        if msg.get("status") == "complete":
                            break
                    except:
                        break
                
                # Should have received completion message
                assert any(msg.get("status") == "complete" for msg in messages)
                
                # Final answer should be present
                final_msg = next(msg for msg in messages if msg.get("status") == "complete")
                assert "final_answer" in final_msg

def test_stream_chat():
    """Test streaming chat endpoint"""
    with patch("api.fetch_ollama", new_callable=AsyncMock) as mock_fetch:
        with patch("api.synthesize_responses", new_callable=AsyncMock) as mock_synth:
            mock_fetch.return_value = "Ollama response"
            mock_synth.return_value = "Synthesized answer"
            
            # Note: Streaming endpoint testing is limited in TestClient
            # This is a basic connectivity test
            response = client.post(
                "/stream/chat",
                json={
                    "query": "Test",
                    "offline_models": ["llama3"],
                    "use_memory": False
                }
            )
            
            # Should return 200 and be a streaming response
            assert response.status_code == 200
