import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add parent directory to path to import api
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to AI Nexus API" in response.json()["message"]

def test_get_models():
    response = client.get("/models")
    assert response.status_code == 200
    data = response.json()
    assert "online" in data
    assert "offline" in data
    assert isinstance(data["online"], list)
    assert isinstance(data["offline"], list)

def test_cors_headers():
    # Simulate a cross-origin request
    response = client.options(
        "/",
        headers={
            "Origin": "http://example.com",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "*"
    assert response.headers["access-control-allow-methods"] == "*"
