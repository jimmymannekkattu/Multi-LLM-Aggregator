import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
from api import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "online", "service": "AI Nexus API"}

def test_list_models():
    # Mock httpx.AsyncClient.get for Ollama tags
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "models": [{"name": "llama2"}, {"name": "mistral"}]
        }
        mock_get.return_value = mock_response
        
        response = client.get("/models")
        assert response.status_code == 200
        data = response.json()
        assert "online" in data
        assert "offline" in data
        assert "llama2" in data["offline"]
        assert len(data["online"]) > 0

@pytest.mark.asyncio
async def test_chat_endpoint_success():
    # Mock internal fetchers and synthesizer
    with patch("api.fetch_openai", new_callable=AsyncMock) as mock_openai:
        mock_openai.return_value = "OpenAI response"
        
        with patch("api.synthesize_responses", new_callable=AsyncMock) as mock_synth:
            mock_synth.return_value = "Final Answer"
            
            payload = {
                "query": "Hello",
                "online_models": ["ChatGPT (OpenAI)"],
                "offline_models": [],
                "use_memory": False
            }
            
            response = client.post("/chat", json=payload)
            
            assert response.status_code == 200
            data = response.json()
            assert data["final_answer"] == "Final Answer"
            assert data["individual_responses"]["ChatGPT"] == "OpenAI response"

@pytest.mark.asyncio
async def test_chat_endpoint_offline_model():
    # Mock fetch_ollama
    with patch("api.fetch_ollama", new_callable=AsyncMock) as mock_ollama:
        mock_ollama.return_value = "Ollama response"
        
        with patch("api.synthesize_responses", new_callable=AsyncMock) as mock_synth:
            mock_synth.return_value = "Final Answer"
            
            payload = {
                "query": "Hello",
                "online_models": [],
                "offline_models": ["llama2"],
                "use_memory": False
            }
            
            response = client.post("/chat", json=payload)
            
            assert response.status_code == 200
            data = response.json()
            assert data["individual_responses"]["Ollama (llama2)"] == "Ollama response"
