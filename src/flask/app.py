from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os
from flask_cors import CORS

# Load environment variables from the .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Hugging Face API key
huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY")
if not huggingface_api_key:
    raise ValueError("Hugging Face API key is missing. Please check your .env file.")

# Hugging Face Inference API endpoint for Question Answering
API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-distilled-squad"

# Path to the text file where the PDF content is stored
TEXT_FILE_PATH = os.path.join(os.path.dirname(__file__), 'pdf_content.txt')

# Function to load text from the file
def load_text_from_file(file_path):
    """
    Loads text from a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The loaded text.
    """
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    return ""

# Load the text from the file into memory
pdf_text = load_text_from_file(TEXT_FILE_PATH)

# Function to query the Hugging Face Inference API
def query_huggingface_api(context, question):
    """
    Queries the Hugging Face Inference API with a given context and question.

    Args:
        context (str): The context text.
        question (str): The question to ask.

    Returns:
        dict: Response from the API.
    """
    headers = {"Authorization": f"Bearer {huggingface_api_key}"}
    payload = {
        "inputs": {
            "question": question,
            "context": context
        }
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.text}
    except Exception as e:
        return {"error": str(e)}

# Endpoint to handle user queries
@app.route('/query', methods=['POST'])
def query():
    """
    Handles POST requests to the /query endpoint.

    Expects JSON input with a "question" field.
    Returns the answer from the Hugging Face API.
    """
    data = request.get_json()
    question = data.get("question")

    # Check if a question was provided
    if not question:
        return jsonify({"error": "No question provided"}), 400

    # Limit the context length to avoid exceeding API limits
    context = pdf_text[:2000]

    # Query the Hugging Face API
    result = query_huggingface_api(context=context, question=question)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
