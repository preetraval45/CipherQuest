import pytest
import json
from unittest.mock import patch
from backend.app import create_app
from backend.models.user import User, db
from backend.models.leaderboard import LeaderboardEntry

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
    """Create a user and return auth headers"""
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'TestPass123!'
    }
    client.post('/api/auth/register', json=user_data)
    
    login_data = {
        'username': 'testuser',
        'password': 'TestPass123!'
    }
    response = client.post('/api/auth/login', json=login_data)
    token = response.get_json()['access_token']
    
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def sample_leaderboard(db_session):
    """Create sample leaderboard entries"""
    # Create users first
    users = [
        User(username='user1', email='user1@test.com', password='TestPass123!'),
        User(username='user2', email='user2@test.com', password='TestPass123!'),
        User(username='user3', email='user3@test.com', password='TestPass123!')
    ]
    
    for user in users:
        db.session.add(user)
    db.session.commit()
    
    # Create leaderboard entries
    entries = [
        LeaderboardEntry(
            user_id=users[0].id,
            total_score=1000,
            modules_completed=5,
            challenges_solved=10
        ),
        LeaderboardEntry(
            user_id=users[1].id,
            total_score=800,
            modules_completed=4,
            challenges_solved=8
        ),
        LeaderboardEntry(
            user_id=users[2].id,
            total_score=600,
            modules_completed=3,
            challenges_solved=6
        )
    ]
    
    for entry in entries:
        db.session.add(entry)
    db.session.commit()
    return entries

class TestLeaderboardRoutes:
    def test_get_leaderboard_success(self, client, auth_headers, sample_leaderboard):
        """Test successful retrieval of leaderboard"""
        response = client.get('/api/leaderboard', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'leaderboard' in data
        assert len(data['leaderboard']) == 3
        # Check that entries are sorted by score (descending)
        scores = [entry['total_score'] for entry in data['leaderboard']]
        assert scores == sorted(scores, reverse=True)

    def test_get_leaderboard_unauthorized(self, client):
        """Test getting leaderboard without authentication"""
        response = client.get('/api/leaderboard')
        assert response.status_code == 401

    def test_get_leaderboard_with_pagination(self, client, auth_headers, sample_leaderboard):
        """Test pagination of leaderboard"""
        response = client.get('/api/leaderboard?limit=2&offset=0', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert len(data['leaderboard']) == 2
        assert data['limit'] == 2
        assert data['offset'] == 0

    def test_get_leaderboard_with_limit(self, client, auth_headers, sample_leaderboard):
        """Test limiting leaderboard results"""
        response = client.get('/api/leaderboard?limit=1', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert len(data['leaderboard']) == 1

    def test_get_user_rank(self, client, auth_headers, sample_leaderboard):
        """Test getting current user's rank"""
        response = client.get('/api/leaderboard/rank', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'rank' in data
        assert 'score' in data

    def test_get_leaderboard_stats(self, client, auth_headers, sample_leaderboard):
        """Test getting leaderboard statistics"""
        response = client.get('/api/leaderboard/stats', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'total_users' in data
        assert 'average_score' in data
        assert 'top_score' in data

    def test_get_leaderboard_by_category(self, client, auth_headers, sample_leaderboard):
        """Test getting leaderboard filtered by category"""
        response = client.get('/api/leaderboard?category=cryptography', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'leaderboard' in data

    def test_get_leaderboard_empty(self, client, auth_headers):
        """Test getting leaderboard when no entries exist"""
        response = client.get('/api/leaderboard', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert len(data['leaderboard']) == 0

    def test_get_leaderboard_with_time_filter(self, client, auth_headers, sample_leaderboard):
        """Test getting leaderboard with time filter"""
        response = client.get('/api/leaderboard?period=weekly', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'leaderboard' in data

    def test_update_user_score(self, client, auth_headers, sample_leaderboard):
        """Test updating user's leaderboard score"""
        score_data = {
            'score': 100,
            'module_completed': True,
            'challenge_solved': False
        }
        
        response = client.post('/api/leaderboard/update', 
                             json=score_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data

    def test_get_leaderboard_around_user(self, client, auth_headers, sample_leaderboard):
        """Test getting leaderboard entries around current user"""
        response = client.get('/api/leaderboard/around-me', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'leaderboard' in data
        assert 'user_rank' in data

    def test_get_leaderboard_export(self, client, auth_headers, sample_leaderboard):
        """Test exporting leaderboard data"""
        response = client.get('/api/leaderboard/export', headers=auth_headers)
        assert response.status_code == 200
        # Should return CSV or JSON format
        assert response.headers['Content-Type'] in ['text/csv', 'application/json'] 