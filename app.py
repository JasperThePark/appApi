from flask import Flask, request, jsonify
from operator import itemgetter

app = Flask(__name__)

# In-memory leaderboard: { mode: [ { "name": ..., "time": ... }, ... ] }
leaderboards = {
    "arithmetic": [],
    "algebra": [],
    "probability": []
}

# Max entries per leaderboard
TOP_N = 3

@app.route("/submit", methods=["POST"])
def submit_score():
    data = request.get_json()

    name = data.get("name")
    mode = data.get("mode")
    score = data.get("score")
    time = data.get("time")

    # Only accept perfect score
    if score != 100:
        return jsonify({"status": "fail", "reason": "Score must be 100"}), 400

    if mode not in leaderboards:
        return jsonify({"status": "fail", "reason": "Invalid mode"}), 400

    # Insert entry
    leaderboard = leaderboards[mode]
    leaderboard.append({"name": name, "time": time})

    # Sort by time ascending (smaller is better) and keep top 3
    leaderboard.sort(key=itemgetter("time"))
    leaderboards[mode] = leaderboard[:TOP_N]

    return jsonify({"status": "success", "leaderboard": leaderboards[mode]})


@app.route("/leaderboard/<mode>", methods=["GET"])
def get_leaderboard(mode):
    if mode not in leaderboards:
        return jsonify({"status": "fail", "reason": "Invalid mode"}), 400
    return jsonify(leaderboards[mode])


# Optional test route
@app.route("/")
def home():
    return "Leaderboard API running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)

