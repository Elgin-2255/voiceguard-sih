"""
VoiceGuard Backend - Smart India Hackathon 2026
AI Voice Deepfake Detection API
Frontend: index.html (GitHub Pages)
Backend: app.py (Python Flask)
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile

app = Flask(__name__)
CORS(app) # allow frontend on github.io to call this API

# --- Config ---
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a', 'ogg'}
MAX_FILE_SIZE = 10 * 1024 * 1024 # 10 MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_features(audio_path):
    """
    Placeholder for real ML feature extraction.
    For SIH final: use librosa MFCC + pretrained model.
    """
    # TODO: Integrate librosa + trained deepfake detection model
    file_size = os.path.getsize(audio_path)
    duration_estimate = file_size / 16000 # dummy
    return {
        "file_size": file_size,
        "duration_estimate": round(duration_estimate, 2)
    }

def predict_deepfake(features):
    """
    Placeholder prediction logic.
    Will be replaced with actual model.infer()
    """
    # Demo heuristic for prototype judging
    score = 82 + (features["file_size"] % 10)
    if score > 100:
        score = 87
    label = "Likely Real" if features["file_size"] % 2 == 0 else "AI-Cloned Suspected"
    return label, score

@app.route('/')
def home():
    return jsonify({
        "service": "VoiceGuard Backend",
        "status": "running",
        "version": "1.0-prototype",
        "endpoints": ["/health", "/check"]
    })

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/check', methods=['POST'])
def check_voice():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded. Use key 'file'"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Only wav, mp3, m4a, ogg allowed"}), 400

    # Save temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    try:
        features = extract_features(tmp_path)
        label, confidence = predict_deepfake(features)

        return jsonify({
            "filename": file.filename,
            "label": label,
            "confidence": confidence,
            "features": features,
            "note": "Prototype model for SIH demonstration"
        })
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)