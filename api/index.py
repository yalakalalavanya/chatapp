from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
import os
# Replace with your actual API key
API_URL = os.getenv('API_URL')
API_KEY = os.getenv('API_KEY')

from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        # Rest of your code

    def do_POST(self):
        # Handle POST requests here
        pass
import requests

def get_bot_response_google_ai(user_message):
    try:
        # Create the payload according to the example provided
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": user_message
                        }
                    ]
                }
            ]
        }
        
        # Make the API request with API key as query parameter
        response = requests.post(f"{API_URL}?key={API_KEY}", json=data, headers={'Content-Type': 'application/json'})
        
        # Log or print the full response
        response_json = response.json()
        print("Response Status Code:", response.status_code)
        print("Response JSON:", response_json)
        
        # Extract the text content from the response
        if response.status_code == 200:
            candidates = response_json.get('candidates', [])
            if len(candidates) > 0:
                content = candidates[0].get('content', {})
                parts = content.get('parts', [])
                if len(parts) > 0:
                    return parts[0].get('text', 'No text found in response')
            return 'No content found in response'
        else:
            return f"Error: {response.status_code} - {response.text}"
    
    except Exception as e:
        return f"Error: {e}"


@app.route('/')
def chat():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.json.get('message')
    response = get_bot_response_google_ai(message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
