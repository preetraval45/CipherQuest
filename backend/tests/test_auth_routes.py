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

class TestAuthRoutes:
    def test_register_success(self, client, db_session):
        """Test successful user registration"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = client.post('/api/auth/register', json=data)
        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data
        assert 'refresh_token' in data
        assert 'user' in data

    def test_register_missing_fields(self, client):
        """Test registration with missing required fields"""
        data = {'username': 'testuser'}
        response = client.post('/api/auth/register', json=data)
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_register_invalid_email(self, client):
        """Test registration with invalid email"""
        data = {
            'username': 'testuser',
            'email': 'invalid-email',
            'password': 'TestPass123!'
        }
        response = client.post('/api/auth/register', json=data)
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_register_weak_password(self, client):
        """Test registration with weak password"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': '123'
        }
        response = client.post('/api/auth/register', json=data)
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_register_duplicate_username(self, client, db_session):
        """Test registration with existing username"""
        # Create first user
        user1_data = {
            'username': 'testuser',
            'email': 'test1@example.com',
            'password': 'TestPass123!'
        }
        client.post('/api/auth/register', json=user1_data)
        
        # Try to register with same username
        user2_data = {
            'username': 'testuser',
            'email': 'test2@example.com',
            'password': 'TestPass123!'
        }
        response = client.post('/api/auth/register', json=user2_data)
        assert response.status_code == 409
        data = response.get_json()
        assert 'error' in data

    def test_login_success(self, client, db_session):
        """Test successful login"""
        # Register user first
        register_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPass123!'
        }
        client.post('/api/auth/register', json=register_data)
        
        # Login
        login_data = {
            'username': 'testuser',
            'password': 'TestPass123!'
        }
        response = client.post('/api/auth/login', json=login_data)
        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data
        assert 'refresh_token' in data

    def test_login_invalid_credentials(self, client, db_session):
        """Test login with invalid credentials"""
        # Register user first
        register_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPass123!'
        }
        client.post('/api/auth/register', json=register_data)
        
        # Try to login with wrong password
        login_data = {
            'username': 'testuser',
            'password': 'WrongPass123!'
        }
        response = client.post('/api/auth/login', json=login_data)
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data

    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user"""
        login_data = {
            'username': 'nonexistent',
            'password': 'TestPass123!'
        }
        response = client.post('/api/auth/login', json=login_data)
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data

    def test_refresh_token_success(self, client, db_session):
        """Test successful token refresh"""
        # Register and login to get tokens
        register_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPass123!'
        }
        client.post('/api/auth/register', json=register_data)
        
        login_data = {
            'username': 'testuser',
            'password': 'TestPass123!'
        }
        login_response = client.post('/api/auth/login', json=login_data)
        refresh_token = login_response.get_json()['refresh_token']
        
        # Refresh token
        headers = {'Authorization': f'Bearer {refresh_token}'}
        response = client.post('/api/auth/refresh', headers=headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data

    def test_refresh_token_invalid(self, client):
        """Test token refresh with invalid token"""
        headers = {'Authorization': 'Bearer invalid-token'}
        response = client.post('/api/auth/refresh', headers=headers)
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data

    def test_logout_success(self, client, db_session):
        """Test successful logout"""
        # Register and login to get tokens
        register_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPass123!'
        }
        client.post('/api/auth/register', json=register_data)
        
        login_data = {
            'username': 'testuser',
            'password': 'TestPass123!'
        }
        login_response = client.post('/api/auth/login', json=login_data)
        access_token = login_response.get_json()['access_token']
        
        # Logout
        headers = {'Authorization': f'Bearer {access_token}'}
        response = client.post('/api/auth/logout', headers=headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data

    def test_rate_limiting(self, client):
        """Test rate limiting on auth endpoints"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPass123!'
        }
        
        # Make multiple requests quickly
        for _ in range(6):
            response = client.post('/api/auth/register', json=data)
        
        # Should be rate limited
        assert response.status_code == 429 