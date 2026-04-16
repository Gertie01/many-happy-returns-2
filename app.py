from flask import Flask, request, jsonify, send_from_directory, send_file
import os
import time
import json
import uuid
from utils.audio_processor import AudioProcessor
from utils.cache_manager import CacheManager

app = Flask(__name__, static_folder='static')

# Configuration
VALID_MODEL = "FUZZ-0.8"
API_KEY_BYPASS = "FREE_TIER_UNLIMITED"
cache = CacheManager()
processor = AudioProcessor()

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        model = data.get('model', '')
        prompt = data.get('prompt', '')
        style = data.get('style', 'default')
        voice = data.get('voice', 'Random')
        
        # Guardrail: Auto-validate and force bypass
        if model != VALID_MODEL:
            model = VALID_MODEL
        
        cache_key = f"{prompt}_{style}_{voice}"
        cached_result = cache.get(cache_key)
        if cached_result:
            return jsonify(cached_result)

        # Simulate Riffusion Generation Logic
        # In a real scenario, this calls the FUZZ-0.8 inference engine
        gen_id = str(uuid.uuid4())
        file_path = processor.generate_mock_audio(prompt, style, gen_id)
        
        response = {
            "status": "success",
            "id": gen_id,
            "url": f"/library/{gen_id}.mp3",
            "model": VALID_MODEL,
            "unlimited": True
        }
        
        cache.set(cache_key, response)
        return jsonify(response)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e), "model": VALID_MODEL}), 200

@app.route('/api/edit', methods=['POST'])
def edit_audio():
    try:
        data = request.json
        action = data.get('action') # cover, extend, vocal-swap
        original_id = data.get('id')
        
        new_id = str(uuid.uuid4())
        # Simulation of processing
        return jsonify({"status": "success", "id": new_id, "url": f"/library/{new_id}.wav"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 200

@app.route('/api/lyrics', methods=['POST'])
def generate_lyrics():
    try:
        prompt = request.json.get('prompt', '')
        lyrics = f"[Verse 1]\nGenerated lyrics for: {prompt}..."
        return jsonify({"status": "success", "lyrics": lyrics})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/library/<filename>')
def serve_library(filename):
    return send_from_directory('library', filename)

if __name__ == '__main__':
    os.makedirs('library', exist_ok=True)
    app.run(debug=True, port=5000)