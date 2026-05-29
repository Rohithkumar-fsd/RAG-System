from flask import Flask, request, jsonify
from flask_cors import CORS

from history_aware_generation import ask_question

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    question = data["question"]

    answer = ask_question(question)

    return jsonify({
        "answer": answer
    })

if __name__ == "__main__":
    app.run(debug=True)