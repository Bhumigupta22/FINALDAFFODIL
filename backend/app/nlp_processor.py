import re
from typing import Dict, Tuple, Optional, List

class NLPProcessor:
    CATEGORIES = {
        'dairy': ['milk', 'cheese', 'yogurt', 'butter', 'cream'],
        'produce': ['apple', 'banana', 'orange', 'carrot', 'broccoli', 'lettuce', 'tomato'],
        'meat': ['chicken', 'beef', 'pork', 'fish', 'sausage'],
        'snacks': ['chips', 'cookies', 'popcorn', 'nuts', 'candy'],
        'beverages': ['water', 'juice', 'soda', 'coffee', 'tea'],
        'pantry': ['bread', 'rice', 'pasta', 'cereal', 'rolls']
    }
    
    COMMANDS = {
        'remove': ['remove', 'delete', 'discard', 'skip', 'cancel', 'don\'t need'],
        'add': ['add', 'buy', 'get', 'need', 'want', 'put', 'grab'],
        'search': ['find', 'search', 'look for', 'get me'],
        'filter': ['under', 'below', 'less than', 'cheaper']
    }
    
    BRANDS = {
        'organic': ['organic', 'natural'],
        'budget': ['budget', 'value', 'store brand'],
        'premium': ['premium', 'deluxe', 'gourmet']
    }
    
    SIZES = ['small', 'medium', 'large', 'xl', 'x-large', 'mini', 'family', 'pack', 'size']

    def process_voice_command(self, text: str) -> Dict:
        if not text or not text.strip():
            return {'error': 'Empty command'}
        
        text_lower = text.lower().strip()
        command_type = 'add'
        
        if any(word in text_lower for word in self.COMMANDS['remove']):
            command_type = 'remove'

        item_name = text_lower
        # List of words to strip out of the item name
        strip_words = self.COMMANDS['add'] + self.COMMANDS['remove'] + ['please', 'to my list', 'from my list', 'the', 'a', 'an']
        
        for word in strip_words:
            item_name = re.sub(rf'\b{re.escape(word)}\b', '', item_name)
        
        # Extract and strip numbers
        number_match = re.search(r'(\d+)', item_name)
        quantity = 1
        if number_match:
            quantity = float(number_match.group(1))
            item_name = item_name.replace(str(int(quantity)), '')

        item_name = ' '.join(item_name.split()).strip()

        return {
            'command': command_type,
            'item_name': item_name,
            'quantity': quantity,
            'category': self.extract_category(item_name),
            'original_text': text
        }

    def extract_category(self, item: str) -> str:
        for category, items in self.CATEGORIES.items():
            if any(cat_item in item.lower() for cat_item in items):
                return category
        return 'other'
    
    def extract_price_range(self, text: str) -> Dict[str, Optional[float]]:
        """Extract price range (min, max) from voice text"""
        text_lower = text.lower()
        
        # Pattern for prices like "$5" or "5 dollars"
        price_patterns = [
            r'\$(\d+(?:\.\d{2})?)',  # $5 or $5.99
            r'(\d+(?:\.\d{2})?)\s*dollars?',  # 5 dollars
            r'(\d+(?:\.\d{2})?)\s*bucks?',  # 5 bucks
        ]
        
        prices = []
        for pattern in price_patterns:
            matches = re.findall(pattern, text_lower)
            prices.extend([float(m) for m in matches])
        
        if not prices:
            return {'min_price': None, 'max_price': None}
        
        prices.sort()
        
        # If single price found, assume "under/below/less than"
        if len(prices) == 1:
            return {'min_price': None, 'max_price': prices[0]}
        
        # If two prices, use as range
        return {'min_price': prices[0], 'max_price': prices[-1]}
    
    def extract_attributes(self, text: str) -> Dict[str, Optional[str]]:
        """Extract brand, size, and other attributes"""
        text_lower = text.lower()
        
        brand = None
        size = None
        
        # Check for brand
        for brand_type, brand_keywords in self.BRANDS.items():
            if any(keyword in text_lower for keyword in brand_keywords):
                brand = brand_type
                break
        
        # Check for size
        for size_keyword in self.SIZES:
            if size_keyword in text_lower:
                size = size_keyword
                break
        
        return {'brand': brand, 'size': size}
    
    def process_search_command(self, text: str) -> Dict:
        """Process search command with filters"""
        if not text or not text.strip():
            return {'error': 'Empty search query'}
        
        text_lower = text.lower().strip()
        
        # Extract item name
        item_name = text_lower
        search_words = self.COMMANDS['search'] + ['please', 'me', 'i need', 'i want']
        for word in search_words:
            item_name = re.sub(rf'\b{re.escape(word)}\b', '', item_name)
        
        item_name = ' '.join(item_name.split()).strip()
        
        # Extract additional attributes
        price_range = self.extract_price_range(text)
        attributes = self.extract_attributes(text)
        
        return {
            'command': 'search',
            'item_name': item_name,
            'category': self.extract_category(item_name),
            'min_price': price_range['min_price'],
            'max_price': price_range['max_price'],
            'brand': attributes['brand'],
            'size': attributes['size'],
            'original_text': text
        }
    
    def process_filter_command(self, text: str) -> Dict:
        """Process price filter command"""
        if not text or not text.strip():
            return {'error': 'Empty filter query'}
        
        price_range = self.extract_price_range(text)
        attributes = self.extract_attributes(text)
        
        return {
            'command': 'filter',
            'min_price': price_range['min_price'],
            'max_price': price_range['max_price'],
            'brand': attributes['brand'],
            'original_text': text
        }

nlp_processor = NLPProcessor()
def process_command(text: str) -> Dict:
    nlp = NLPProcessor()
    text_lower = text.lower()
    
    # Detect command type
    if any(word in text_lower for word in nlp.COMMANDS['search']):
        return nlp.process_search_command(text)
    elif any(word in text_lower for word in nlp.COMMANDS['filter']):
        return nlp.process_filter_command(text)
    else:
        return nlp.process_voice_command(text)