from flask import jsonify, request
from flask_restful import Resource

from api.providers import get_provider

REQUIRED_KEYS = {"from", "to", "logs"}


class Extract(Resource):
    def post(self):
        # Validate provider
        provider_name = request.form.get("provider")
        if not provider_name:
            return {"error": "Missing 'provider' field in request"}, 400

        # Validate file
        if "file" not in request.files:
            return {"error": "Missing file in request"}, 400

        file = request.files["file"]
        if not file.filename:
            return {"error": "Empty filename"}, 400

        if not file.filename.lower().endswith(".pdf"):
            return {"error": "Invalid file type, expected PDF"}, 400

        try:
            provider = get_provider(provider_name)
        except ValueError as e:
            return {"error": str(e)}, 400

        try:
            data = provider.extract(file.read())
        except ValueError as e:
            return {"error": str(e)}, 502
        except RuntimeError as e:
            return {"error": str(e)}, 502
        except Exception as e:
            return {"error": str(e)}, 500

        # Validate structure
        if not all(key in data for key in REQUIRED_KEYS):
            return {"error": "Invalid document format"}, 400

        if data.get("error") == "Invalid document format":
            return {"error": "Invalid document format"}, 400

        return jsonify(data)
