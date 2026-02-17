import os
from flask_cors import CORS  # <--- ADD THIS LINE
from app import create_app
from app.config import config

# 1. Create the application instance at the top level
env = os.getenv('FLASK_ENV', 'development')
app = create_app()
app.config.from_object(config[env])

CORS(app)  # <--- ADD THIS LINE (Allows your frontend to talk to this API)

if __name__ == '__main__':
    # 2. Use Render's dynamic port, or 5000 for local testing
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
