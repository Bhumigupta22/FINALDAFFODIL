import pandas as pd
import sqlite3
import os

# Path to your database - make sure this matches your config
DB_PATH = 'shopping_assistant.db'

def import_and_train():
    if not os.path.exists('Groceries_dataset.csv'):
        print("Error: Groceries_dataset.csv not found!")
        return

    print("--- Starting Data Import ---")
    df = pd.read_csv('Groceries_dataset.csv')
    
    # 1. Connect to SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 2. Clear existing history to avoid duplicates
    cursor.execute("DELETE FROM purchase_history")

    # 3. Import Global Frequencies
    # This makes 'whole milk' show up as a suggestion because it's popular
    print("Calculating item frequencies...")
    item_counts = df['itemDescription'].value_counts().reset_index()
    item_counts.columns = ['item_name', 'frequency']

    for _, row in item_counts.iterrows():
        cursor.execute('''
            INSERT INTO purchase_history (item_name, category, frequency)
            VALUES (?, ?, ?)
        ''', (row['item_name'], 'grocery', int(row['frequency'])))

    conn.commit()
    conn.close()
    print(f"✅ Success! Imported {len(item_counts)} items into history.")
    print("--- Now training the Apriori AI ---")

    # 4. Train the Apriori Engine using Baskets
    # We group by Member and Date to see what was bought together
    from app.apriori import engine
    baskets = df.groupby(['Member_number', 'Date'])['itemDescription'].apply(list).tolist()
    
    # We use a small min_support because there are 38k rows
    engine.fit(baskets, min_support=0.0005, min_confidence=0.05)
    print(f"✅ AI Trained! Found {len(engine.rules)} smart associations.")

if __name__ == "__main__":
    import_and_train()