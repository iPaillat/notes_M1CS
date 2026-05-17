import os
import time
import requests
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

NOTES_URL = "https://raw.githubusercontent.com/Gladrat/notes_M1CS/main/notes.json"
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")

_cache = {"data": None, "ts": 0}


def fetch_notes():
    now = time.time()
    if _cache["data"] and now - _cache["ts"] < 2:
        return _cache["data"]
    r = requests.get(NOTES_URL, timeout=5)
    r.raise_for_status()
    data = r.json()
    if "etudiants" not in data:
        raise ValueError("invalid structure")
    _cache["data"] = data
    _cache["ts"] = now
    return data


@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/notes")
def notes():
    try:
        data = fetch_notes()
    except Exception:
        return jsonify({"error": "Service temporairement indisponible"}), 503

    student_id = request.args.get("id")
    if student_id is not None:
        try:
            idx = int(student_id)
            etudiants = [data["etudiants"][idx]]
        except (ValueError, IndexError):
            return jsonify({"error": "Not found"}), 404
        return jsonify({**data, "etudiants": etudiants})

    return jsonify(data)


@app.route("/search")
def search():
    try:
        data = fetch_notes()
    except Exception:
        return jsonify({"error": "Service temporairement indisponible"}), 503

    q = request.args.get("q", "").lower()
    results = [
        e for e in data["etudiants"]
        if q in e["nom"].lower() or q in e["prenom"].lower()
    ]
    return jsonify({**data, "etudiants": results})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
