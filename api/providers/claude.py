import os
import json
import base64

import anthropic

from api.providers.base import BaseProvider
from api.services import PROMPT


class ClaudeProvider(BaseProvider):
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY"))

    def extract(self, file_bytes: bytes) -> dict:
        try:
            pdf_data = base64.standard_b64encode(file_bytes).decode("utf-8")

            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "document",
                                "source": {
                                    "type": "base64",
                                    "media_type": "application/pdf",
                                    "data": pdf_data,
                                },
                            },
                            {
                                "type": "text",
                                "text": PROMPT
                            }
                        ],
                    }
                ],
            )

            return json.loads(response.content[0].text)

        except json.JSONDecodeError:
            raise ValueError("Invalid JSON from Claude")

        except anthropic.RateLimitError:
            raise RuntimeError("Rate limit exceeded. Please try again later.")

        except anthropic.APIStatusError as e:
            raise RuntimeError(
                f"Claude API error: {e.status_code} - {e.message}")
