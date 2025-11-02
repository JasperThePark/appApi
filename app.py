from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ----------------------------
# DATABASE CONFIG
# ----------------------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///leaderboard.db"  # local database file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ----------------------------
# DATABASE MODEL
# ----------------------------
class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "score": self.score}

# ----------------------------
# ROUTES
# ----------------------------

@app.route("/")
def home():
    return jsonify({"message": "Backend running successfully!"})

@app.route("/leaderboard", methods=["GET"])
def get_leaderboard():
    scores = Score.query.order_by(Score.score.desc()).limit(10).all()
    return jsonify([s.to_dict() for s in scores])

@app.route("/submit", methods=["POST"])
def submit_score():
    data = request.get_json()
    name = data.get("name")
    score = data.get("score")

    if not name or score is None:
        return jsonify({"error": "Invalid input"}), 400

    new_score = Score(name=name, score=score)
    db.session.add(new_score)
    db.se
