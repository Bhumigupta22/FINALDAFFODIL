import sqlite3
from contextlib import contextmanager
from app.config import Config

DATABASE = Config.DATABASE

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    # Table 1: Shopping List
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shopping_list (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            category TEXT,
            quantity REAL DEFAULT 1,
            unit TEXT,
            price REAL,
            brand TEXT,
            size TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed BOOLEAN DEFAULT 0
        )
    ''')
    # Table 2: Purchase History
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchase_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            category TEXT,
            purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            frequency INTEGER DEFAULT 1
        )
    ''')
    # Table 3: Grocery Items Database (for searching)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS grocery_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            category TEXT,
            brand TEXT,
            size TEXT,
            price REAL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Add missing columns to shopping_list if they don't exist
    cursor.execute("PRAGMA table_info(shopping_list)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'brand' not in columns:
        cursor.execute('ALTER TABLE shopping_list ADD COLUMN brand TEXT')
    if 'size' not in columns:
        cursor.execute('ALTER TABLE shopping_list ADD COLUMN size TEXT')
    
    conn.commit()
    conn.close()

@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def add_shopping_item(item_name, category, quantity=1, brand=None, size=None, price=None):
    with get_db() as conn:
        cursor = conn.cursor()
        # Check if item already exists
        cursor.execute('''
            SELECT id, quantity FROM shopping_list 
            WHERE LOWER(item_name) = LOWER(?) AND completed = 0
        ''', (item_name.strip(),))
        existing = cursor.fetchone()
        
        if existing:
            # Update existing item quantity
            new_quantity = existing['quantity'] + quantity
            cursor.execute('''
                UPDATE shopping_list SET quantity = ? WHERE id = ?
            ''', (new_quantity, existing['id']))
            return existing['id']
        else:
            # Insert new item
            cursor.execute('''
                INSERT INTO shopping_list (item_name, category, quantity, brand, size, price)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (item_name.strip(), category, quantity, brand, size, price))
            return cursor.lastrowid

def get_shopping_list():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM shopping_list WHERE completed = 0')
        return [dict(row) for row in cursor.fetchall()]

def remove_shopping_item(item_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM shopping_list WHERE id = ?', (item_id,))
        return cursor.rowcount > 0

def remove_item_by_name(item_name):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM shopping_list WHERE LOWER(item_name) = LOWER(?)', (item_name.strip(),))
        return cursor.rowcount > 0

def mark_item_complete(item_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE shopping_list SET completed = 1 WHERE id = ?', (item_id,))
        return cursor.rowcount > 0

def add_to_history(item_name, category):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, frequency FROM purchase_history WHERE item_name = ?', (item_name,))
        existing = cursor.fetchone()
        if existing:
            cursor.execute('UPDATE purchase_history SET frequency = frequency + 1 WHERE id = ?', (existing['id'],))
        else:
            cursor.execute('INSERT INTO purchase_history (item_name, category) VALUES (?, ?)', (item_name, category))

def get_purchase_history():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM purchase_history ORDER BY frequency DESC LIMIT 20')
        return [dict(row) for row in cursor.fetchall()]

def search_items(item_name: str, category: str = None, brand: str = None, 
                size: str = None, min_price: float = None, max_price: float = None):
    """Search for items with optional filters"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Build dynamic query
        query = 'SELECT * FROM grocery_items WHERE item_name LIKE ?'
        params = [f'%{item_name}%']
        
        if category:
            query += ' AND category = ?'
            params.append(category)
        
        if brand:
            query += ' AND brand = ?'
            params.append(brand)
        
        if size:
            query += ' AND size = ?'
            params.append(size)
        
        if min_price is not None:
            query += ' AND price >= ?'
            params.append(min_price)
        
        if max_price is not None:
            query += ' AND price <= ?'
            params.append(max_price)
        
        query += ' ORDER BY price ASC'
        
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

def filter_by_price(min_price: float = None, max_price: float = None, brand: str = None):
    """Filter items by price range and optional brand"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        query = 'SELECT * FROM grocery_items WHERE 1=1'
        params = []
        
        if min_price is not None:
            query += ' AND price >= ?'
            params.append(min_price)
        
        if max_price is not None:
            query += ' AND price <= ?'
            params.append(max_price)
        
        if brand:
            query += ' AND brand = ?'
            params.append(brand)
        
        query += ' ORDER BY price ASC'
        
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

def add_grocery_item(item_name: str, category: str, brand: str = None, 
                    size: str = None, price: float = None, description: str = None):
    """Add item to grocery database"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO grocery_items (item_name, category, brand, size, price, description)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (item_name, category, brand, size, price, description))
        return cursor.lastrowid