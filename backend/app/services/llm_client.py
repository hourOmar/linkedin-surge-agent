from google import genai

from app.core.config import settings


class LLMClient:
    """Single wrapper around the Gemini API (Google AI Studio). No other module should import `google.genai` directly."""

    def __init__(self) -> None:
        self._client = genai.Client(api_key=settings.google_api_key)

    def generate(self, prompt: str) -> str:
        response = self._client.models.generate_content(
            model=settings.model_name,
            contents=prompt,
            config={"temperature": settings.temperature},
        )
        return response.text


llm_client = LLMClient()
