import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from agents import discovery
import g4f

@pytest.mark.asyncio
async def test_get_g4f_models():
    models = await discovery.get_g4f_models()
    assert isinstance(models, list)
    assert len(models) > 0
    assert models[0]["name"] == "gpt_4"

@pytest.mark.asyncio
async def test_verify_model_g4f_success():
    with patch("g4f.ChatCompletion.create_async", new_callable=AsyncMock) as mock_create:
        mock_create.return_value = "Hello"
        
        # Mock getattr for model resolution
        with patch("agents.discovery.getattr") as mock_getattr:
            mock_getattr.return_value = "dummy_model"
            with patch("agents.discovery.hasattr", return_value=True):
                
                success, response = await discovery.verify_model("gpt_4", "g4f")
                
                assert success is True
                assert response == "Hello"

@pytest.mark.asyncio
async def test_verify_model_g4f_invalid_model():
    with patch("agents.discovery.hasattr", return_value=False):
        success, response = await discovery.verify_model("invalid_model", "g4f")
        assert success is False
        assert "not found" in response

@pytest.mark.asyncio
async def test_verify_model_ollama_success():
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "Ollama says hi"}
        mock_post.return_value = mock_response
        
        success, response = await discovery.verify_model("llama2", "Ollama", base_url="http://localhost:11434")
        
        assert success is True
        assert response == "Ollama says hi"
        mock_post.assert_called_once()

@pytest.mark.asyncio
async def test_search_models_g4f():
    # Mock dir(g4f.models)
    with patch("builtins.dir", return_value=["gpt_4", "llama_v2", "_internal"]):
        results = await discovery.search_models("gpt")
        assert len(results) == 1
        assert results[0]["name"] == "gpt_4"
        assert results[0]["provider"] == "g4f"

@pytest.mark.asyncio
async def test_search_models_openrouter():
    # Mock get_openrouter_models
    with patch("agents.discovery.get_openrouter_models", new_callable=AsyncMock) as mock_or:
        mock_or.return_value = [
            {"name": "openai/gpt-4", "display": "GPT-4"},
            {"name": "meta/llama-2", "display": "Llama 2"}
        ]
        
        results = await discovery.search_models("llama", openrouter_key="test_key")
        
        # Should find llama from OpenRouter (and potentially g4f if not mocked out, but here we test OR path)
        # We need to mock dir again to isolate OR or just check if OR result is present
        found_or = any(r["provider"] == "OpenRouter" and "llama" in r["name"] for r in results)
        assert found_or is True
