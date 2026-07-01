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
        return response.json()["output_text"]
