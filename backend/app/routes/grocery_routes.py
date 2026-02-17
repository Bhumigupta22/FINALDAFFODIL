from flask import Blueprint, request, jsonify
from app.database import add_grocery_item, get_db

bp = Blueprint('grocery', __name__, url_prefix='/api/grocery')

@bp.route('/add', methods=['POST'])
def add_item():
    """Add a new grocery item to the database"""
    try:
        data = request.get_json()
        
        # Validate required fields
        item_name = data.get('item_name', '').strip()
        price = data.get('price')
        
        if not item_name:
            return jsonify({'error': 'Item name is required'}), 400
        
        if price is None or price < 0:
            return jsonify({'error': 'Valid price is required'}), 400
        
        # Get optional fields
        category = data.get('category', 'other')
        brand = data.get('brand')
        size = data.get('size')
        description = data.get('description')
        
        # Add to database
        item_id = add_grocery_item(
            item_name=item_name,
            category=category,
            brand=brand,
            size=size,
            price=float(price),
            description=description
        )
        
        return jsonify({
            'id': item_id,
            'item_name': item_name,
            'category': category,
            'brand': brand,
            'size': size,
            'price': float(price),
            'description': description,
            'message': f'Successfully added {item_name} at ${price:.2f}'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/list', methods=['GET'])
def list_items():
    """Get all grocery items"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM grocery_items ORDER BY price ASC')
            items = [dict(row) for row in cursor.fetchall()]
            return jsonify({'items': items, 'count': len(items)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Get a specific grocery item"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM grocery_items WHERE id = ?', (item_id,))
            item = cursor.fetchone()
            
            if not item:
                return jsonify({'error': 'Item not found'}), 404
            
            return jsonify(dict(item)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete a grocery item"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM grocery_items WHERE id = ?', (item_id,))
            
            if cursor.rowcount > 0:
                return jsonify({'success': True, 'message': 'Item deleted'}), 200
            else:
                return jsonify({'error': 'Item not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
