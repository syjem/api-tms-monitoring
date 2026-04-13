import os
import json

from google import genai
from google.genai import types
from google.genai.errors import ClientError, ServerError

from api.providers.base import BaseProvider
from api.services import PROMPT


class GeminiProvider(BaseProvider):
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def extract(self, file_bytes: bytes) -> dict:
        try:
            part = types.Part.from_bytes(
                data=file_bytes, mime_type="application/pdf")

            response = self.client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=[part, PROMPT],
                config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(thinking_budget=0),
                    response_mime_type="application/json",
                ),
            )

            return json.loads(response.text)

        except json.JSONDecodeError:
            raise ValueError("Invalid JSON from Gemini")

        except ClientError as e:
            if e.code == 429:
                raise RuntimeError(
                    "Rate limit exceeded. Please try again later.")
            raise RuntimeError(f"Gemini client error: {e.code}: {e.message}")

        except ServerError as e:
            if e.code == 503:
                raise RuntimeError(
                    "Gemini is currently overloaded. Please try again later.")
            raise RuntimeError(f"Gemini server error: {e.code} - {e.message}")
