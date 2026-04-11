from flask import Flask, jsonify, render_template_string
from flask_cors import CORS
from flask_restful import Api
from dotenv import load_dotenv

from api import html_template, allowed_origins
from api.health import GeminiHealthCheck
from api.services.extract import Extract

app = Flask(__name__)
load_dotenv()

CORS(app, resources={r"/api/*": {
    "origins": allowed_origins,
    "methods": ["GET", "POST"]
}})

api = Api(app)


@app.route("/")
def index():
    return render_template_string(html_template)


@app.route("/api/health")
def health():
    flash = GeminiHealthCheck(model="gemini-2.5-flash")
    flash_lite = GeminiHealthCheck(model="gemini-2.5-flash-lite")

    return jsonify({
        "flash": flash.check(),
        "lite": flash_lite.check()
    })


api.add_resource(Extract, "/api/extract")
