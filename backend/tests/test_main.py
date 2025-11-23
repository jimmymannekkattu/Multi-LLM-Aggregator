import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Multi-LLM Aggregator API is running"}

@patch("main.get_all_responses")
@patch("main.synthesize_responses")
def test_ask_endpoint(mock_synthesize, mock_get_all):
    # Setup mocks
    mock_get_all.return_value = {
        "ChatGPT": "Res 1",
        "Claude": "Res 2",
        "Gemini": "Res 3",
        "Perplexity": "Res 4"
    }
    mock_synthesize.return_value = "Final Answer"
    
    payload = {"query": "What is AI?"}
    response = client.post("/ask", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["final_answer"] == "Final Answer"
    assert data["individual_responses"]["ChatGPT"] == "Res 1"
