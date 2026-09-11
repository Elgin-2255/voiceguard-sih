from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/')
def home():
    return "VoiceGuard backend running"

@app.route('/check', methods=['POST'])
def check():
    return jsonify({"result": "Real voice", "confidence": 92})

if __name__ == '__main__':
    app.run(debug=True)