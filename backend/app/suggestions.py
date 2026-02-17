from typing import List, Dict
from datetime import datetime
import random

class SuggestionEngine:
    """Generate smart suggestions based on history and seasonal items"""
    
    SEASONAL_ITEMS = {
        'spring': ['strawberry', 'asparagus', 'spinach', 'lettuce'],
        'summer': ['watermelon', 'peach', 'blueberry', 'tomato', 'corn'],
        'fall': ['apple', 'pumpkin', 'squash', 'pear'],
        'winter': ['orange', 'lemon', 'kale', 'kiwi']
    }
    
    SUBSTITUTES = {
        'milk': 'almond milk',
        'bread': 'whole wheat bread',
        'sugar': 'honey',
        'butter': 'margarine',
        'chips': 'popcorn'
    }

    def get_suggestions(self, history: List[Dict], current_list: List[Dict]) -> List[Dict]:
        current_names = [i['item_name'].lower() for i in current_list]
        suggestions = []

        # 1. Substitute Suggestions (Check if a substitute exists for items in the list)
        for item in current_list:
            name = item['item_name'].lower()
            if name in self.SUBSTITUTES:
                sub = self.SUBSTITUTES[name]
                if sub not in current_names:
                    suggestions.append({
                        'item': sub,
                        'category': 'substitute',
                        'reason': f"Try as a healthy alternative to {name}",
                        'confidence': 0.9
                    })

        # 2. History Suggestions (Items bought often but NOT in the current list)
        for h_item in history:
            name = h_item['item_name'].lower()
            if h_item['frequency'] > 2 and name not in current_names:
                suggestions.append({
                    'item': h_item['item_name'],
                    'category': h_item['category'],
                    'reason': "You buy this frequently",
                    'confidence': 0.8
                })

        # 3. Seasonal Suggestions
        month = datetime.now().month
        season = 'winter'
        if 3 <= month <= 5: season = 'spring'
        elif 6 <= month <= 8: season = 'summer'
        elif 9 <= month <= 11: season = 'fall'
        
        for s_item in self.SEASONAL_ITEMS.get(season, []):
            if s_item not in current_names:
                suggestions.append({
                    'item': s_item,
                    'category': 'produce',
                    'reason': f"Fresh in {season}!",
                    'confidence': 0.7
                })

        # 4. Default Fallback (If nothing else works)
        if not suggestions:
            defaults = ['eggs', 'bread', 'milk', 'bananas']
            for d in defaults:
                if d not in current_names:
                    suggestions.append({
                        'item': d,
                        'category': 'pantry',
                        'reason': "Popular staple item",
                        'confidence': 0.5
                    })

        # Remove duplicates and return top 5
        seen = set()
        unique_suggestions = []
        for s in suggestions:
            if s['item'].lower() not in seen:
                unique_suggestions.append(s)
                seen.add(s['item'].lower())

        return sorted(unique_suggestions, key=lambda x: x['confidence'], reverse=True)[:5]

# Instance
suggestion_engine = SuggestionEngine()

def get_suggestions(purchase_history: List[Dict], current_list: List[Dict]) -> List[Dict]:
    return suggestion_engine.get_suggestions(purchase_history, current_list)