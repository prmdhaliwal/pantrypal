import pytest

from app.llm_providers import LLMProviderConfig, build_llm_client_from_env
from app.openai_provider import OpenAIResponsesClient


class FakeClient:
    def generate(self, prompt: str) -> str:
        return prompt


def test_build_llm_client_from_env_returns_none_without_provider():
    client = build_llm_client_from_env({})

    assert client is None


def test_build_llm_client_from_env_uses_registered_provider_builder():
    calls = {}

    def build_fake_client(config: LLMProviderConfig) -> FakeClient:
        calls["config"] = config
        return FakeClient()

    client = build_llm_client_from_env(
        {
            "LLM_PROVIDER": "fake",
            "LLM_MODEL": "fake-model",
            "LLM_API_KEY": "fake-key",
        },
        provider_builders={"fake": build_fake_client},
    )

    assert isinstance(client, FakeClient)
    assert calls["config"] == LLMProviderConfig(
        provider="fake",
        model="fake-model",
        api_key="fake-key",
    )


def test_build_llm_client_from_env_rejects_unknown_provider():
    with pytest.raises(ValueError, match="Unsupported LLM provider: unknown"):
        build_llm_client_from_env(
            {"LLM_PROVIDER": "unknown"},
            provider_builders={},
        )


def test_build_llm_client_from_env_uses_openai_api_key_alias():
    client = build_llm_client_from_env(
        {
            "LLM_PROVIDER": "openai",
            "LLM_MODEL": "gpt-test",
            "OPENAI_API_KEY": "openai-key",
        }
    )

    assert isinstance(client, OpenAIResponsesClient)
    assert client.api_key == "openai-key"
    assert client.model == "gpt-test"
