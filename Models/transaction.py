from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Foreign key to Player
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)

    # Foreign key to AuctionItem (the item won by the player)
    auction_item_id = db.Column(db.Integer, db.ForeignKey('auction_items.id'), nullable=False)

    def __repr__(self):
        return f"<Transaction: Player {self.player_id} paid {self.amount} for {self.auction_item_id}>"
