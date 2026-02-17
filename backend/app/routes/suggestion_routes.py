from flask import Blueprint, jsonify
from app.database import get_purchase_history, get_shopping_list
from app.suggestions import get_suggestions
from app.apriori import engine as apriori_engine

bp = Blueprint('suggestions', __name__, url_prefix='/api/suggestions')

@bp.route('/', methods=['GET'])
def get_smart_suggestions():
    """Get smart suggestions based on history, seasonal, and Apriori rules"""
    try:
        history = get_purchase_history()
        current_list = get_shopping_list()
        suggestions = get_suggestions(history, current_list)
        
        # Add Apriori-based recommendations if engine has rules
        if apriori_engine.rules:
            # For each item in current list, get Apriori recommendations
            for item in current_list:
                apriori_recs = apriori_engine.get_recommendations(item['item_name'], top_n=2, min_confidence=0.15)
                for rec in apriori_recs:
                    # Check if not already suggested
                    if not any(s['item'].lower() == rec['item'].lower() for s in suggestions):
                        suggestions.append({
                            'item': rec['item'],
                            'category': 'other',  # Could enhance with actual category
                            'reason': f"Often bought with {item['item_name']} (confidence: {rec['confidence']:.0%})",
                            'suggestion_type': 'apriori',
                            'confidence': rec['confidence']
                        })
        
        # Sort by confidence
        suggestions.sort(key=lambda x: x.get('confidence', 0), reverse=True)
        
        return jsonify({
            'suggestions': suggestions,
            'count': len(suggestions)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/history', methods=['GET'])
def get_history():
    """Get purchase history for user"""
    try:
        history = get_purchase_history()
        return jsonify({
            'history': history,
            'count': len(history)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
