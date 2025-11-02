from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allows your frontend JS to fetch from Render

# In-memory leaderboard
leaderboards = {
    "arithmetic": [],
    "algebra": [],
    "probability": []
}
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

@app.route("/")
def home():
    return "Leaderboard API running!"

# Get leaderboard for a mode
@app.route("/leaderboard/<mode>", methods=["GET"])
def get_leaderboard(mode):
    if mode not in leaderboards:
        return jsonify([])  # return empty list if invalid mode
    # return top 3 sorted by time ascending
    sorted_board = sorted(leaderboards[mode], key=lambda x: x["time"])[:3]
    return jsonify(sorted_board)

# Submit a perfect score
@app.route("/submit", methods=["POST"])
def submit_score():
    data = request.get_json()
    name = data.get("name")
    mode = data.get("mode")
    score = data.get("score")
    time = data.get("time")

    if not all([name, mode, score, time]):
        return jsonify({"status": "fail", "reason": "Missing fields"}), 400

    if score != 100:
        return jsonify({"status": "fail", "reason": "Score not perfect"}), 400

    if mode not in leaderboards:
        return jsonify({"status": "fail", "reason": "Invalid mode"}), 400

    # Only add if faster than existing times
    board = leaderboards[mode]
    if len(board) < 3 or time < max([entry["time"] for entry in board]):
        board.append({"name": name, "time": time})
        # keep top 3 sorted
        leaderboards[mode] = sorted(board, key=lambda x: x["time"])[:3]

    return jsonify({"status": "success"})


