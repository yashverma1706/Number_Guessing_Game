class PlayerVsComputerGame:

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

        if secret_number is None:
            raise ValueError(
                "A secret number is required."
            )

        if not isinstance(secret_number, int):
            raise ValueError(
                "Secret number must be an integer."
            )

        if not range_min <= secret_number <= range_max:
            raise ValueError(
                f"Secret number must be between "
                f"{range_min} and {range_max}."
            )

        self.range_min = range_min
        self.range_max = range_max

        # TEST/ENGINE ONLY.
        # The real API will keep this on the backend.
        self.secret_number = secret_number

        self.low = range_min
        self.high = range_max

        self.attempts = 0
        self.status = "active"

        self.current_guess = None

    def get_next_guess(self):

        if self.status != "active":
            return None

        if self.low > self.high:
            self.status = "invalid"
            return None

        self.current_guess = (self.low + self.high) // 2

        self.attempts += 1

        return self.current_guess

    def give_feedback(self, feedback):

        if self.status != "active":
            return {
                "result": "game_over",
                "message": "The game is already over."
            }

        if self.current_guess is None:
            return {
                "result": "invalid",
                "message": "Computer has not made a guess yet."
            }

        if feedback not in ["higher", "lower", "correct"]:
            return {
                "result": "invalid",
                "message": (
                    "Feedback must be "
                    "'higher', 'lower', or 'correct'."
                )
            }

        if feedback == "correct":

            self.status = "won"

            return {
                "result": "correct",
                "message": "Computer guessed correctly! 🤖",
                "attempts": self.attempts
            }

        if feedback == "higher":

            self.low = self.current_guess + 1

        elif feedback == "lower":

            self.high = self.current_guess - 1

        if self.low > self.high:

            self.status = "invalid"

            return {
                "result": "invalid",
                "message": "The feedback was inconsistent."
            }

        return {
            "result": feedback,
            "message": (
                "Computer will make another guess."
            ),
            "next_range": {
                "min": self.low,
                "max": self.high
            },
            "attempts": self.attempts
        }