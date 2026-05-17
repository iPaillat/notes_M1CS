import os
import requests
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

NOTES_URL = "https://raw.githubusercontent.com/Gladrat/notes_M1CS/main/notes.json"
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")


@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/notes")
def notes():
    try:
        r = requests.get(NOTES_URL, timeout=5)
        r.raise_for_status()
        data = r.json()
        if "etudiants" not in data:
            raise ValueError("invalid structure")
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
        r = requests.get(NOTES_URL, timeout=5)
        r.raise_for_status()
        data = r.json()
    except Exception:
        return jsonify({"error": "Service temporairement indisponible"}), 503

    q = request.args.get("q", "").lower()
    results = [
        e for e in data["etudiants"]
        if q in e["nom"].lower() or q in e["prenom"].lower()
    ]
    return jsonify({**data, "etudiants": results})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
