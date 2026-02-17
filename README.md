# Voice Command Shopping Assistant

A modern voice-based shopping list manager with AI-powered smart suggestions. Add items using natural voice commands, get smart recommendations based on your purchase history, and manage your shopping list efficiently.

## Features

✨ **Voice Commands**
- Natural language processing for flexible voice input (e.g., "Add milk" or "I need apples")
- Automatic item categorization (dairy, produce, meat, snacks, beverages, pantry)
- Quantity and unit recognition (e.g., "2 bottles of water")
- Multilingual support (English, Spanish, French, German, Italian, Japanese, Chinese, Hindi)

🧠 **Smart Suggestions**
- History-based recommendations (products you frequently buy)
- Seasonal product suggestions
- Alternative product recommendations
- Real-time suggestion updates

📝 **Shopping List Management**
- Add/remove/complete items via voice or buttons
- Automatic categorization with visual organization
- Quantity tracking with units
- Clean, minimalist interface

🎯 **User Experience**
- Minimalist, mobile-optimized interface
- Real-time visual feedback
- Voice recognition status indicators
- Responsive design for all devices

## Tech Stack

**Backend:**
- Flask (Python web framework)
- Google Cloud Speech-to-Text API
- spaCy & NLTK (Natural Language Processing)
- SQLite (Local database)
- Flask-CORS (Cross-origin requests)

**Frontend:**
- React 18 (UI library)
- Vite (Build tool)
- Axios (HTTP client)
- CSS3 (Styling with gradients & animations)

**Infrastructure:**
- Docker & Docker Compose
- Google Cloud Run (Deployment)
- Cloud SQL (Production database)

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Docker (optional)
- Google Cloud account with Speech-to-Text API enabled

### Local Development

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Set up environment variables
cp .env.example .env
# Edit .env with your Google Cloud credentials path

# Run development server
python run.py
```

Server will be available at `http://localhost:5000`

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env

# Run development server
npm run dev
```

App will be available at `http://localhost:3000`

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up

# Access the application
# Frontend: http://localhost:3000
# Backend: http://localhost:5000
```

## API Documentation

### Shopping List Endpoints

```
GET    /api/shopping/list              - Get all items
POST   /api/shopping/add               - Add new item
DELETE /api/shopping/<id>              - Remove item
PUT    /api/shopping/<id>/complete     - Mark as purchased
```

**Add Item:**
```json
{
  "item_name": "Milk",
  "category": "dairy",
  "quantity": 2,
  "unit": "bottles"
}
```

### Voice Processing Endpoints

```
POST   /api/voice/process              - Process voice command
POST   /api/voice/transcribe           - Transcribe audio file
GET    /api/voice/languages            - Get supported languages
```

### Suggestions Endpoints

```
GET    /api/suggestions/               - Get smart suggestions
GET    /api/suggestions/history        - Get purchase history
```

## Environment Variables

**Backend (.env):**
```
FLASK_ENV=development
GOOGLE_CLOUD_CREDENTIALS=/path/to/credentials.json
DATABASE=shopping_assistant.db
```

**Frontend (.env):**
```
VITE_API_URL=http://localhost:5000
```

## Project Structure

```
voice-shopping-assistant/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── nlp_processor.py
│   │   ├── voice_processor.py
│   │   ├── suggestions.py
│   │   └── routes/
│   │       ├── shopping_routes.py
│   │       ├── voice_routes.py
│   │       └── suggestion_routes.py
│   ├── tests/
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── VoiceInput.jsx
│   │   │   ├── ShoppingList.jsx
│   │   │   └── Suggestions.jsx
│   │   ├── api.js
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── docker-compose.yml
├── README.md
└── APPROACH.md
```

## Error Handling

The application includes comprehensive error handling:
- Graceful fallback for voice recognition failures
- User-friendly error messages
- Automatic retry mechanisms
- Validation of all user inputs
- Database transaction rollback on errors

## Performance Considerations

- Frontend uses React hooks for efficient state management
- API responses include loading states
- Database queries are optimized with indexing
- Voice processing runs asynchronously to prevent UI blocking
- Suggestions are cached and updated on demand

## Limitations & Future Enhancements

**Current Limitations:**
- Requires microphone access (browser permission)
- Offline mode not yet implemented
- Single-user session (no user accounts)

**Future Enhancements:**
- User authentication and cloud sync
- Offline data persistence with IndexedDB
- Price comparison across stores
- Dietary restriction filters
- Barcode scanning
- Recipe-based shopping lists
- Smart purchase predictions

## Testing

Run tests:
```bash
cd backend
pytest tests/
```

## Deployment to Google Cloud

### Setup

```bash
# Authenticate with Google Cloud
gcloud auth login

# Create a Google Cloud project
gcloud projects create voice-shopping-assistant

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable speech.googleapis.com
```

### Deploy Backend

```bash
cd backend
gcloud run deploy voice-shopping-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Deploy Frontend

```bash
cd frontend
npm run build

gcloud storage buckets create gs://voice-shopping-frontend

gsutil -m cp -r dist/* gs://voice-shopping-frontend/

gcloud compute backend-buckets create voice-shopping-backend \
  --gcs-bucket-name=voice-shopping-frontend
```

## Security Considerations

- All API endpoints validate input data
- CORS is properly configured
- Environment variables for sensitive credentials
- No hardcoded secrets in code
- SQL injection prevention through parameterized queries

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues and feature requests, please open an issue on GitHub.

---

**Created:** February 2026
**Version:** 1.0.0
