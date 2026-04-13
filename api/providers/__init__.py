from api.providers.gemini import GeminiProvider
from api.providers.claude import ClaudeProvider

PROVIDERS = {
    "gemini": GeminiProvider,
    "claude": ClaudeProvider,
}


def get_provider(name: str):
    provider_class = PROVIDERS.get(name.lower())
    if not provider_class:
        raise ValueError(
            f"Unsupported provider: '{name}'. Choose from: {list(PROVIDERS.keys())}")
    return provider_class()
