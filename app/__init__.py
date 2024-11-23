from flask import Flask
from app.utils.db import db
import logging

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie_app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Import routes
    from app.routes.api_routes import api_bp
    from app.routes.user_routes import user_bp
    from app.routes.watchlist_routes import watchlist_bp

    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(watchlist_bp, url_prefix='/watchlist')

    logging.basicConfig(level=logging.INFO)
    app.logger.info('Application startup')

    return app
