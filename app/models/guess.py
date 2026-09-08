from app import db


class Guess(db.Model):
    __tablename__ = "guesses"

    id = db.Column(db.Integer, primary_key=True)

    game_id = db.Column(
        db.Integer,
        db.ForeignKey("games.id"),
        nullable=False
    )

    player_id = db.Column(
        db.Integer,
        db.ForeignKey("players.id"),
        nullable=False
    )

    guess = db.Column(
        db.Integer,
        nullable=False
    )

    result = db.Column(
        db.String(20),
        nullable=False
    )

    attempt_number = db.Column(
        db.Integer,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    game = db.relationship(
        "Game",
        back_populates="guesses"
    )

    player = db.relationship(
        "Player"
    )

    def __repr__(self):
        return f"<Guess {self.guess} - {self.result}>"