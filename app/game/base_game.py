import random


class BaseGame:

    def __init__(
        self,
        range_min=1,
        range_max=100,
        secret_number=None
    ):
        if range_min >= range_max:
            raise ValueError(
                "Minimum must be less than maximum."
            )

        self.range_min = range_min
        self.range_max = range_max

        if secret_number is None:
            self.secret_number = random.randint(
                range_min,
                range_max
            )
        else:
            if not isinstance(secret_number, int):
                raise ValueError(
                    "Secret number must be an integer."
                )

            if not range_min <= secret_number <= range_max:
                raise ValueError(
                    f"Secret number must be between "
                    f"{range_min} and {range_max}."
                )

            self.secret_number = secret_number

        self.attempts = 0
        self.status = "active"

    def make_guess(self, guess):

        if self.status != "active":
            return {
                "result": "game_over",
                "message": "The game is already over."
            }

        if not isinstance(guess, int):
            return {
                "result": "invalid",
                "message": "Guess must be an integer."
            }

        if guess < self.range_min or guess > self.range_max:
            return {
                "result": "invalid",
                "message": (
                    f"Guess must be between "
                    f"{self.range_min} and "
                    f"{self.range_max}."
                )
            }

        self.attempts += 1

        if guess < self.secret_number:
            return {
                "result": "higher",
                "message": "Try a higher number.",
                "attempts": self.attempts
            }

        if guess > self.secret_number:
            return {
                "result": "lower",
                "message": "Try a lower number.",
                "attempts": self.attempts
            }

        self.status = "won"

        return {
            "result": "correct",
            "message": "Correct! 🎉",
            "attempts": self.attempts
        }