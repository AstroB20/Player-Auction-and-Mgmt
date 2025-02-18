from flask import Flask
from app.database import db
from app.routes import auction_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Tiger@localhost/auction_system'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(auction_bp)

    with app.app_context():
        db.create_all()

    return app
