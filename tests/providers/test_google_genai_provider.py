import pytest
from unittest.mock import patch, MagicMock
from aisuite.providers.google_genai_provider import GoogleGenaiProvider


@pytest.fixture(autouse=True)
def set_api_key_env_var(monkeypatch):
    """Fixture to set environment variables for tests."""
    monkeypatch.setenv("GEMINI_API_KEY", "test-gemini-api-key")


def test_google_genai_provider_initialization():
    """Test the initialization of GoogleGenaiProvider."""
    provider = GoogleGenaiProvider(api_key="test-gemini-api-key")
    assert provider.api_key == "test-gemini-api-key"
    assert provider.client is not None


def test_google_genai_provider_chat_completions_create():
    """Test the chat_completions_create method of GoogleGenaiProvider."""
    provider = GoogleGenaiProvider(api_key="test-gemini-api-key")
    messages = [{"role": "user", "content": "Hello!"}]
    model = "gemini-2.0-flash-exp"
    response_text_content = "mocked-text-response-from-model"

    mock_response = MagicMock()
    mock_response.text = response_text_content

    with patch.object(provider.client.models, "generate_content", return_value=mock_response) as mock_generate_content:
        response = provider.chat_completions_create(model=model, messages=messages)

        mock_generate_content.assert_called_with(
            model=model,
            contents=[message["content"] for message in messages]
        )

        assert response.choices[0].message.content == response_text_content
