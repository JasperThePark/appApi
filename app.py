from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

leaderboards = {
    "arithmetic": [],
    "algebra": [],
    "probability": []
}

@app.route("/")
def home():
    return "Leaderboard API running!"

@app.route("/leaderboard/<mode>", methods=["GET"])
def get_leaderboard(mode):
    if mode not in leaderboards:
        return jsonify({"status": "fail", "reason": "Invalid mode"}), 400
    # Return sorted top 3 by time
    sorted_list = sorted(leaderboards[mode], key=lambda x: x["time"])[:3]
    return jsonify(sorted_list)

@app.route("/submit", methods=["POST"])
def submit_score():
    data = request.get_json()
    name = data.get("name")
    mode = data.get("mode")
    score = data.get("score")
    time = data.get("time")

    if not (name and mode and score is not None and time is not None):
        return jsonify({"status": "fail", "reason": "Missing fields"}), 400
    if score != 100:
        return jsonify({"status": "fail", "reason": "Score must be 100"}), 400
    if mode not in leaderboards:
        return jsonify({"status": "fail", "reason": "Invalid mode"}), 400

    board = leaderboards[mode]
    board.append({"name": name, "time": time})
    board.sort(key=lambda x: x["time"])
    leaderboards[mode] = board[:3]

    return jsonify({"status": "success", "leaderboard": leaderboards[mode]})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
