import pytest
import json
from unittest.mock import patch
from backend.app import create_app
from backend.models.user import User, db

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

class TestUserRoutes:
    def test_get_user_profile(self, client, db_session, auth_headers):
        """Test getting user profile"""
        response = client.get('/api/user/profile', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'user' in data
        assert data['user']['username'] == 'testuser'

    def test_update_user_profile(self, client, db_session, auth_headers):
        """Test updating user profile"""
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'bio': 'Updated bio'
        }
        
        response = client.put('/api/user/profile', json=update_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert data['user']['first_name'] == 'Updated'
        assert data['user']['last_name'] == 'Name'
        assert data['user']['bio'] == 'Updated bio'

    def test_change_password(self, client, db_session, auth_headers):
        """Test changing user password"""
        password_data = {
            'current_password': 'TestPass123!',
            'new_password': 'NewPass123!'
        }
        
        response = client.put('/api/user/password', json=password_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data

    def test_change_password_wrong_current(self, client, db_session, auth_headers):
        """Test changing password with wrong current password"""
        password_data = {
            'current_password': 'WrongPass123!',
            'new_password': 'NewPass123!'
        }
        
        response = client.put('/api/user/password', json=password_data, headers=auth_headers)
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_get_user_stats(self, client, db_session, auth_headers):
        """Test getting user statistics"""
        response = client.get('/api/user/stats', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'stats' in data
        assert 'xp' in data['stats']
        assert 'level' in data['stats']

    def test_get_user_achievements(self, client, db_session, auth_headers):
        """Test getting user achievements"""
        response = client.get('/api/user/achievements', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'achievements' in data

    def test_get_user_progress(self, client, db_session, auth_headers):
        """Test getting user progress"""
        response = client.get('/api/user/progress', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'progress' in data

    def test_delete_user_account(self, client, db_session, auth_headers):
        """Test deleting user account"""
        response = client.delete('/api/user/account', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data

    def test_get_user_activity(self, client, db_session, auth_headers):
        """Test getting user activity feed"""
        response = client.get('/api/user/activity', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'activity' in data

    def test_upload_avatar(self, client, db_session, auth_headers):
        """Test uploading user avatar"""
        # This would require file upload testing
        # For now, just test the endpoint exists
        response = client.post('/api/user/avatar', headers=auth_headers)
        # Should return 400 for missing file
        assert response.status_code in [400, 415]

    def test_get_user_settings(self, client, db_session, auth_headers):
        """Test getting user settings"""
        response = client.get('/api/user/settings', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'settings' in data

    def test_update_user_settings(self, client, db_session, auth_headers):
        """Test updating user settings"""
        settings_data = {
            'email_notifications': True,
            'theme': 'dark',
            'language': 'en'
        }
        
        response = client.put('/api/user/settings', json=settings_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert data['settings']['email_notifications'] == True
        assert data['settings']['theme'] == 'dark' 