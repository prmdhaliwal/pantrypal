import os
from dataclasses import dataclass
from typing import Callable, Mapping

from app.assistant import LLMClient
from app.openai_provider import OpenAIResponsesClient


@dataclass(frozen=True)
class LLMProviderConfig:
    provider: str
    model: str | None = None
    api_key: str | None = None


ProviderBuilder = Callable[[LLMProviderConfig], LLMClient]


DEFAULT_PROVIDER_BUILDERS: Mapping[str, ProviderBuilder] = {
    "openai": lambda config: OpenAIResponsesClient(
        api_key=_required_value(config.api_key, "LLM_API_KEY"),
        model=_required_value(config.model, "LLM_MODEL"),
    )
}


def build_llm_client_from_env(
    env: Mapping[str, str] | None = None,
    provider_builders: Mapping[str, ProviderBuilder] | None = None,
) -> LLMClient | None:
    source = os.environ if env is None else env
    provider = source.get("LLM_PROVIDER")

    if not provider:
        return None

    builders = DEFAULT_PROVIDER_BUILDERS if provider_builders is None else provider_builders
    provider_key = provider.lower()

    if provider_key not in builders:
        raise ValueError(f"Unsupported LLM provider: {provider}")

    config = LLMProviderConfig(
        provider=provider_key,
        model=source.get("LLM_MODEL"),
        api_key=source.get("LLM_API_KEY") or source.get("OPENAI_API_KEY"),
    )
    return builders[provider_key](config)


def _required_value(value: str | None, name: str) -> str:
    if not value:
        raise ValueError(f"{name} is required")

    return value
