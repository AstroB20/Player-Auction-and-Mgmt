from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Float, default=1000.00)  # Starting balance for player
    # To represent bids made by the player
    bids = db.relationship('Bid', backref='player', lazy=True)

    def __repr__(self):
        return f"<Player {self.name}, Balance: {self.balance}>"
