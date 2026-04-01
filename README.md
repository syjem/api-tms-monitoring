# Flask PDF Extraction API

This repository contains a lightweight **Python/Flask REST API** that uses Google’s **Gemini API** to extract structured data from PDF files.

The API exposes a single endpoint:  
`POST /api/extract`

---

## Features

- Upload PDF files and extract structured JSON using Gemini (`gemini-2.5-flash`).
- Returns clean, parseable JSON for easy frontend mapping.

---

## Requirements

- Python 3.9+
- [Google Generative AI Python SDK](https://pypi.org/project/google-genai/)
- Flask & Flask-RESTful
- Flask-CORS
- python-dotenv

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/syjem/api-tms-monitoring.git
   cd api-tms-monitoring-server
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/Mac
   .venv\Scripts\activate      # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a .env file in the project root:

   ```bash
   GEMINI_API_KEY=your_google_gemini_api_key
   ```

5. Create a .flaskenv file in the project root:

   ```bash
   export FLASK_APP=api/app.py
   export FLASK_DEBUG=True
   ```

## Usage

1. Run the Flask app:

   ```bash
   flask run
   ```

2. By default, the API runs at:

   ```bash
   http://127.0.0.1:5000
   ```
