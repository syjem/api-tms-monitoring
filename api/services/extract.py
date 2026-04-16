import hmac
import os

from flask import jsonify, request
from flask_restful import abort, Resource

from api.providers import get_provider

REQUIRED_KEYS = {"from", "to", "logs"}

EXTRACT_API_KEY = os.getenv("EXTRACT_API_KEY")
if not EXTRACT_API_KEY:
    raise RuntimeError("EXTRACT_API_KEY environment variable is not set")


class Extract(Resource):
    def post(self):
        # Validate headers
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            abort(401, error="Missing 'Authorization' header")

        # Validate Bearer format
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            abort(401, error="Invalid Authorization format. Expected 'Bearer <token>'")

        token = parts[1]

        # hmac constant-time comparison
        if not hmac.compare_digest(token, EXTRACT_API_KEY):
            abort(401, error="Invalid token")

        # Validate provider
        provider_name = request.form.get("provider")
        if not provider_name:
            abort(400, error="Missing 'provider' field in request")

        # Validate file
        if "file" not in request.files:
            abort(400, error="Missing file in request")

        file = request.files["file"]
        if not file.filename:
            abort(400, error="Empty filename")

        if not file.filename.lower().endswith(".pdf"):
            abort(400, error="Invalid file type, expected PDF")

        try:
            provider = get_provider(provider_name)
        except ValueError as e:
            abort(400, error=str(e))

        try:
            data = provider.extract(file.read())
        except ValueError as e:
            abort(502, error=str(e))
        except RuntimeError as e:
            abort(502, error=str(e))
        except Exception as e:
            abort(500, error=str(e))

        # Validate structure
        if not all(key in data for key in REQUIRED_KEYS):
            abort(400, error="Invalid document format")

        if data.get("error") == "Invalid document format":
            abort(400, error="Invalid document format")

        return jsonify(data)
