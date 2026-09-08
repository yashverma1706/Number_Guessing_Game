from app import db
from app.models import Player, Game, GamePlayer, Guess

from app.game.base_game import BaseGame
from app.game.single_player import SinglePlayerGame
from app.game.two_player import TwoPlayerGame
from app.game.two_player_computer import TwoPlayerComputerGame
from app.game.player_vs_computer import PlayerVsComputerGame


class GameService:

    def __init__(self):
        self.active_games = {}

    def create_game(
        self,
        mode,
        player1_id,
        player2_id=None,
        range_min=1,
        range_max=100,
        secret_number=None
    ):
        if player1_id is None:
            raise ValueError("Player 1 is required.")

        if range_min >= range_max:
            raise ValueError(
                "Minimum must be less than maximum."
            )

        player1 = db.session.get(Player, player1_id)

        if player1 is None:
            raise ValueError(
                "Player 1 does not exist."
            )

        player2 = None

        if mode in ["two_player", "two_player_computer"]:

            if player2_id is None:
                raise ValueError(
                    "Player 2 is required for two-player mode."
                )

            player2 = db.session.get(Player, player2_id)

            if player2 is None:
                raise ValueError(
                    "Player 2 does not exist."
                )

            if player1_id == player2_id:
                raise ValueError(
                    "Player 1 and Player 2 must be different."
                )

        # Create game engine

        if mode == "single_player":

            game = SinglePlayerGame(
                range_min=range_min,
                range_max=range_max
            )

            game.set_player(player1_id)

            number_source = "computer"

        elif mode == "two_player":

            game = TwoPlayerGame(
                player1_id=player1_id,
                player2_id=player2_id,
                range_min=range_min,
                range_max=range_max
            )

            number_source = "player"

        elif mode == "two_player_computer":

            game = TwoPlayerComputerGame(
                player1_id=player1_id,
                player2_id=player2_id,
                range_min=range_min,
                range_max=range_max
            )

            number_source = "computer"

        elif mode == "player_vs_computer":

            if secret_number is None:
                raise ValueError(
                    "Secret number is required."
                )

            game = PlayerVsComputerGame(
                range_min=range_min,
                range_max=range_max,
                secret_number=secret_number
            )

            game.player_id = player1_id

            number_source = "player"

        else:
            raise ValueError(
                f"Invalid game mode: {mode}"
            )

        game.mode = mode

        # Create database Game record

        db_game = Game(
            mode=mode,
            number_source=number_source,
            range_min=range_min,
            range_max=range_max,
            status="active",
            secret_number=(
                game.secret_number
                if mode != "two_player"
                else None
            ),
            current_round=(
                game.current_round
                if mode == "two_player"
                else 1
            )
        )

        db.session.add(db_game)
        db.session.flush()

        # Create Player 1 record

        game_player1 = GamePlayer(
            game_id=db_game.id,
            player_id=player1_id,
            role="player1"
        )

        db.session.add(game_player1)

        # Create Player 2 record

        if player2_id is not None:

            game_player2 = GamePlayer(
                game_id=db_game.id,
                player_id=player2_id,
                role="player2"
            )

            db.session.add(game_player2)

        db.session.commit()

        game_id = db_game.id

        self.active_games[game_id] = game

        return game_id, game

    def get_game(self, game_id):

        # First check memory
        game = self.active_games.get(game_id)

        if game is not None:
            return game

        # If not in memory, load from database
        db_game = db.session.get(Game, game_id)

        if db_game is None:
            return None

        game_players = GamePlayer.query.filter_by(
            game_id=game_id
        ).all()

        if not game_players:
            return None

        player1_id = game_players[0].player_id

        player2_id = None

        if len(game_players) > 1:
            player2_id = game_players[1].player_id

        # Single Player

        if db_game.mode == "single_player":

            game = SinglePlayerGame(
                range_min=db_game.range_min,
                range_max=db_game.range_max
            )

            game.secret_number = db_game.secret_number
            game.set_player(player1_id)

            game_player = game_players[0]

            game.attempts = game_player.attempts
            game.status = db_game.status

        # Two Player

        elif db_game.mode == "two_player":

            if player2_id is None:
                return None

            game = TwoPlayerGame(
                player1_id=player1_id,
                player2_id=player2_id,
                range_min=db_game.range_min,
                range_max=db_game.range_max
            )

            game.current_round = db_game.current_round
            game.status = db_game.status

            for game_player in game_players:

                game.scores[
                    game_player.player_id
                ] = game_player.score

                game.attempts[
                    game_player.player_id
                ] = game_player.attempts

            # Restore current round game

            if (
                db_game.status == "active"
                and db_game.secret_number is not None
            ):

                current_guesser = game.get_guesser()

                game.round_game = BaseGame(
                    range_min=db_game.range_min,
                    range_max=db_game.range_max,
                    secret_number=db_game.secret_number
                )

                current_guesser_record = next(
                    (
                        p for p in game_players
                        if p.player_id == current_guesser
                    ),
                    None
                )

                if current_guesser_record is not None:
                    game.round_game.attempts = 0

            # Restore round 1 result

            if db_game.current_round == 2:

                player2_record = next(
                    (
                        p for p in game_players
                        if p.player_id == player2_id
                    ),
                    None
                )

                if player2_record is not None:

                    game.round_results.append({
                        "round": 1,
                        "setter_id": player1_id,
                        "guesser_id": player2_id,
                        "attempts": player2_record.attempts,
                        "score": player2_record.score
                    })

        # Two Player Computer

        elif db_game.mode == "two_player_computer":

            if player2_id is None:
                return None

            game = TwoPlayerComputerGame(
                player1_id=player1_id,
                player2_id=player2_id,
                range_min=db_game.range_min,
                range_max=db_game.range_max
            )

            game.secret_number = db_game.secret_number
            game.status = db_game.status

            for game_player in game_players:

                player_id = game_player.player_id

                game.player_games[
                    player_id
                ].attempts = game_player.attempts

                game.scores[
                    player_id
                ] = game_player.score

                if game_player.finished:
                    game.finished_players.add(player_id)

            if db_game.status == "active":

                guesses = Guess.query.filter_by(
                    game_id=game_id
                ).order_by(
                    Guess.id.desc()
                ).all()

                if guesses:

                    last_player = guesses[0].player_id

                    if last_player == player1_id:
                        game.current_player = player2_id
                    else:
                        game.current_player = player1_id

                else:
                    game.current_player = player1_id

                if game.current_player in game.finished_players:
                    game.switch_to_remaining_player()

        # Player vs Computer

        elif db_game.mode == "player_vs_computer":

            game = PlayerVsComputerGame(
                range_min=db_game.range_min,
                range_max=db_game.range_max,
                secret_number=db_game.secret_number
            )

            game.player_id = player1_id
            game.status = db_game.status

            game_player = game_players[0]

            game.attempts = game_player.attempts

            # Restore binary-search state
            if db_game.computer_low is not None:
                game.low = db_game.computer_low

            if db_game.computer_high is not None:
                game.high = db_game.computer_high

            if db_game.computer_current_guess is not None:
                game.current_guess = db_game.computer_current_guess

        else:
            return None

        game.mode = db_game.mode

        # Put reconstructed game back into memory

        self.active_games[game_id] = game

        return game

    def remove_game(self, game_id):

        return self.active_games.pop(game_id, None)