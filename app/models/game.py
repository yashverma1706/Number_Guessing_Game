from app import db


class Game(db.Model):
    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True)

    mode = db.Column(db.String(50), nullable=False)

    number_source = db.Column(db.String(20), nullable=False)

    range_min = db.Column(
        db.Integer, 
        nullable=False
    )

    range_max = db.Column(
        db.Integer, 
        nullable=False
    )

    secret_number = db.Column(
        db.Integer,
        nullable=True
    )

    current_round = db.Column(
        db.Integer,
        default=1,
        nullable=False
    )

    computer_low = db.Column(
    db.Integer,
    nullable=True
    )

    computer_high = db.Column(
        db.Integer,
        nullable=True
    )

    computer_current_guess = db.Column(
        db.Integer,
        nullable=True
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="active"
    )

    winner_id = db.Column(
        db.Integer,
        db.ForeignKey("players.id"),
        nullable=True
    )

    started_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    ended_at = db.Column(
        db.DateTime,
        nullable=True
    )

    game_players = db.relationship(
        "GamePlayer",
        back_populates="game",
        cascade="all, delete-orphan"
    )

    guesses = db.relationship(
        "Guess",
        back_populates="game",
        cascade="all, delete-orphan"
    )

    winner = db.relationship(
        "Player",
        foreign_keys=[winner_id]
    )

    def __repr__(self):
        return f"<Game {self.id} - {self.mode}>"