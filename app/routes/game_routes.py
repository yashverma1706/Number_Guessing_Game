from datetime import datetime

from flask import Blueprint, jsonify, request

from app import db
from app.models import Game, GamePlayer, Guess, Player

from app.services.game_service import GameService
from app.game.two_player import TwoPlayerGame


game_bp = Blueprint(
    "game",
    __name__,
    url_prefix="/api/games"
)

game_service = GameService()


@game_bp.route("/", methods=["POST"])
def create_game():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required."
        }), 400

    try:
        game_id, game = game_service.create_game(
            mode=data.get("mode"),
            player1_id=data.get("player1_id"),
            player2_id=data.get("player2_id"),
            range_min=data.get("range_min", 1),
            range_max=data.get("range_max", 100),
            secret_number=data.get("secret_number")
        )

        return jsonify({
            "message": "Game created successfully.",
            "game_id": game_id,
            "mode": data.get("mode"),
            "range": {
                "min": game.range_min,
                "max": game.range_max
            }
        }), 201

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 400


@game_bp.route("/<int:game_id>", methods=["GET"])
def get_game(game_id):

    game = game_service.get_game(game_id)

    if game is None:
        return jsonify({
            "error": "Game not found."
        }), 404

    response = {
        "game_id": game_id,
        "mode": game.mode,
        "status": game.status,
        "range": {
            "min": game.range_min,
            "max": game.range_max
        }
    }

    # Single Player
    if game.mode == "single_player":

        response.update({
            "player_id": game.player_id,
            "attempts": game.attempts
        })

    # Two Player - Player Chooses
    elif game.mode == "two_player":

        response.update({
            "round": game.current_round,
            "setter_id": game.get_setter()
            if game.status == "active" else None,
            "guesser_id": game.get_guesser()
            if game.status == "active" else None,
            "scores": game.scores,
            "attempts": game.attempts,
            "round_results": game.round_results
        })

        if game.status == "completed":
            response["winner"] = game.get_winner()

    # Two Player - Computer Generates
    elif game.mode == "two_player_computer":

        response.update({
            "current_player": (
                game.current_player
                if game.status == "active"
                else None
            ),
            "scores": game.scores,
            "attempts": {
                player_id: game.player_games[player_id].attempts
                for player_id in game.player_games
            },
            "finished_players": list(
                game.finished_players
            )
        })

        if game.status == "completed":
            response["winner"] = game.get_winner()

    # Player vs Computer
    elif game.mode == "player_vs_computer":

        response.update({
            "player_id": game.player_id,
            "attempts": game.attempts,
            "current_guess": game.current_guess
        })

    return jsonify(response)

@game_bp.route("/<int:game_id>/guess", methods=["POST"])
def make_guess(game_id):

    game = game_service.get_game(game_id)

    if game is None:
        return jsonify({
            "error": "Game not found."
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required."
        }), 400

    player_id = data.get("player_id")
    guess = data.get("guess")

    if player_id is None:
        return jsonify({
            "error": "Player ID is required."
        }), 400

    if guess is None:
        return jsonify({
            "error": "Guess is required."
        }), 400

    if not isinstance(guess, int):
        return jsonify({
            "error": "Guess must be an integer."
        }), 400

    try:
        # Make the guess using the game engine
        result = game.make_guess(
            player_id=player_id,
            guess=guess
        )

        # Only save valid guesses
        if result.get("result") in [
            "higher",
            "lower",
            "correct"
        ]:

            db_game = db.session.get(Game, game_id)

            if db_game is not None:

                # Find the player participating in this game
                game_player = GamePlayer.query.filter_by(
                    game_id=game_id,
                    player_id=player_id
                ).first()

                if game_player is not None:

                    # Current attempt number
                    attempt_number = game_player.attempts + 1

                    # Save guess
                    guess_record = Guess(
                        game_id=game_id,
                        player_id=player_id,
                        guess=guess,
                        result=result["result"],
                        attempt_number=attempt_number
                    )

                    db.session.add(guess_record)

                    # Update player attempts
                    game_player.attempts += 1

                    # Update game status
                    db_game.status = game.status
                    if game.status in ["won", "completed"]:
                        db_game.ended_at = datetime.utcnow()

                    # Update round
                    if hasattr(game, "current_round"):
                        db_game.current_round = game.current_round

                    # --------------------------------
                    # Update player score and status
                    # --------------------------------

                    if game.mode == "single_player":

                        base_score = 1000
                        penalty = game.attempts * 50

                        game_player.score = max(
                            base_score - penalty,
                            0
                        )

                        if game.status == "won":
                            game_player.finished = True


                    elif game.mode == "two_player":

                        # Update scores for both players
                        for player_record in GamePlayer.query.filter_by(
                            game_id=game_id
                        ).all():

                            player_record.score = game.scores[
                                player_record.player_id
                            ]

                        # Both players have finished when the game is completed
                        if game.status == "completed":

                            for player_record in GamePlayer.query.filter_by(
                                game_id=game_id
                            ).all():

                                player_record.finished = True


                    elif game.mode == "two_player_computer":

                        # Update score if this player has finished
                        game_player.score = game.scores[player_id]

                        if player_id in game.finished_players:
                            game_player.finished = True


                    # --------------------------------
                    # Set winner when game is complete
                    # --------------------------------

                    if game.status in ["won", "completed"]:

                        winner_id = None

                        if hasattr(game, "get_winner"):
                            winner = game.get_winner()

                            if isinstance(winner, int):
                                winner_id = winner

                        db_game.winner_id = winner_id


                    # Save changes
                    db.session.commit()

        return jsonify(result)

    except TypeError:
        return jsonify({
            "error": (
                "This game mode does not support "
                "this guess operation."
            )
        }), 400

@game_bp.route("/<int:game_id>/computer-guess", methods=["POST"])
def computer_guess(game_id):

    game = game_service.get_game(game_id)

    if game is None:
        return jsonify({
            "error": "Game not found."
        }), 404

    if not hasattr(game, "get_next_guess"):
        return jsonify({
            "error": "This game does not support computer guessing."
        }), 400

    guess = game.get_next_guess()

    if guess is None:

        if game.status == "invalid":
            return jsonify({
                "error": "The game has become invalid."
            }), 400

        return jsonify({
            "error": "No guess is available."
        }), 400

    # Save computer search state
    db_game = db.session.get(Game, game_id)

    if db_game is not None:

        db_game.computer_low = game.low
        db_game.computer_high = game.high
        db_game.computer_current_guess = game.current_guess
        db_game.status = game.status

        game_player = GamePlayer.query.filter_by(
            game_id=game_id,
            player_id=game.player_id
        ).first()

        if game_player is not None:
            game_player.attempts = game.attempts

        db.session.commit()

    return jsonify({
        "guess": guess,
        "attempts": game.attempts
    })

@game_bp.route("/<int:game_id>/feedback", methods=["POST"])
def computer_feedback(game_id):

    game = game_service.get_game(game_id)

    if game is None:
        return jsonify({
            "error": "Game not found."
        }), 404

    if not hasattr(game, "give_feedback"):
        return jsonify({
            "error": (
                "This game does not support "
                "computer feedback."
            )
        }), 400

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required."
        }), 400

    feedback = data.get("feedback")

    if feedback not in [
        "higher",
        "lower",
        "correct"
    ]:
        return jsonify({
            "error": (
                "Feedback must be "
                "'higher', 'lower', or 'correct'."
            )
        }), 400

    result = game.give_feedback(feedback)

    # Save updated computer state
    db_game = db.session.get(Game, game_id)

    if db_game is not None:

        db_game.computer_low = game.low
        db_game.computer_high = game.high
        db_game.computer_current_guess = game.current_guess
        db_game.status = game.status

        game_player = GamePlayer.query.filter_by(
            game_id=game_id,
            player_id=game.player_id
        ).first()

        if game_player is not None:

            game_player.attempts = game.attempts

            if game.status == "won":

                base_score = 1000
                penalty = game.attempts * 50

                game_player.score = max(
                    base_score - penalty,
                    0
                )

                game_player.finished = True

        if game.status == "won":
            db_game.winner_id = game.player_id

        db.session.commit()

    return jsonify(result)

@game_bp.route("/<int:game_id>/round", methods=["POST"])
def start_round(game_id):

    game = game_service.get_game(game_id)

    if game is None:
        return jsonify({
            "error": "Game not found."
        }), 404

    if not isinstance(game, TwoPlayerGame):
        return jsonify({
            "error": "This game does not support rounds."
        }), 400

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required."
        }), 400

    secret_number = data.get("secret_number")

    if secret_number is None:
        return jsonify({
            "error": "Secret number is required."
        }), 400

    if not isinstance(secret_number, int):
        return jsonify({
            "error": "Secret number must be an integer."
        }), 400

    try:
        # Start round in game engine
        result = game.start_round(
            secret_number=secret_number
        )

        # Save round state to database
        db_game = db.session.get(
            Game,
            game_id
        )

        if db_game is not None:

            db_game.secret_number = secret_number
            db_game.current_round = game.current_round
            db_game.status = game.status

            db.session.commit()

        return jsonify(result)

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 400

@game_bp.route("/player/<int:player_id>/history", methods=["GET"])
def get_player_history(player_id):

    player = db.session.get(Player, player_id)

    if player is None:
        return jsonify({
            "error": "Player not found."
        }), 404

    game_players = GamePlayer.query.filter_by(
        player_id=player_id
    ).order_by(
        GamePlayer.id.desc()
    ).all()

    history = []

    for game_player in game_players:

        game = db.session.get(
            Game,
            game_player.game_id
        )

        if game is None:
            continue

        result = "in_progress"

        if game.status in ["won", "completed"]:

            if game.winner_id == player_id:
                result = "win"

            elif game.winner_id is None:
                result = "draw"

            else:
                result = "loss"

        history.append({
            "game_id": game.id,
            "mode": game.mode,
            "status": game.status,
            "result": result,
            "score": game_player.score,
            "attempts": game_player.attempts,
            "started_at": (
                game.started_at.isoformat()
                if game.started_at
                else None
            ),
            "ended_at": (
                game.ended_at.isoformat()
                if game.ended_at
                else None
            )
        })

    return jsonify({
        "player_id": player_id,
        "games": history
    })

@game_bp.route("/player/<int:player_id>/stats", methods=["GET"])
def get_player_stats(player_id):

    player = db.session.get(Player, player_id)

    if player is None:
        return jsonify({
            "error": "Player not found."
        }), 404

    game_players = GamePlayer.query.filter_by(
        player_id=player_id
    ).all()

    games_played = 0
    wins = 0
    losses = 0
    draws = 0
    total_score = 0
    total_attempts = 0
    best_score = 0

    for game_player in game_players:

        game = db.session.get(
            Game,
            game_player.game_id
        )

        if game is None:
            continue

        games_played += 1

        total_score += game_player.score
        total_attempts += game_player.attempts

        if game_player.score > best_score:
            best_score = game_player.score

        if game.status in ["won", "completed"]:

            if game.winner_id == player_id:
                wins += 1

            elif game.winner_id is None:
                draws += 1

            else:
                losses += 1

    average_score = 0
    average_attempts = 0

    win_percentage = 0

    if games_played > 0:
        win_percentage = round(
            (wins / games_played) * 100,
            2
        )

    if games_played > 0:

        average_score = round(
            total_score / games_played,
            2
        )

        average_attempts = round(
            total_attempts / games_played,
            2
        )

    return jsonify({
        "player_id": player_id,
        "statistics": {
            "games_played": games_played,
            "wins": wins,
            "losses": losses,
            "draws": draws,
            "win_percentage": win_percentage,
            "total_score": total_score,
            "average_score": average_score,
            "average_attempts": average_attempts,
            "best_score": best_score
        }
    })