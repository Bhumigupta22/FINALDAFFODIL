## New Features: Item Search & Price Range Filtering

### ✨ Features Added

#### 1. **Item Search by Voice**
Users can now search for specific items using voice commands with detailed filters:

**Example Voice Commands:**
- "Find me organic apples"
- "Search for toothpaste"
- "Look for large milk"
- "Find organic bread"

**What gets extracted:**
- Item name (e.g., "apples")
- Brand (e.g., "organic")  
- Size (e.g., "large")
- Category (automatic detection)

#### 2. **Price Range Filtering**
Voice-based filtering to specify price ranges and brands:

**Example Voice Commands:**
- "Find toothpaste under $5"
- "Apples below $3"
- "Find budget apples"
- "Show me items under $10"

**What gets extracted:**
- Minimum price
- Maximum price
- Brand preferences (organic, budget, premium)

### 🔧 Backend Changes

#### New Files Created:
- `app/routes/search_routes.py` - New search and filter endpoints
- `scripts/populate_grocery_items.py` - Script to populate sample products

#### Files Modified:
- `app/nlp_processor.py` - Enhanced NLP to extract prices, brands, and sizes
- `app/database.py` - Added search and filter functions
- `app/routes/voice_routes.py` - Enhanced to return search results
- `app/__init__.py` - Registered new search routes

#### Database Schema Updates:
- Added `brand` and `size` columns to `shopping_list` table
- Created new `grocery_items` table for product database with:
  - `item_name` - Product name
  - `category` - Product category
  - `brand` - Brand/type (organic, budget, premium)
  - `size` - Size classification
  - `price` - Product price
  - `description` - Product description

### 🎨 Frontend Changes

#### New Files Created:
- `components/SearchResults.jsx` - Component to display search results
- `styles/SearchResults.css` - Styling for search results

#### Files Modified:
- `src/api.js` - Added searchAPI with endpoints for search and filtering
- `src/App.jsx` - Integrated search results display

### 📋 API Endpoints

#### New Search Routes (`/api/search/`)

1. **POST `/search/items`** - Search items with filters
   ```json
   {
     "text": "Find organic apples"
   }
   ```
   Response includes search results with prices and details

2. **POST `/search/by-price`** - Filter items by price range
   ```json
   {
     "text": "Find items under $5"
   }
   ```

3. **POST `/search/voice`** - Voice-enabled item search
   ```json
   {
     "text": "Search for organic milk"
   }
   ```

### 🚀 How to Use

#### 1. Populate Sample Data
Run the data population script to add sample products:
```bash
cd backend
python -c "from scripts.populate_grocery_items import populate_grocery_items; populate_grocery_items()"
```

#### 2. Using Search via Voice
**In the app UI:**
1. Tap the microphone button
2. Say: "Find me organic apples" or "Show toothpaste under $5"
3. The app will extract filters and display matching products
4. Click "Add to Cart" to add items to your shopping list

#### 3. Direct API Usage
```bash
# Search for items
curl -X POST http://localhost:5000/api/search/items \
  -H "Content-Type: application/json" \
  -d '{"text": "Find organic apples"}'

# Filter by price
curl -X POST http://localhost:5000/api/search/by-price \
  -H "Content-Type: application/json" \
  -d '{"min_price": 0, "max_price": 5}'
```

### 🔍 NLP Command Detection

The system automatically detects command types:
- **Search commands**: "find", "search", "look for", "get me"
- **Filter commands**: "under", "below", "less than", "cheaper"
- **Add commands**: "add", "buy", "get", "need", "want", "put", "grab"
- **Remove commands**: "remove", "delete", "discard", "skip", "cancel"

### 💾 Database Schema

**grocery_items table:**
```sql
CREATE TABLE grocery_items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  item_name TEXT NOT NULL,
  category TEXT,
  brand TEXT,
  size TEXT,
  price REAL,
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

**Updated shopping_list table:**
```sql
CREATE TABLE shopping_list (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  item_name TEXT NOT NULL,
  category TEXT,
  quantity REAL DEFAULT 1,
  unit TEXT,
  price REAL,
  brand TEXT,           -- NEW
  size TEXT,            -- NEW
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  completed BOOLEAN DEFAULT 0
)
```

### 🎯 Future Enhancements

Possible additions:
- Real-time inventory integration with grocery stores
- Location-based pricing
- Wishlist/favorites
- Barcode scanning for quick add
- User preferences for preferred brands
- Historical price tracking
