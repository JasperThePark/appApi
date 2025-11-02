from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Get Render database URL
db_url = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Define leaderboard table
class Leaderboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    mode = db.Column(db.String(50), nullable=False)
    time = db.Column(db.Float, nullable=False)
    score = db.Column(db.Integer, nullable=False)

with app.app_context():
    db.create_all()  # Create tables if not exist

@app.route("/submit", methods=["POST"])
def submit_score():
    data = request.get_json()
    new_entry = Leaderboard(
        name=data["name"],
        mode=data["mode"],
        time=data["time"],
        score=data["score"]
    )
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({"status": "success"})

@app.route("/leaderboard/<mode>")
def leaderboard(mode):
    results = Leaderboard.query.filter_by(mode=mode).order_by(Leaderboard.time.asc()).limit(10).all()
    return jsonify([
        {"name": r.name, "time": r.time, "score": r.score}
        for r in results
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
