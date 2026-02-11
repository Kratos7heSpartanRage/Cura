import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class LLM:
    def __init__(self, model: str = "llama-3.1-8b-instant"):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables.")

        self.client = Groq(api_key=api_key)
        self.model = model

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,
            )

            content = response.choices[0].message.content

            if content is None:
                return ""

            return content.strip()

        except Exception as e:
            print(f"❌ LLM Error: {e}")
            return ""

