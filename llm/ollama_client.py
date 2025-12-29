import requests
import time
import os

class OllamaClient:
    def __init__(
        self,
        model: str = "gemma3:4b",
        timeout: int = 180,
        max_retries: int = 3,
    ):
        self.model = model
        self.timeout = timeout
        self.max_retries = max_retries
        host = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11500").rstrip("/")
        self.url = f"{host}/api/generate"


    def generate(self, system_prompt: str, user_input: str) -> str:
        prompt = f"{system_prompt}\n\n{user_input}"
        last_exception = None

        for attempt in range(1, self.max_retries + 1):
            try:
                response = requests.post(
                    self.url,
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                    },
                    timeout=self.timeout,
                )

                response.raise_for_status()
                return response.json()["response"].strip()

            except Exception as e:
                last_exception = e
                time.sleep(3 * attempt)

        raise RuntimeError(f"Ollama request failed after retries: {last_exception}")
