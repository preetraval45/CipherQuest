import pytest
import json
from unittest.mock import patch
from backend.app import create_app
from backend.models.progress import Progress, db

@pytest.fixture
def app():
    app = create_app('testing')
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db_session(app):
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()

@pytest.fixture
def auth_headers(client, db_session):
    """Create authenticated user and return headers"""
    # Register user
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'TestPass123!'
    }
    client.post('/api/auth/register', json=user_data)
    
    # Login to get token
    login_data = {
        'username': 'testuser',
        'password': 'TestPass123!'
    }
    response = client.post('/api/auth/login', json=login_data)
    token = response.get_json()['access_token']
    
    return {'Authorization': f'Bearer {token}'}

class TestProgressRoutes:
    def test_get_user_progress(self, client, db_session, auth_headers):
        """Test getting user progress"""
        response = client.get('/api/progress', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'progress' in data

    def test_update_module_progress(self, client, db_session, auth_headers):
        """Test updating module progress"""
        progress_data = {
            'module_id': 1,
            'status': 'completed',
            'score': 85,
            'time_spent': 1200
        }
        
        response = client.post('/api/progress/module', json=progress_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'progress' in data
        assert data['progress']['status'] == 'completed'

    def test_update_challenge_progress(self, client, db_session, auth_headers):
        """Test updating challenge progress"""
        progress_data = {
            'challenge_id': 1,
            'status': 'completed',
            'attempts': 3,
            'time_spent': 600
        }
        
        response = client.post('/api/progress/challenge', json=progress_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'progress' in data
        assert data['progress']['status'] == 'completed'

    def test_get_module_progress(self, client, db_session, auth_headers):
        """Test getting progress for specific module"""
        # First create some progress
        progress_data = {
            'module_id': 1,
            'status': 'in_progress',
            'score': 50,
            'time_spent': 600
        }
        client.post('/api/progress/module', json=progress_data, headers=auth_headers)
        
        # Get the progress
        response = client.get('/api/progress/module/1', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'progress' in data
        assert data['progress']['module_id'] == 1

    def test_get_challenge_progress(self, client, db_session, auth_headers):
        """Test getting progress for specific challenge"""
        # First create some progress
        progress_data = {
            'challenge_id': 1,
            'status': 'completed',
            'attempts': 2,
            'time_spent': 300
        }
        client.post('/api/progress/challenge', json=progress_data, headers=auth_headers)
        
        # Get the progress
        response = client.get('/api/progress/challenge/1', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'progress' in data
        assert data['progress']['challenge_id'] == 1

    def test_get_progress_summary(self, client, db_session, auth_headers):
        """Test getting progress summary"""
        response = client.get('/api/progress/summary', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'summary' in data
        assert 'total_modules' in data['summary']
        assert 'completed_modules' in data['summary']
        assert 'total_challenges' in data['summary']
        assert 'completed_challenges' in data['summary']

    def test_reset_progress(self, client, db_session, auth_headers):
        """Test resetting user progress"""
        response = client.post('/api/progress/reset', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data

    def test_get_learning_path(self, client, db_session, auth_headers):
        """Test getting personalized learning path"""
        response = client.get('/api/progress/learning-path', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'learning_path' in data

    def test_update_quiz_progress(self, client, db_session, auth_headers):
        """Test updating quiz progress"""
        quiz_data = {
            'quiz_id': 1,
            'score': 80,
            'total_questions': 10,
            'correct_answers': 8,
            'time_spent': 300
        }
        
        response = client.post('/api/progress/quiz', json=quiz_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'progress' in data
        assert data['progress']['score'] == 80

    def test_get_progress_analytics(self, client, db_session, auth_headers):
        """Test getting progress analytics"""
        response = client.get('/api/progress/analytics', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'analytics' in data
        assert 'streak' in data['analytics']
        assert 'average_score' in data['analytics']
        assert 'time_spent' in data['analytics']

    def test_export_progress(self, client, db_session, auth_headers):
        """Test exporting progress data"""
        response = client.get('/api/progress/export', headers=auth_headers)
        assert response.status_code == 200
        # Should return a file download
        assert response.headers.get('Content-Type') == 'application/json'

    def test_invalid_progress_update(self, client, db_session, auth_headers):
        """Test updating progress with invalid data"""
        invalid_data = {
            'module_id': 'invalid_id',
            'status': 'invalid_status'
        }
        
        response = client.post('/api/progress/module', json=invalid_data, headers=auth_headers)
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data 