import httpx


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"


class OpenAIResponsesClient:
    def __init__(
        self,
        api_key: str,
        model: str,
        http_client: httpx.Client | None = None,
    ) -> None:
        self.api_key = api_key
        self.model = model
        self.http_client = http_client or httpx.Client(timeout=30)

    def generate(self, prompt: str) -> str:
        response = self.http_client.post(
            OPENAI_RESPONSES_URL,
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "model": self.model,
                "input": prompt,
            },
        )
        response.raise_for_status()
        return _extract_response_text(response.json())


def _extract_response_text(payload: dict) -> str:
    output_text = payload.get("output_text")
    if isinstance(output_text, str):
        return output_text

    for output_item in payload.get("output", []):
        if not isinstance(output_item, dict):
            continue

        for content_item in output_item.get("content", []):
            if not isinstance(content_item, dict):
                continue

            if content_item.get("type") == "output_text":
                text = content_item.get("text")
                if isinstance(text, str):
                    return text

    raise KeyError("output_text")
