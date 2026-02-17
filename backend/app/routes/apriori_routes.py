from flask import Blueprint, jsonify, request
from app.apriori import engine

# Yahan hum 'bp' define kar rahe hain jo __init__.py ko chahiye
bp = Blueprint('apriori', __name__, url_prefix='/api/suggestions/apriori')

@bp.route('/rules', methods=['GET'])
def get_rules():
    """Rules dekhne ke liye route"""
    return jsonify({
        'rules_count': len(engine.rules),
        'rules': [str(rule) for rule in engine.rules[:20]]
    })

@bp.route('/predict', methods=['POST'])
def predict():
    """Suggestions dene ke liye route"""
    data = request.get_json()
    current_items = data.get('items', [])
    predictions = engine.predict(current_items)
    return jsonify({'predictions': predictions})