from .base_game import BaseGame


class TwoPlayerComputerGame:

    def __init__(
        self,
        player1_id,
        player2_id,
        range_min=1,
        range_max=100
    ):
        self.player1_id = player1_id
        self.player2_id = player2_id

        self.range_min = range_min
        self.range_max = range_max

        # Generate ONE secret number
        self.secret_number = BaseGame(
            range_min,
            range_max
        ).secret_number

        # Each player gets an independent game state
        self.player_games = {
            player1_id: BaseGame(
                range_min,
                range_max,
                secret_number=self.secret_number
            ),
            player2_id: BaseGame(
                range_min,
                range_max,
                secret_number=self.secret_number
            )
        }

        self.current_player = player1_id

        self.scores = {
            player1_id: 0,
            player2_id: 0
        }

        self.finished_players = set()

        self.status = "active"

    def get_current_player(self):
        return self.current_player

    def make_guess(self, player_id, guess):

        if self.status != "active":
            return {
                "result": "game_over",
                "message": "The game is already over."
            }

        if player_id != self.current_player:
            return {
                "result": "not_your_turn",
                "message": "It is not your turn."
            }

        if player_id in self.finished_players:
            return {
                "result": "already_finished",
                "message": "You have already finished."
            }

        player_game = self.player_games[player_id]

        result = player_game.make_guess(guess)

        # Player guessed correctly
        if result["result"] == "correct":

            self.finished_players.add(player_id)

            self.scores[player_id] = self.calculate_score(
                player_game.attempts
            )

            # Both players have finished
            if len(self.finished_players) == 2:

                self.status = "completed"

                return {
                    **result,
                    "game_status": "completed",
                    "scores": self.scores,
                    "winner": self.get_winner()
                }

            # Only this player has finished
            self.switch_to_remaining_player()

            return {
                **result,
                "game_status": "waiting_for_other_player",
                "next_player": self.current_player,
                "scores": self.scores
            }

        # Wrong guess
        self.switch_player()

        return {
            **result,
            "next_player": self.current_player
        }

    def switch_player(self):

        if self.current_player == self.player1_id:
            self.current_player = self.player2_id
        else:
            self.current_player = self.player1_id

        # Skip finished players
        if self.current_player in self.finished_players:
            self.switch_player()

    def switch_to_remaining_player(self):

        if self.player1_id in self.finished_players:
            self.current_player = self.player2_id
        else:
            self.current_player = self.player1_id

    def calculate_score(self, attempts):

        base_score = 1000
        penalty = attempts * 50

        return max(base_score - penalty, 0)

    def get_winner(self):

        if self.status != "completed":
            return None

        player1_score = self.scores[self.player1_id]
        player2_score = self.scores[self.player2_id]

        if player1_score > player2_score:
            return self.player1_id

        if player2_score > player1_score:
            return self.player2_id

        return "draw"