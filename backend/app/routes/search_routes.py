from flask import Blueprint, request, jsonify
from app.database import search_items, filter_by_price
from app.nlp_processor import NLPProcessor

bp = Blueprint('search', __name__, url_prefix='/api/search')

nlp = NLPProcessor()

@bp.route('/items', methods=['POST'])
def search_items_route():
    """Search for items with optional filters (voice or text)"""
    try:
        data = request.get_json()
        text_query = data.get('text') or data.get('query')
        
        if not text_query:
            return jsonify({'error': 'Search query is required'}), 400
        
        # Process voice command to extract filters
        search_result = nlp.process_search_command(text_query)
        
        if 'error' in search_result:
            return jsonify(search_result), 400
        
        # Search items with extracted filters
        items = search_items(
            item_name=search_result.get('item_name'),
            category=search_result.get('category'),
            brand=search_result.get('brand'),
            size=search_result.get('size'),
            min_price=search_result.get('min_price'),
            max_price=search_result.get('max_price')
        )
        
        return jsonify({
            'query': text_query,
            'filters': {
                'item_name': search_result.get('item_name'),
                'category': search_result.get('category'),
                'brand': search_result.get('brand'),
                'size': search_result.get('size'),
                'min_price': search_result.get('min_price'),
                'max_price': search_result.get('max_price')
            },
            'results': [dict(item) for item in items],
            'count': len(items)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/by-price', methods=['POST'])
def filter_price_route():
    """Filter items by price range (voice or direct params)"""
    try:
        data = request.get_json()
        
        # Support both direct parameters and voice text
        min_price = data.get('min_price')
        max_price = data.get('max_price')
        brand = data.get('brand')
        text_query = data.get('text') or data.get('query')
        
        # If voice text provided, parse it
        if text_query:
            filter_result = nlp.process_filter_command(text_query)
            if 'error' in filter_result:
                return jsonify(filter_result), 400
            min_price = filter_result.get('min_price')
            max_price = filter_result.get('max_price')
            brand = filter_result.get('brand')
        
        # Filter items
        items = filter_by_price(
            min_price=min_price,
            max_price=max_price,
            brand=brand
        )
        
        return jsonify({
            'filters': {
                'min_price': min_price,
                'max_price': max_price,
                'brand': brand
            },
            'results': [dict(item) for item in items],
            'count': len(items)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/voice', methods=['POST'])
def voice_search():
    """Voice-based item search"""
    try:
        data = request.get_json()
        text = data.get('text')
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        # Process the voice command
        search_result = nlp.process_search_command(text)
        
        if 'error' in search_result:
            return jsonify(search_result), 400
        
        # Search items
        items = search_items(
            item_name=search_result.get('item_name'),
            category=search_result.get('category'),
            brand=search_result.get('brand'),
            size=search_result.get('size'),
            min_price=search_result.get('min_price'),
            max_price=search_result.get('max_price')
        )
        
        return jsonify({
            'command': 'search',
            'text': text,
            'extracted_item': search_result.get('item_name'),
            'extracted_filters': {
                'brand': search_result.get('brand'),
                'size': search_result.get('size'),
                'price_range': {
                    'min': search_result.get('min_price'),
                    'max': search_result.get('max_price')
                }
            },
            'results': [dict(item) for item in items],
            'count': len(items)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
