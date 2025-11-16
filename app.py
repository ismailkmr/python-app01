from flask import Flask, request, jsonify
from flask_cors import CORS
import json, os

app = Flask(__name__)
CORS(app)
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.json')

# Ensure JSON file exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

@app.route('/api/data', methods=['POST'])
def save_data():
    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify({"error": "Expected JSON object"}), 400
    with open(DATA_FILE, 'r+') as f:
        try:
            existing = json.load(f)
        except json.JSONDecodeError:
            existing = []
        existing.append(data)
        f.seek(0)
        json.dump(existing, f, indent=4)
        f.truncate()
    return jsonify({"message": "Data saved successfully"}), 201

@app.route('/api/data', methods=['GET'])
def get_data():
    with open(DATA_FILE) as f:
        try:
            existing = json.load(f)
        except json.JSONDecodeError:
            existing = []
    return jsonify(existing)

if __name__ == '__main__':
    # default port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
