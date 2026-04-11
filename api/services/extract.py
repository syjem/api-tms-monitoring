import os
import re
import json

from flask import jsonify, request
from flask_restful import Resource
from google import genai
from google.genai import types
from google.genai.errors import ClientError, ServerError
from api.services import PROMPT


class Extract(Resource):
    def post(self):
        client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

        # Validate file input
        if "file" not in request.files:
            return {"error": "Missing file in request"}, 400

        file = request.files["file"]
        if not file.filename:
            return {"error": "Empty filename"}, 400

        if not file.filename.lower().endswith(".pdf"):
            return {"error": "Invalid file type, expected PDF"}, 400

        try:
            part = types.Part.from_bytes(
                data=file.read(),
                mime_type="application/pdf"
            )

            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=[part, PROMPT],
                config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(thinking_budget=0),
                    response_mime_type="application/json",
                ),
            )

            # Parse JSON safely
            try:
                data = json.loads(response.text)
            except json.JSONDecodeError:
                return {"error": "Invalid JSON from Gemini"}, 500

            # Validate expected JSON structure
            required_keys = {"from", "to", "logs"}
            if not all(key in data for key in required_keys):
                return {"error": "Invalid document format"}, 400

            if "error" in data and data.get("error") == "Invalid document format":
                return {"error": "Invalid document format"}, 400

            return jsonify(data)

        except ClientError as e:
            if e.code == 429:
                return {"error": "Rate limit exceeded. Please try again later."}, 429
            return {"error": f"Gemini client error: {e.code}: {e.message}"}, e.code

        except ServerError as e:
            if e.code == 503:
                return {"error": "Gemini is currently overloaded. Please try again later."}, 503
            return {"error": f"Gemini server error: {e.code} - {e.message}"}, e.code

        except Exception as e:
            return {"error": str(e)}, 500
