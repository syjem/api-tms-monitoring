from google import genai
from google.genai import types
from google.genai.errors import ServerError
import time


class GeminiHealthCheck:
    def __init__(self, model="gemini-2.5-flash-lite"):
        self.client = genai.Client()
        self.model = model

    def check(self) -> dict:
        """
        Perform a health check on Gemini's availability.

        Returns a dict with:
          - status: "healthy" | "degraded" | "unhealthy"
          - latency_ms: round-trip time in milliseconds (if reachable)
          - model: the model used for the check
          - error: error message (if unhealthy or degraded)
        """
        start = time.monotonic()

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents="ping",
                config=types.GenerateContentConfig(
                    max_output_tokens=1,
                ),
            )
            latency_ms = round((time.monotonic() - start) * 1000, 2)

            # A valid response with no candidates signals content filtering / empty reply
            if not response.candidates:
                return {
                    "status": "degraded",
                    "latency_ms": latency_ms,
                    "model": self.model,
                    "error": "No candidates returned — possible content filtering issue",
                }

            return {
                "status": "healthy",
                "latency_ms": latency_ms,
                "model": self.model,
            }

        except ServerError as e:
            # 5xx errors: Gemini-side outage or overload
            latency_ms = round((time.monotonic() - start) * 1000, 2)
            return {
                "status": "unhealthy",
                "latency_ms": latency_ms,
                "model": self.model,
                "error": f"Server error {e.code}: {e.message}",
            }

        except Exception as e:
            # Network timeouts, DNS failures, unexpected errors
            latency_ms = round((time.monotonic() - start) * 1000, 2)
            return {
                "status": "unhealthy",
                "latency_ms": latency_ms,
                "model": self.model,
                "error": f"Unexpected error: {str(e)}",
            }
