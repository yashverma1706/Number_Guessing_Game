from .base_game import BaseGame


class TwoPlayerGame:

    def __init__(self, player1_id, player2_id, range_min=1, range_max=100):
        self.player1_id = player1_id
        self.player2_id = player2_id

        self.range_min = range_min
        self.range_max = range_max

        self.current_round = 1
        self.status = "active"

        self.round_game = None

        self.scores = {
            player1_id: 0,
            player2_id: 0
        }

        self.attempts = {
            player1_id: 0,
            player2_id: 0
        }

        self.round_results = []

    def start_round(self, secret_number):

        if self.current_round > 2:
            raise ValueError("Both rounds are already completed.")

        setter = self.get_setter()
        guesser = self.get_guesser()

        self.round_game = BaseGame(
            range_min=self.range_min,
            range_max=self.range_max,
            secret_number=secret_number
        )

        return {
            "round": self.current_round,
            "setter_id": setter,
            "guesser_id": guesser,
            "status": "active"
        }

    def make_guess(self, player_id, guess):

        if self.status != "active":
            return {
                "result": "game_over",
                "message": "The game is already over."
            }

        guesser = self.get_guesser()

        if player_id != guesser:
            return {
                "result": "not_your_turn",
                "message": "It is not your turn to guess."
            }

        result = self.round_game.make_guess(guess)

        if "attempts" in result:
            self.attempts[player_id] += 1

        if result["result"] == "correct":
            self.finish_round()

        return result

    def get_setter(self):

        if self.current_round == 1:
            return self.player1_id

        return self.player2_id

    def get_guesser(self):

        if self.current_round == 1:
            return self.player2_id

        return self.player1_id

    def finish_round(self):

        guesser = self.get_guesser()

        attempts = self.round_game.attempts

        self.scores[guesser] = self.calculate_round_score(
            attempts
        )

        self.round_results.append({
            "round": self.current_round,
            "setter_id": self.get_setter(),
            "guesser_id": guesser,
            "attempts": attempts,
            "score": self.scores[guesser]
        })

        if self.current_round == 1:
            self.current_round = 2
            self.round_game = None
        else:
            self.status = "completed"

    def calculate_round_score(self, attempts):

        base_score = 1000
        penalty = attempts * 50

        return max(base_score - penalty, 0)

    def get_winner(self):

        if self.status != "completed":
            return None

        if self.scores[self.player1_id] > self.scores[self.player2_id]:
            return self.player1_id

        if self.scores[self.player2_id] > self.scores[self.player1_id]:
            return self.player2_id

        return "draw"