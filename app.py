from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auction_system.db'  # Example using SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Import models to register them with SQLAlchemy
from Models.player import Player
from Models.bid import Bid
from Models.auction_item import AuctionItem
from Models.transaction import Transaction

if __name__ == '__main__':
    app.run(debug=True)
