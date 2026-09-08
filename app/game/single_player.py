from .base_game import BaseGame


class SinglePlayerGame(BaseGame):

    def __init__(self, range_min=1, range_max=100):

        super().__init__(
            range_min=range_min,
            range_max=range_max
        )

        self.mode = "single_player"
        self.player_id = None

    def set_player(self, player_id):

        self.player_id = player_id

    def make_guess(self, player_id, guess):

        if player_id != self.player_id:

            return {
                "result": "not_your_game",
                "message": "This game belongs to another player."
            }

        return super().make_guess(guess)