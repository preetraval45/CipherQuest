import os
import pytest
from unittest.mock import patch
from flask import Flask
from backend.routes.ai import ai_bp
from backend.utils import llm_service

# Set up a test Flask app
@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(ai_bp, url_prefix='/api/ai')
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

# --- LLM Service Tests ---
def test_llm_service_success(monkeypatch):
    class DummyResponse:
        def __getitem__(self, key):
            if key == 'choices':
                return [{'message': {'content': 'Test AI response'}}]
    
    monkeypatch.setenv('OPENAI_API_KEY', 'test-key')
    with patch('openai.ChatCompletion.create', return_value=DummyResponse()):
        result = llm_service.send_prompt_to_llm('Hello')
        assert 'response' in result
        assert result['response'] == 'Test AI response'

def test_llm_service_no_api_key(monkeypatch):
    monkeypatch.delenv('OPENAI_API_KEY', raising=False)
    result = llm_service.send_prompt_to_llm('Hello')
    assert 'error' in result
    assert 'API key' in result['error']

def test_llm_service_rate_limit(monkeypatch):
    monkeypatch.setenv('OPENAI_API_KEY', 'test-key')
    # Exhaust the rate limiter
    llm_service.llm_rate_limiter.calls = [llm_service.llm_rate_limiter.calls.append(0) for _ in range(llm_service.llm_rate_limiter.max_calls)]
    result = llm_service.send_prompt_to_llm('Hello')
    assert 'error' in result
    assert 'rate limit' in result['error'].lower()
    llm_service.llm_rate_limiter.calls.clear()

# --- Endpoint Tests ---
def test_ai_chat_success(client, monkeypatch):
    class DummyResponse:
        def __getitem__(self, key):
            if key == 'choices':
                return [{'message': {'content': 'Test AI response'}}]
    monkeypatch.setenv('OPENAI_API_KEY', 'test-key')
    with patch('openai.ChatCompletion.create', return_value=DummyResponse()):
        resp = client.post('/api/ai/chat', json={'prompt': 'Hello'})
        data = resp.get_json()
        assert resp.status_code == 200
        assert 'response' in data
        assert data['response'] == 'Test AI response'

def test_ai_chat_no_prompt(client):
    resp = client.post('/api/ai/chat', json={})
    data = resp.get_json()
    assert resp.status_code == 400
    assert 'error' in data

def test_ai_chat_rate_limit(client, monkeypatch):
    monkeypatch.setenv('OPENAI_API_KEY', 'test-key')
    # Exhaust the rate limiter
    llm_service.llm_rate_limiter.calls = [llm_service.llm_rate_limiter.calls.append(0) for _ in range(llm_service.llm_rate_limiter.max_calls)]
    resp = client.post('/api/ai/chat', json={'prompt': 'Hello'})
    data = resp.get_json()
    assert resp.status_code == 429
    assert 'error' in data
    llm_service.llm_rate_limiter.calls.clear() 