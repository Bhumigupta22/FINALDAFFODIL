# Setting Up the New Search & Filter Features

## Quick Start Guide

### 1. Backend Setup

The backend changes are automatic. Key modifications include:

**Database Enhancement:**
- New `grocery_items` table for product search
- Updated `shopping_list` table with `brand` and `size` columns
- New search and filter functions in `database.py`

**New Routes:**
- `POST /api/search/items` - Search items with filters
- `POST /api/search/by-price` - Price range filtering
- `POST /api/search/voice` - Voice search

### 2. Populate Sample Product Data

Before using search features, populate the database with sample products:

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run the population script
python -c "from scripts.populate_grocery_items import populate_grocery_items; populate_grocery_items()"
```

This adds 25 sample grocery items with prices, brands, and sizes.

### 3. Start the Application

**Terminal 1 - Backend:**
```bash
cd backend
.\venv\Scripts\Activate.ps1
python run.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### 4. Try the Features

#### Voice Search Examples:
1. **Search by name with brand:**
   - Say: "Find me organic apples"
   - Shows organic apples with prices

2. **Search with size preference:**
   - Say: "Get me large milk"
   - Shows large milk options

3. **Budget search:**
   - Say: "Find cheap bread"
   - Shows budget-friendly bread options

4. **Price range filtering:**
   - Say: "Find apples under 5 dollars"
   - Shows apples priced at $5 or less

5. **Toothpaste search:**
   - Say: "Find me toothpaste under 4 dollars"
   - Shows toothpaste options under $4

### 5. Features Overview

| Feature | Voice Command | Extracted Data |
|---------|---------------|-----------------|
| Item Search | "Find me organic apples" | name, brand, category |
| Size Selection | "Get me large milk" | name, size, category |
| Price Filtering | "Find apples under $5" | name, max_price, category |
| Budget Search | "Find cheap bread" | name, brand (budget) |
| Multi-filter | "Find organic milk under $6" | name, brand, price, category |

### 6. Frontend Components

**SearchResults Component:**
- Displays matching products
- Shows price, brand, and size tags
- "Add to Cart" button for each item
- Responsive design for mobile/desktop

### 7. Database Tables

**grocery_items Table:**
Contains searchable products with:
- `item_name` - Product name
- `category` - Category (dairy, produce, etc.)
- `brand` - Brand type (organic, budget, premium)
- `size` - Size classification
- `price` - Selling price
- `description` - Product description

**Updated shopping_list Table:**
Now includes:
- `brand` - Selected brand/type
- `size` - Selected size
- `price` - Item price from search

### 8. Advanced Usage

#### Search via API:
```bash
# Search for items
curl -X POST http://localhost:5000/api/search/items \
  -H "Content-Type: application/json" \
  -d '{"text": "Find organic apples"}'

# Filter by price range
curl -X POST http://localhost:5000/api/search/by-price \
  -H "Content-Type: application/json" \
  -d '{
    "min_price": 2,
    "max_price": 5,
    "brand": "organic"
  }'
```

### 9. Speech Recognition Support

| Browser | Status | Notes |
|---------|--------|-------|
| Chrome | ✓ Full Support | Recommended for best experience |
| Edge | ✓ Full Support | Works well |
| Safari | ✓ Full Support | iOS 14.5+ |
| Firefox | ⚠️ Limited | May require extensions |

### 10. Troubleshooting

**No search results?**
- Ensure you've populated the database with sample data
- Check that the item name is spelled correctly
- Try using category keywords (like "dairy" for milk)

**Voice not working?**
- Check browser microphone permissions
- Use Chrome, Edge, or Safari
- Ensure microphone is properly connected

**Price extraction issues?**
- Format: "under $5" or "5 dollars" or "5 bucks"
- Support other formats - be creative!

---

For more details, see [SEARCH_FEATURES.md](SEARCH_FEATURES.md)
