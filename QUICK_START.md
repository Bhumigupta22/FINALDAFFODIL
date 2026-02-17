# Quick Reference: New Search & Filter Features

## 🎤 Voice Commands Cheat Sheet

### Item Search
```
"Find me [brand] [item] [size]"
"Search for [item] [brand]"
"Get me [size] [item]"
"Look for [brand] [item]"
```

**Examples:**
- "Find me organic apples"
- "Search for large milk"
- "Get me budget bread"

### Price Filtering
```
"Find [item] under $[price]"
"Show [item] [price] dollars"
"Look for [item] below $[price]"
```

**Examples:**
- "Find toothpaste under $5"
- "Show apples below 3 dollars"
- "Get me bread under 4 bucks"

---

## 📝 Sample Products in Database

After running the population script, you have:

| Item | Brands Available | Prices | Sizes |
|------|------------------|--------|-------|
| Apples | organic, budget, premium | $0.59-$4.49 | medium, large |
| Milk | organic, standard, skim | $2.99-$5.99 | large |
| Bread | organic, standard, budget | $1.99-$4.49 | — |
| Toothpaste | budget, standard, whitening | $2.99-$4.99 | medium |
| Cheese | standard, budget, premium | $3.99-$6.99 | medium, large |
| Chicken | standard, organic | $6.49-$10.99 | — |

---

## 🚀 Quick Setup

```bash
# 1. Backend setup
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py

# 2. Frontend setup (new terminal)
cd frontend
npm install
npm run dev

# 3. Populate database (in backend directory)
python -c "from scripts.populate_grocery_items import populate_grocery_items; populate_grocery_items()"
```

---

## 🎯 Try These Commands

1. **"Find me organic apples"**
   - Returns organic apples with prices

2. **"Get me large milk"**
   - Shows large size milk options

3. **"Find toothpaste under $4"**
   - Shows toothpaste priced at $4 or less

4. **"Search for budget bread"**
   - Returns budget-friendly bread options

5. **"Show me apples below 3 dollars"**
   - Apple options under $3

---

## 🔍 What Gets Extracted

### Item Search
- **Item name**: What you're looking for
- **Brand**: organic, budget, premium
- **Size**: small, medium, large, xl
- **Category**: Automatic from keywords

### Price Filtering
- **Max price**: "under $5"
- **Min price**: "over $3" 
- **Brand**: "cheap", "budget", "premium"

---

## 📱 Frontend Usage

1. **Tap microphone** → Speak command
2. **See search results** ↓
3. **Click "Add to Cart"** to add items
4. **View in shopping list** with brand/size/price badges

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| No results found | Check database is populated, try different keywords |
| Voice not working | Use Chrome/Edge, check microphone permissions |
| Price not detected | Use format: "$5" or "5 dollars" |
| Can't see brand/size | Items from search results will include these |

---

## 📊 API Quick Reference

```bash
# Search items
curl -X POST http://localhost:5000/api/search/items \
  -H "Content-Type: application/json" \
  -d '{"text": "Find organic apples"}'

# Filter by price
curl -X POST http://localhost:5000/api/search/by-price \
  -H "Content-Type: application/json" \
  -d '{"max_price": 5, "brand": "organic"}'

# Process voice command (includes search)
curl -X POST http://localhost:5000/api/voice/process \
  -H "Content-Type: application/json" \
  -d '{"text": "Find toothpaste under $4"}'
```

---

## 📚 Documentation Files

- **IMPLEMENTATION_SUMMARY.md** - Complete technical breakdown
- **SEARCH_FEATURES.md** - Feature documentation & API specs
- **SETUP_SEARCH_FEATURES.md** - Detailed setup guide

---

## ✨ Key Features at a Glance

✅ **Voice-based search** with natural language  
✅ **Multi-filter support** (brand, size, price)  
✅ **Price range filtering** ($, dollars, bucks)  
✅ **Visual search results** with item details  
✅ **One-click add to cart** from search results  
✅ **Shopping list** shows brand/size/price info  
✅ **Responsive design** for mobile & desktop  
✅ **Sample data included** (25 products)  

---

**Ready to use!** Start with "Find me organic apples" 🎤🍎
