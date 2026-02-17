from flask import Blueprint, request, jsonify
from app.nlp_processor import process_command
from app.voice_processor import transcribe_audio
from app.database import search_items, filter_by_price

bp = Blueprint('voice', __name__, url_prefix='/api/voice')

@bp.route('/process', methods=['POST'])
def process_voice_command():
    """Process voice command and extract intent"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        result = process_command(text)
        
        if 'error' in result:
            return jsonify(result), 400
        
        # If it's a search command, also return search results
        if result.get('command') == 'search':
            items = search_items(
                item_name=result.get('item_name'),
                category=result.get('category'),
                brand=result.get('brand'),
                size=result.get('size'),
                min_price=result.get('min_price'),
                max_price=result.get('max_price')
            )
            result['search_results'] = [dict(item) for item in items]
            result['results_count'] = len(items)
        
        # If it's a filter command, return filtered results
        elif result.get('command') == 'filter':
            items = filter_by_price(
                min_price=result.get('min_price'),
                max_price=result.get('max_price'),
                brand=result.get('brand')
            )
            result['filter_results'] = [dict(item) for item in items]
            result['results_count'] = len(items)
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/transcribe', methods=['POST'])
def transcribe():
    """Transcribe audio to text"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'Audio file is required'}), 400
        
        audio_file = request.files['audio']
        language = request.form.get('language', 'en-US')
        
        audio_content = audio_file.read()
        result = transcribe_audio(audio_content, language)
        
        if result.get('error'):
            return jsonify(result), 400
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/languages', methods=['GET'])
def get_languages():
    """Get supported languages"""
    languages = {
        'en-US': 'English (US)',
        'en-GB': 'English (UK)',
        'es-ES': 'Spanish',
        'fr-FR': 'French',
        'de-DE': 'German',
        'it-IT': 'Italian',
        'ja-JP': 'Japanese',
        'zh-CN': 'Chinese (Mandarin)',
        'hi-IN': 'Hindi'
    }
    return jsonify({'languages': languages}), 200
