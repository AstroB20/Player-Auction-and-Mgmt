from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Bid(db.Model):
    __tablename__ = 'bids'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Foreign key to Player
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)

    # Foreign key to AuctionItem (you may need to create this model separately)
    auction_item_id = db.Column(db.Integer, db.ForeignKey('auction_items.id'), nullable=False)

    def __repr__(self):
        return f"<Bid by Player {self.player_id} for {self.amount}>"
