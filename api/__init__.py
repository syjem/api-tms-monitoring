allowed_origins = ["https://tms-monitoring.vercel.app"]

html_template = """
<!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <meta name="description" content="API documentation for Employee Monitoring System" />
            <link
                rel="icon"
                href="{{ url_for('static', filename='favicon.png') }}"
            />
            <title>API - Employee Monitoring</title>
            <style>
                * {
                    box-sizing: border-box;
                }
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 2rem auto;
                    padding: 1rem;
                    line-height: 1.6;
                }
                h1 {
                    text-align: center;
                    color: #333;
                    font-size: 20px;
                    margin-bottom: 3rem;
                }
                div.container {
                    background-color: #f9f9f9;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    padding: 1rem;
                    box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.1);
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                    margin-bottom: 1rem;
                }
                code {
                    font-family: "Courier New", Courier, monospace;
                    font-size: 14px;
                    font-weight: 500;
                    padding: 0.2rem 0.4rem;
                    border-radius: 4px;
                }
                code.get {
                    color: black;
                    background: oklch(97.9% 0.021 166.113);
                }

                code.post {
                    color: black;
                    background: oklch(97.1% 0.013 17.38);
                }

                strong {
                    font-size: 12px;
                    font-weight: 700;
                    padding: 0.3rem 1rem;
                    border-radius: 4px;
                }
                strong.get {
                    color: green;
                    background: oklch(84.5% 0.143 164.978);
                }
                strong.post {
                    color: red;
                    background: oklch(93.6% 0.032 17.717);
                }
            </style>
        </head>
        <body>
            <main>
                <h1>The API exposes two endpoints: </h1>
                <div class="container">
                    <strong class="get">GET</strong>
                    <code class="get">/api/health</code>
                </div>
                <div class="container">
                    <strong class="post">POST</strong>
                    <code class="post">/api/extract</code>
                </div>
            </main>
        </body>
    </html>
"""
