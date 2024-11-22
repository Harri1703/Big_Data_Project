from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
import re

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize Hugging Face's transformer-based question-answering pipeline
qa_pipeline = pipeline("question-answering")

# Path to the document
file_path = r"D:\Harri\Projects\Big Data Project\chatbot_vit\src\flask\pdf_content.txt"
with open(file_path, "r") as file:
    document_text = file.read()

@app.route("/ask", methods=["POST"])
def ask_question():
    """
    Endpoint to handle user questions and return answers based on the loaded text.
    """
    try:
        # Get the user question from the request
        data = request.get_json()
        question = data.get("question")

        if not question:
            return jsonify({"error": "Question is required."}), 400

        # Use Hugging Face's transformer model to get the answer
        answer = qa_pipeline(question=question, context=document_text)

        # Return the answer
        return jsonify({
            "question": question,
            "answer": answer['answer']
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
