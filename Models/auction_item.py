from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class AuctionItem(db.Model):
    __tablename__ = 'auction_items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    starting_price = db.Column(db.Float, nullable=False)

    # Relationship with Bid (an item can have multiple bids)
    bids = db.relationship('Bid', backref='auction_item', lazy=True)

    def __repr__(self):
        return f"<AuctionItem {self.name}, Starting Price: {self.starting_price}>"
