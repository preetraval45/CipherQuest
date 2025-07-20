from flask import Blueprint, request, jsonify
from utils.llm_service import send_prompt_to_llm

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/api/ai/chat', methods=['POST'])
def chat():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({'error': 'Prompt is required.'}), 400
    result = send_prompt_to_llm(prompt)
    if 'error' in result:
        return jsonify({'error': result['error']}), 429 if 'rate limit' in result['error'].lower() else 500
    return jsonify({'response': result['response']}) 