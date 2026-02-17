# Voice Command Shopping Assistant

************************************************************************************************************
DEPLOYMENT LINK :  https://finaldaffodil.vercel.app/
************************************************************************************************************

The Voice Command Shopping Assistant is a full-stack web application designed to simplify shopping list management using voice-based interactions and smart recommendations. The frontend is built with React and Vite, providing a responsive and mobile-optimized user interface with real-time feedback for voice input, item updates, and suggestion display. Voice commands are captured in the browser and sent to the backend through REST APIs.

The backend is developed using Flask and deployed on Render. It handles voice command processing, natural language understanding, and shopping list operations. spaCy and NLTK are used to extract item names, quantities, units, and categories from natural language input. The processed data is stored in a database, enabling persistent list management and history tracking.

A recommendation module analyzes past shopping behavior to generate smart suggestions such as frequently purchased items and relevant alternatives. The frontend communicates with the backend using Axios, ensuring smooth data flow and separation of concerns. The application follows a modular architecture, making it easy to maintain, scale, and extend with future features like user authentication and personalized recommendations.

#How does this app work 
- On the top click "Try to speak". Speak anything you want like grab an apple or add apple or delete apple anything it will ask to confirm and will directly add to the "Shopping list" section. If you want to say Add 12 bananas it will add 12 Bananas directly in Shopping List.
- Below it there is Type what you want to add and delete: write manually and click on "GO" it will directly add to the shopping list.
- There is increment(+) and decrement(-) to increase or decrease the quantity of the item.
- There is also a Search option in Shopping List section.
- In "Add Grocery Item with Price" section you can add your item with different fields like name, price,category etc and it will add to the database.
- Now this saved dataset in database is used in "Filter by Price" section. Try search Min = 0 and Max = 10 and choosing the brand also and click "FILTER". It will give the filtered result.
- You can directly add the filtered ones in the Shopping List by clicking "Add to cart".
- There is a Smart Suggestion section which will give suggestion according to weather and according to shopping list. This is built by using Apriori Algorithm.
- If you want to add from Smart Suggestions you can click "+Add" button it will add directly in Shopping List 

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
USED APRIORI ALGORITHM

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

# Run development server
python run.py
```

Server will be available at `http://localhost:5000`

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install


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



## Testing

Run tests:
```bash
cd backend
pytest tests/
```


### Deploy Backend
ON RENDER 

### Deploy Frontend
ON VERSEL

## Security Considerations

- All API endpoints validate input data
- CORS is properly configured
- Environment variables for sensitive credentials
- No hardcoded secrets in code
- SQL injection prevention through parameterized queries


## License

MIT License - See LICENSE file for details

## Support

For issues and feature requests, please open an issue on GitHub.

---

**Created:** February 2026
**Version:** 1.0.0
