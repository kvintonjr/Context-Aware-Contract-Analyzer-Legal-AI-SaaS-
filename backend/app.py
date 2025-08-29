import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from pathlib import Path

def create_app(testing=False):
    """Application factory"""
    app = Flask(__name__)
    CORS(app)

    # In testing, the key will be set in the test setup.
    # In production, we load it from the .env file.
    if not testing:
        # Manually load .env file
        dotenv_path = Path(__file__).parent / '.env'
        if dotenv_path.exists():
            with open(dotenv_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        os.environ.setdefault(key.strip(), value.strip())

    # We need a client to exist for the app to work.
    # In a real app, you might put this on g or the app context.
    # For testing, we will mock the client's methods.
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    @app.route('/analyze', methods=['POST'])
    def analyze_contract():
        data = request.get_json()
        contract_text = data.get('contract_text', '')

        if not contract_text:
            return jsonify({"error": "No contract text provided"}), 400

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful legal assistant. Analyze the provided contract text and return a summary, a list of potential risks, and a risk score from 0 to 100. The response should be in JSON format with keys 'summary', 'risks', and 'risk_score'. The 'risks' should be a list of objects, each with 'clause', 'risk_level', and 'explanation'."},
                    {"role": "user", "content": contract_text}
                ],
                response_format={ "type": "json_object" }
            )
            analysis = response.choices[0].message.content
            return analysis, 200, {'Content-Type': 'application/json'}

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
