import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add parent directory to path to import api
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api import app

client = TestClient(app)

def test_websocket_connection():
    with client.websocket_connect("/ws/chat") as websocket:
        # Connection should be successful
        pass

def test_websocket_message_flow():
    with client.websocket_connect("/ws/chat") as websocket:
        # Send a test query
        payload = {
            "query": "Hello",
            "online_models": ["Free Web (g4f)"],
            "offline_models": []
        }
        websocket.send_json(payload)
        
        # Expect a status message first ("Thinking...")
        # Note: The exact sequence depends on the implementation, 
        # but we should receive at least one response.
        data = websocket.receive_json()
        assert "type" in data
        
        # We might get multiple messages (status, then response)
        # Loop until we get a response or error, or timeout
        while data["type"] == "status":
            data = websocket.receive_json()
            
        assert data["type"] in ["response", "error"]
        if data["type"] == "response":
            assert "content" in data
            assert len(data["content"]) > 0

def test_websocket_invalid_payload():
    with client.websocket_connect("/ws/chat") as websocket:
        # Send invalid JSON
        websocket.send_text("Not JSON")
        
        # Should receive an error
        data = websocket.receive_json()
        assert data["type"] == "error"
