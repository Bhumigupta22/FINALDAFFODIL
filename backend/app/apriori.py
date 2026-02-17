from typing import List, Dict, Any
from apyori import apriori
import json


class AprioriEngine:
    def __init__(self):
        self.rules = []
        self.transactions: List[List[str]] = []

    def fit(self, transactions: List[List[str]], min_support: float = 0.02, min_confidence: float = 0.3, min_lift: float = 1.0):
        """Run apriori on transactions and cache rules."""
        self.transactions = [list(map(lambda s: s.strip().lower(), t)) for t in transactions]
        results = apriori(self.transactions, min_support=min_support, min_confidence=min_confidence, min_lift=min_lift)

        rules = []
        for record in results:
            items = tuple(record.items)
            support = float(record.support)
            for stat in record.ordered_statistics:
                base = tuple(stat.items_base)
                add = tuple(stat.items_add)
                confidence = float(stat.confidence)
                lift = float(stat.lift)
                rules.append({
                    'base': list(base),
                    'add': list(add),
                    'support': support,
                    'confidence': confidence,
                    'lift': lift
                })

        # sort rules by confidence then lift
        rules.sort(key=lambda r: (r['confidence'], r['lift']), reverse=True)
        self.rules = rules
        return rules

    def get_recommendations(self, item: str, top_n: int = 5, min_confidence: float = 0.2) -> List[Dict[str, Any]]:
        item_lower = item.strip().lower()
        recs = []
        for r in self.rules:
            if item_lower in r['base'] and r['confidence'] >= min_confidence:
                for add in r['add']:
                    recs.append({
                        'item': add,
                        'base': r['base'],
                        'support': r['support'],
                        'confidence': r['confidence'],
                        'lift': r['lift']
                    })

        # deduplicate by item and keep highest scoring
        seen = {}
        for rec in recs:
            key = rec['item']
            if key not in seen or (rec['confidence'], rec['lift']) > (seen[key]['confidence'], seen[key]['lift']):
                seen[key] = rec

        results = sorted(list(seen.values()), key=lambda r: (r['confidence'], r['lift']), reverse=True)
        return results[:top_n]


# Global engine
engine = AprioriEngine()

def load_transactions_from_json(data: Any) -> List[List[str]]:
    """Accept either list-of-lists or list-of-strings CSV-like in JSON."""
    if isinstance(data, list):
        # if items are strings containing commas, split
        transactions = []
        for t in data:
            if isinstance(t, str):
                transactions.append([i.strip().lower() for i in t.split(',') if i.strip()])
            elif isinstance(t, list):
                transactions.append([str(i).strip().lower() for i in t if str(i).strip()])
        return transactions
    return []
