import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import llm_providers
import g4f

@pytest.mark.asyncio
async def test_fetch_g4f_success():
    # Mock g4f.ChatCompletion.create_async
    with patch("g4f.ChatCompletion.create_async", new_callable=AsyncMock) as mock_create:
        mock_create.return_value = "Hello from g4f"
        
        # Mock getattr to return a dummy model object
        with patch("llm_providers.getattr") as mock_getattr:
            mock_getattr.return_value = "dummy_model_obj"
            with patch("llm_providers.hasattr", return_value=True):
                
                response = await llm_providers.fetch_g4f("Hi", "gpt_4", "TestProvider")
                
                assert "Hello from g4f" in response
                assert "Source: Free Web" in response
                mock_create.assert_called_once()

@pytest.mark.asyncio
async def test_fetch_g4f_failure():
    with patch("g4f.ChatCompletion.create_async", new_callable=AsyncMock) as mock_create:
        mock_create.side_effect = Exception("Network error")
        
        response = await llm_providers.fetch_g4f("Hi", "gpt_4", "TestProvider")
        
        assert "Error (TestProvider - Free Web)" in response
        assert "Network error" in response

@pytest.mark.asyncio
async def test_fetch_openai_success():
    mock_client = AsyncMock()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Hello from OpenAI"}}]
    }
    mock_client.post.return_value = mock_response

    with patch.dict("os.environ", {"OPENAI_API_KEY": "sk-test"}):
        response = await llm_providers.fetch_openai("Hi", mock_client)
        assert response == "Hello from OpenAI"

@pytest.mark.asyncio
async def test_fetch_openai_no_key_fallback():
    # Should fallback to g4f if no key
    with patch.dict("os.environ", {}, clear=True):
        with patch("llm_providers.fetch_g4f", new_callable=AsyncMock) as mock_g4f:
            mock_g4f.return_value = "Fallback response"
            
            response = await llm_providers.fetch_openai("Hi", AsyncMock())
            assert response == "Fallback response"
            mock_g4f.assert_called_once()
