import logging
import os

from flask import Flask, render_template, request
import base64
import requests
from flask import jsonify
from rich.markdown import Markdown
from dotenv import load_dotenv

load_dotenv()

# Set the logging level to INFO
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)


class ImageAnalyzer:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    @staticmethod
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def analyze_image(self, image_path):
        base64_image = self.encode_image(image_path)
        with open('system.md', 'r') as file:
            prompt = file.read()
        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]
                }
            ],
            "max_tokens": 100
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=self.headers, json=payload)
        return response.json()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        # Ensure the upload directory exists
        upload_dir = 'uploads/'
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        # Save the uploaded file
        file_path = upload_dir + file.filename
        file.save(file_path)
        # Analyze the image
        analyzer = ImageAnalyzer(api_key=os.getenv('OPENAI_API_KEY'))
        response = analyzer.analyze_image(file_path)
        markdown_response = Markdown(str(response))
        print(markdown_response)
        return jsonify(response)

    return "Error"


if __name__ == '__main__':
    app.run(debug=True)
