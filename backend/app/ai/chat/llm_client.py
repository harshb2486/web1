from typing import Dict, Optional
from app.core.config import settings


class LLMClient:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL

    async def generate(self, prompt: str, system_prompt: str = "") -> str:
        if not self.api_key:
            return self._mock_response(prompt)

        try:
            import httpx
            async with httpx.AsyncClient() as client:
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": prompt})

                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self.model,
                        "messages": messages,
                        "max_tokens": 1000,
                        "temperature": 0.7,
                    },
                    timeout=30.0,
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            return self._mock_response(prompt)

    def _mock_response(self, prompt: str) -> str:
        return (
            "I've analyzed your request based on the available data. "
            "Here are my findings:\n\n"
            "Based on your channel analytics and current trends, "
            "I recommend focusing on content that aligns with your "
            "audience's interests and current trend momentum.\n\n"
            "Would you like me to dive deeper into any specific area?"
        )
