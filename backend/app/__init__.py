from flask import Flask
from flask_cors import CORS
from app.database import init_db

def create_app():
    app = Flask(__name__)
    CORS(app)
    init_db()

    from app.routes import shopping_routes, voice_routes, suggestion_routes, apriori_routes, search_routes, grocery_routes
    app.register_blueprint(shopping_routes.bp)
    app.register_blueprint(voice_routes.bp)
    app.register_blueprint(suggestion_routes.bp)
    app.register_blueprint(apriori_routes.bp)
    app.register_blueprint(search_routes.bp)
    app.register_blueprint(grocery_routes.bp)

    return app