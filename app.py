from flask import Flask, request, jsonify

app = Flask(__name__)

leaderboard = []

@app.route("/submit", methods=["POST"])
def submit_score():
    data = request.get_json()
    name = data.get("name")
    time = data.get("time")
    if name and isinstance(time, (int, float)):
        leaderboard.append({"name": name, "time": time})
        leaderboard.sort(key=lambda x: x["time"])
        leaderboard[:] = leaderboard[:3]  # keep top 3
    return jsonify(leaderboard)

@app.route("/leaderboard", methods=["GET"])
def get_leaderboard():
    return jsonify(leaderboard)

if __name__ == "__main__":
    app.run(debug=True)
