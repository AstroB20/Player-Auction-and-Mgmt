from app.database import db

class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    base_price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='Available')
    sold_to = db.Column(db.String(50))
    sold_price = db.Column(db.Integer)
