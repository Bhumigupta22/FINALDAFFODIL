import os
from app import create_app
from app.config import config

# 1. Create the application instance at the top level (REQUIRED for Render/Gunicorn)
env = os.getenv('FLASK_ENV', 'development')
app = create_app()
app.config.from_object(config[env])

if __name__ == '__main__':
    # 2. Use Render's dynamic port, or 5000 for local testing
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)