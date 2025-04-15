from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
from models import db, Guest, Episode, Appearance

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return {"message": "Server is running"}

# GET /episodes
@app.route("/episodes", methods=["GET"])
def get_episodes():
    episodes = Episode.query.all()
    return jsonify([{
        "id": e.id,
        "date": e.date,
        "number": e.number
    } for e in episodes]), 200

# GET /episodes/<id>
@app.route("/episodes/<int:id>", methods=["GET"])
def get_episode(id):
    episode = Episode.query.get(id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404

    return jsonify({
        "id": episode.id,
        "date": episode.date,
        "number": episode.number,
        "appearances": [
            {
                "id": a.id,
                "rating": a.rating,
                "guest_id": a.guest.id,
                "episode_id": a.episode.id,
                "guest": {
                    "id": a.guest.id,
                    "name": a.guest.name,
                    "occupation": a.guest.occupation
                }
            } for a in episode.appearances
        ]
    }), 200

# GET /guests
@app.route("/guests", methods=["GET"])
def get_guests():
    guests = Guest.query.all()
    return jsonify([{
        "id": g.id,
        "name": g.name,
        "occupation": g.occupation
    } for g in guests]), 200

# POST /appearances
@app.route("/appearances", methods=["POST"])
def create_appearance():
    data = request.get_json()

    rating = data.get("rating")
    episode_id = data.get("episode_id")
    guest_id = data.get("guest_id")

    # Validate existence of episode and guest
    episode = Episode.query.get(episode_id)
    guest = Guest.query.get(guest_id)

    if not episode or not guest:
        return jsonify({"errors": ["Guest or Episode not found"]}), 404

    try:
        new_appearance = Appearance(
            rating=rating,
            episode_id=episode_id,
            guest_id=guest_id
        )

        db.session.add(new_appearance)
        db.session.commit()

        return jsonify({
            "id": new_appearance.id,
            "rating": new_appearance.rating,
            "guest_id": new_appearance.guest.id,
            "episode_id": new_appearance.episode.id,
            "episode": {
                "id": new_appearance.episode.id,
                "date": new_appearance.episode.date,
                "number": new_appearance.episode.number
            },
            "guest": {
                "id": new_appearance.guest.id,
                "name": new_appearance.guest.name,
                "occupation": new_appearance.guest.occupation
            }
        }), 201

    except (ValueError, IntegrityError):
        db.session.rollback()
        return jsonify({"errors": ["validation errors"]}), 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)