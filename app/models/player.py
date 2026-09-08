from app import db


class Player(db.Model):
    __tablename__ = "players"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    game_players = db.relationship(
        "GamePlayer",
        back_populates="player",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Player {self.username}>"