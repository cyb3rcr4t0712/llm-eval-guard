import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()


class GeminiClient:
    def __init__(
        self,
        model: str = "gemini-2.0-flash",
        temperature: float = 0.2,
        max_retries: int = 3,
    ):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise EnvironmentError("GEMINI_API_KEY not found")

        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_retries = max_retries

    def generate(self, system_prompt: str, user_input: str) -> str:
        prompt = f"{system_prompt}\n\n{user_input}"

        last_exception = None
        for attempt in range(1, self.max_retries + 1):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config={"temperature": self.temperature},
                )

                return response.text.strip()
            
            except Exception as e:
                last_exception = e
                time.sleep(2 * attempt)

        raise RuntimeError(f"Gemini request failed after retries: {last_exception}")
