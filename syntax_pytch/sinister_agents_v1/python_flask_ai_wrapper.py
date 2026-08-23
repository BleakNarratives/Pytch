"""
[DNA_TAG]
ORIGIN: Moto4_A9
PILLAR: valet_concierge
PATH: python_flask_ai_wrapper.py
LAST_SYNC: 2026-08-02T01:13:33Z
[/DNA_TAG]
"""
import os
import requests
import json
from flask import Flask, render_template_string, request, jsonify

# You'll need to install Flask and requests.
# To do so, open your terminal and run:
# pip install Flask requests

# --- HTML Template (Embedded for simplicity) ---
# This is a single-page app that uses Tailwind CSS for styling.
# It has a form to submit a prompt and an area to display the AI's response.
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Wrapper Jig</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {
            font-family: 'Inter', sans-serif;
        }
    </style>
</head>
<body class="bg-gray-900 text-white min-h-screen flex items-center justify-center p-4">
    <div class="bg-gray-800 p-8 rounded-xl shadow-lg w-full max-w-2xl">
        <h1 class="text-3xl font-bold text-center mb-6">AI Wrapper Jig</h1>
        <p class="text-center text-gray-400 mb-8">
            Enter a prompt and get a response from the Gemini AI model.
        </p>

        <form id="ai-form" class="space-y-4">
            <textarea id="prompt-input" rows="6" class="mt-2 p-3 w-full rounded-lg bg-gray-700 text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Type your prompt here..."></textarea>
            
            <button type="submit" id="submit-button" class="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg transition-colors duration-200 shadow-md">
                Generate Response
            </button>
        </form>

        <div id="response-container" class="mt-6">
            <h2 class="text-2xl font-bold mb-2">AI's Response:</h2>
            <div id="response-output" class="bg-gray-700 p-4 rounded-lg text-gray-300 whitespace-pre-wrap">
                <!-- AI response will appear here -->
            </div>
            <div id="loading-spinner" class="hidden text-center mt-4">
                <svg class="animate-spin h-8 w-8 text-white mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
            </div>
        </div>
    </div>

    <script>
        const form = document.getElementById('ai-form');
        const promptInput = document.getElementById('prompt-input');
        const responseOutput = document.getElementById('response-output');
        const submitButton = document.getElementById('submit-button');
        const loadingSpinner = document.getElementById('loading-spinner');

        form.addEventListener('submit', async (event) => {
            event.preventDefault();
            const prompt = promptInput.value;

            if (!prompt) {
                responseOutput.textContent = 'Please enter a prompt.';
                return;
            }

            // Show loading state
            submitButton.disabled = true;
            submitButton.textContent = 'Generating...';
            loadingSpinner.classList.remove('hidden');
            responseOutput.textContent = '';

            try {
                // Fetch response from our Flask backend
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ prompt })
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                responseOutput.textContent = data.response;
            } catch (error) {
                console.error('Error:', error);
                responseOutput.textContent = 'An error occurred. Please try again.';
            } finally {
                // Hide loading state
                submitButton.disabled = false;
                submitButton.textContent = 'Generate Response';
                loadingSpinner.classList.add('hidden');
            }
        });
    </script>
</body>
</html>
"""

# --- Flask Application Setup ---
app = Flask(__name__)

# This is the API key. You must replace the placeholder with your actual API key.
# It is recommended to use environment variables in a real application.
# You can get one from https://makersuite.google.com/
API_KEY = ""
# If you leave the API key as is, the canvas environment will automatically provide one.

# This is the model we will use.
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent"

# --- Flask Routes ---
@app.route('/')
def index():
    """Renders the single-page HTML template."""
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate', methods=['POST'])
def generate_response():
    """Handles the request to generate AI text."""
    try:
        data = request.get_json()
        user_prompt = data.get('prompt')

        if not user_prompt:
            return jsonify({'response': 'No prompt provided.'}), 400

        # Construct the payload for the Gemini API call
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": user_prompt}
                    ]
                }
            ]
        }
        headers = {'Content-Type': 'application/json'}

        # Make the API call to Gemini
        # We will use exponential backoff for retries
        retries = 0
        max_retries = 5
        base_delay = 1.0  # seconds
        response = None

        while retries < max_retries:
            try:
                response = requests.post(
                    f"{API_URL}?key={API_KEY}",
                    headers=headers,
                    data=json.dumps(payload)
                )

                if response.status_code == 429: # Too many requests
                    delay = base_delay * (2 ** retries)
                    print(f"Rate limit hit. Retrying in {delay} seconds...")
                    time.sleep(delay)
                    retries += 1
                else:
                    response.raise_for_status() # Raise an error for bad status codes
                    break

            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}. Retrying...")
                delay = base_delay * (2 ** retries)
                time.sleep(delay)
                retries += 1
                response = None

        if response is None:
            return jsonify({'response': 'Failed to connect to the API after multiple retries.'}), 500

        api_response_data = response.json()

        # Check for candidates and content in the response
        if 'candidates' in api_response_data and len(api_response_data['candidates']) > 0:
            candidate = api_response_data['candidates'][0]
            if 'content' in candidate and 'parts' in candidate['content'] and len(candidate['content']['parts']) > 0:
                generated_text = candidate['content']['parts'][0]['text']
                return jsonify({'response': generated_text})
            else:
                return jsonify({'response': 'API response content is missing or malformed.'}), 500
        else:
            return jsonify({'response': 'No candidates found in API response.'}), 500

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({'response': f'An unexpected error occurred: {e}'}), 500

if __name__ == '__main__':
    # You can run this app by simply executing this file.
    # It will automatically reload if you make changes.
    app.run(debug=True)