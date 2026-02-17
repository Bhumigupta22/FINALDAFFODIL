import csv
import os
import sys
# Ensure project root is on sys.path so `app` package is importable when script is run directly
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root not in sys.path:
    sys.path.insert(0, root)

from app.apriori import engine, load_transactions_from_json


DATA_PATH = os.path.expanduser(r"C:\Users\varsh\OneDrive\Desktop\Groceries_dataset.csv")


def load_csv_transactions(path):
    transactions = []
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return transactions

    # This dataset has columns: Member_number,Date,itemDescription
    # Group items by (Member_number, Date) to form transactions
    groups = {}
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            member = row.get('Member_number') or row.get('member_number')
            date = row.get('Date') or row.get('date')
            item = row.get('itemDescription') or row.get('itemdescription') or row.get('item')
            if not member or not date or not item:
                continue
            key = (member.strip(), date.strip())
            groups.setdefault(key, set()).add(item.strip().lower())

    transactions = [list(items) for items in groups.values() if items]
    return transactions


def print_rules(rules, top_n=20):
    print(f"Top {min(len(rules), top_n)} rules")
    for i, r in enumerate(rules[:top_n], 1):
        base = ', '.join(r.get('base', []))
        add = ', '.join(r.get('add', []))
        print(f"{i}. {base} -> {add} | support={r.get('support'):.4f} confidence={r.get('confidence'):.4f} lift={r.get('lift'):.4f}")


if __name__ == '__main__':
    tx = load_csv_transactions(DATA_PATH)
    if not tx:
        print('No transactions loaded.')
        raise SystemExit(1)

    print(f'Loaded {len(tx)} transactions. Running Apriori...')

    # Try multiple support thresholds to find meaningful rules on this dataset
    for supp in [0.002, 0.001, 0.0005, 0.0002]:
        print(f"\nRunning Apriori with min_support={supp}")
        rules = engine.fit(tx, min_support=supp, min_confidence=0.2, min_lift=1.0)
        print(f"Found {len(rules)} rules")
        if rules:
            print_rules(rules, top_n=10)
            break

    # Show recommendations for a few sample items using the rules we found
    for item in ['bread', 'milk', 'whole milk', 'yogurt', 'coffee']:
        recs = engine.get_recommendations(item, top_n=5, min_confidence=0.15)
        print(f"\nRecommendations for '{item}':")
        if not recs:
            print('  (none)')
        for r in recs:
            print(f"  - {r['item']} (conf={r['confidence']:.2f}, lift={r['lift']:.2f}, support={r['support']:.6f})")
