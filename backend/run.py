import os
from app import create_app
from app.config import config

def create_application():
    """Create and configure the Flask application"""
    env = os.getenv('FLASK_ENV', 'development')
    app = create_app()
    app.config.from_object(config[env])
    return app

if __name__ == '__main__':
    app = create_application()
    app.run(debug=True, host='0.0.0.0', port=5000)
