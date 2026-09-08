from app import db


class GamePlayer(db.Model):
    __tablename__ = "game_players"

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

    role = db.Column(
        db.String(30),
        nullable=False
    )

    score = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    attempts = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    finished = db.Column(
    db.Boolean,
    default=False,
    nullable=False
    )

    game = db.relationship(
        "Game",
        back_populates="game_players"
    )

    player = db.relationship(
        "Player",
        back_populates="game_players"
    )

    def __repr__(self):
        return f"<GamePlayer {self.player_id} - Game {self.game_id}>"