from flask import Blueprint, request, jsonify
from app.database import (
    add_shopping_item, get_shopping_list, remove_shopping_item,
    mark_item_complete, add_to_history, get_db, remove_item_by_name
)

bp = Blueprint('shopping', __name__, url_prefix='/api/shopping')

@bp.route('/list', methods=['GET'])
def get_list():
    try:
        items = get_shopping_list()
        # Transform DB rows into frontend-expected shape and wrap in `items`
        formatted = [
            {
                'id': i['id'],
                'item_name': i['item_name'],
                'category': i.get('category'),
                'quantity': i.get('quantity', 1),
                'unit': i.get('unit'),
                'brand': i.get('brand'),
                'size': i.get('size'),
                'price': i.get('price')
            }
            for i in items
        ]
        return jsonify({'items': formatted}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/add', methods=['POST'])
def add_item():
    try:
        data = request.get_json()
        # Accept either `name` or `item_name` to be flexible
        name = data.get('item_name') or data.get('name')
        if not name:
            return jsonify({'error': 'Name is required'}), 400

        category = data.get('category', 'other')
        quantity = data.get('quantity', 1)
        brand = data.get('brand')
        size = data.get('size')
        price = data.get('price')

        item_id = add_shopping_item(name, category, quantity, brand, size, price)

        # Return the created item in the shape frontend expects (`item`)
        return jsonify({
            'item': {
                'id': item_id,
                'item_name': name,
                'category': category,
                'quantity': quantity,
                'brand': brand,
                'size': size,
                'price': price
            }
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        success = remove_shopping_item(item_id)
        if success:
            return jsonify({'success': True}), 200
        return jsonify({'error': 'Item not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    try:
        data = request.get_json()
        quantity = data.get('quantity')
        
        if quantity is None:
            return jsonify({'error': 'Quantity is required'}), 400
        
        if quantity < 1:
            # Delete item if quantity < 1
            remove_shopping_item(item_id)
            return jsonify({'success': True}), 200
        
        # Update quantity in database
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE shopping_list SET quantity = ? WHERE id = ?', (quantity, item_id))
            
            # Fetch updated item
            cursor.execute('SELECT * FROM shopping_list WHERE id = ?', (item_id,))
            item = cursor.fetchone()
            
            if not item:
                return jsonify({'error': 'Item not found'}), 404
            
            # Convert Row to dict for proper property access
            item_dict = dict(item)
            return jsonify({
                'item': {
                    'id': item_dict['id'],
                    'item_name': item_dict['item_name'],
                    'category': item_dict.get('category'),
                    'quantity': item_dict.get('quantity', 1),
                    'unit': item_dict.get('unit'),
                    'brand': item_dict.get('brand'),
                    'size': item_dict.get('size'),
                    'price': item_dict.get('price')
                }
            }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:item_id>/complete', methods=['PUT'])
def complete_item(item_id):
    try:
        success = mark_item_complete(item_id)
        if success:
            return jsonify({'success': True}), 200
        return jsonify({'error': 'Item not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500