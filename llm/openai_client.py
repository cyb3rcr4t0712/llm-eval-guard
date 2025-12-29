import os
import time
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class OpenAIClient:
    def __init__(
        self,
        model: str,
        temperature: float = 0.2,
        max_tokens: int = 512,
        timeout: int = 30,
        max_retries: int = 3,
    ):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise EnvironmentError("OPENAI_API_KEY not found")

        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.max_retries = max_retries

    def generate(self, system_prompt: str, user_input: str) -> str:
        last_exception: Optional[Exception] = None

        for attempt in range(1, self.max_retries + 1):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input},
                    ],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    timeout=self.timeout,
                )

                return response.choices[0].message.content.strip()

            except Exception as e:
                last_exception = e
                time.sleep(2 * attempt)

        raise RuntimeError(f"OpenAI request failed after retries: {last_exception}")
