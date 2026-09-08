from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    os.makedirs(app.instance_path, exist_ok=True)

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "sqlite:///" + os.path.join(app.instance_path, "game.db")
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from app.routes.game_routes import game_bp
    app.register_blueprint(game_bp)

    from app.routes.page_routes import page_bp
    app.register_blueprint(page_bp)

    from app.models import Player
    with app.app_context():
        db.create_all()


    @app.route("/api/players", methods=["POST"])
    def create_player():
        data = request.get_json()

        username = data.get("username")

        if not username:
            return jsonify({
                "error": "Username is required"
            }), 400

        existing_player = Player.query.filter_by(
            username=username
        ).first()

        if existing_player:
            return jsonify({
                "error": "Username already exists"
            }), 409

        player = Player(username=username)

        db.session.add(player)
        db.session.commit()

        return jsonify({
            "message": "Player created successfully",
            "player": {
                "id": player.id,
                "username": player.username,
                "created_at": player.created_at.isoformat()
            }
        }), 201

    @app.route("/api/players", methods=["GET"])
    def get_players():
        players = Player.query.all()

        return jsonify([
            {
                "id": player.id,
                "username": player.username,
                "created_at": player.created_at.isoformat()
            }
            for player in players
        ])

    return app