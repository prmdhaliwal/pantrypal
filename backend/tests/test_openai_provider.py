import json

import httpx

from app.llm_providers import build_llm_client_from_env
from app.openai_provider import OpenAIResponsesClient


def test_openai_responses_client_generates_text_with_responses_api():
    requests = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            json={"output_text": "Use the eggs and rice for fried rice."},
        )

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = OpenAIResponsesClient(
        api_key="test-key",
        model="gpt-test",
        http_client=http_client,
    )

    answer = client.generate("Pantry prompt")

    assert answer == "Use the eggs and rice for fried rice."
    assert requests[0].method == "POST"
    assert str(requests[0].url) == "https://api.openai.com/v1/responses"
    assert requests[0].headers["authorization"] == "Bearer test-key"
    assert json.loads(requests[0].content) == {
        "model": "gpt-test",
        "input": "Pantry prompt",
    }


def test_openai_responses_client_reads_nested_output_text():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "output": [
                    {
                        "type": "message",
                        "content": [
                            {
                                "type": "output_text",
                                "text": "Use the eggs and rice for fried rice.",
                            }
                        ],
                    }
                ]
            },
        )

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = OpenAIResponsesClient(
        api_key="test-key",
        model="gpt-test",
        http_client=http_client,
    )

    assert client.generate("Pantry prompt") == "Use the eggs and rice for fried rice."


def test_build_llm_client_from_env_registers_openai_provider():
    client = build_llm_client_from_env(
        {
            "LLM_PROVIDER": "openai",
            "LLM_MODEL": "gpt-test",
            "LLM_API_KEY": "test-key",
        }
    )

    assert isinstance(client, OpenAIResponsesClient)
