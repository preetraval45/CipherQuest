import pytest
import json
from unittest.mock import patch
from backend.app import create_app
from backend.models.challenge import Challenge, db

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

class TestChallengeRoutes:
    def test_get_challenges(self, client, db_session, auth_headers):
        """Test getting all challenges"""
        response = client.get('/api/challenges', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'challenges' in data

    def test_get_challenge_by_id(self, client, db_session, auth_headers):
        """Test getting a specific challenge"""
        # Create a test challenge first
        challenge_data = {
            'title': 'Test Challenge',
            'description': 'A test challenge',
            'difficulty': 'easy',
            'category': 'cryptography',
            'points': 100
        }
        create_response = client.post('/api/challenges', json=challenge_data, headers=auth_headers)
        challenge_id = create_response.get_json()['challenge']['id']
        
        # Get the challenge
        response = client.get(f'/api/challenges/{challenge_id}', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert data['challenge']['title'] == 'Test Challenge'

    def test_create_challenge(self, client, db_session, auth_headers):
        """Test creating a new challenge"""
        challenge_data = {
            'title': 'New Challenge',
            'description': 'A new challenge description',
            'difficulty': 'medium',
            'category': 'web_security',
            'points': 200,
            'flag': 'flag{test_flag}',
            'hints': ['Hint 1', 'Hint 2']
        }
        
        response = client.post('/api/challenges', json=challenge_data, headers=auth_headers)
        assert response.status_code == 201
        data = response.get_json()
        assert data['challenge']['title'] == 'New Challenge'
        assert data['challenge']['difficulty'] == 'medium'

    def test_create_challenge_missing_fields(self, client, db_session, auth_headers):
        """Test creating challenge with missing required fields"""
        challenge_data = {
            'title': 'Incomplete Challenge'
            # Missing required fields
        }
        
        response = client.post('/api/challenges', json=challenge_data, headers=auth_headers)
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_update_challenge(self, client, db_session, auth_headers):
        """Test updating an existing challenge"""
        # Create a challenge first
        challenge_data = {
            'title': 'Original Title',
            'description': 'Original description',
            'difficulty': 'easy',
            'category': 'cryptography',
            'points': 100
        }
        create_response = client.post('/api/challenges', json=challenge_data, headers=auth_headers)
        challenge_id = create_response.get_json()['challenge']['id']
        
        # Update the challenge
        update_data = {
            'title': 'Updated Title',
            'description': 'Updated description',
            'difficulty': 'hard',
            'points': 300
        }
        
        response = client.put(f'/api/challenges/{challenge_id}', json=update_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert data['challenge']['title'] == 'Updated Title'
        assert data['challenge']['difficulty'] == 'hard'

    def test_delete_challenge(self, client, db_session, auth_headers):
        """Test deleting a challenge"""
        # Create a challenge first
        challenge_data = {
            'title': 'Challenge to Delete',
            'description': 'This will be deleted',
            'difficulty': 'easy',
            'category': 'cryptography',
            'points': 100
        }
        create_response = client.post('/api/challenges', json=challenge_data, headers=auth_headers)
        challenge_id = create_response.get_json()['challenge']['id']
        
        # Delete the challenge
        response = client.delete(f'/api/challenges/{challenge_id}', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data

    def test_submit_flag(self, client, db_session, auth_headers):
        """Test submitting a flag for a challenge"""
        # Create a challenge with a flag
        challenge_data = {
            'title': 'Flag Challenge',
            'description': 'Submit the correct flag',
            'difficulty': 'easy',
            'category': 'cryptography',
            'points': 100,
            'flag': 'flag{correct_flag}'
        }
        create_response = client.post('/api/challenges', json=challenge_data, headers=auth_headers)
        challenge_id = create_response.get_json()['challenge']['id']
        
        # Submit correct flag
        flag_data = {'flag': 'flag{correct_flag}'}
        response = client.post(f'/api/challenges/{challenge_id}/submit', json=flag_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert data['correct'] == True

    def test_submit_wrong_flag(self, client, db_session, auth_headers):
        """Test submitting wrong flag for a challenge"""
        # Create a challenge with a flag
        challenge_data = {
            'title': 'Flag Challenge',
            'description': 'Submit the correct flag',
            'difficulty': 'easy',
            'category': 'cryptography',
            'points': 100,
            'flag': 'flag{correct_flag}'
        }
        create_response = client.post('/api/challenges', json=challenge_data, headers=auth_headers)
        challenge_id = create_response.get_json()['challenge']['id']
        
        # Submit wrong flag
        flag_data = {'flag': 'flag{wrong_flag}'}
        response = client.post(f'/api/challenges/{challenge_id}/submit', json=flag_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert data['correct'] == False

    def test_get_challenges_by_category(self, client, db_session, auth_headers):
        """Test getting challenges filtered by category"""
        # Create challenges in different categories
        challenges = [
            {'title': 'Crypto 1', 'description': 'Crypto challenge', 'difficulty': 'easy', 'category': 'cryptography', 'points': 100},
            {'title': 'Web 1', 'description': 'Web challenge', 'difficulty': 'easy', 'category': 'web_security', 'points': 100},
            {'title': 'Crypto 2', 'description': 'Another crypto challenge', 'difficulty': 'medium', 'category': 'cryptography', 'points': 200}
        ]
        
        for challenge in challenges:
            client.post('/api/challenges', json=challenge, headers=auth_headers)
        
        # Get crypto challenges
        response = client.get('/api/challenges?category=cryptography', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert len(data['challenges']) == 2
        assert all(challenge['category'] == 'cryptography' for challenge in data['challenges'])

    def test_get_challenges_by_difficulty(self, client, db_session, auth_headers):
        """Test getting challenges filtered by difficulty"""
        # Create challenges with different difficulties
        challenges = [
            {'title': 'Easy 1', 'description': 'Easy challenge', 'difficulty': 'easy', 'category': 'cryptography', 'points': 100},
            {'title': 'Medium 1', 'description': 'Medium challenge', 'difficulty': 'medium', 'category': 'cryptography', 'points': 200},
            {'title': 'Hard 1', 'description': 'Hard challenge', 'difficulty': 'hard', 'category': 'cryptography', 'points': 300}
        ]
        
        for challenge in challenges:
            client.post('/api/challenges', json=challenge, headers=auth_headers)
        
        # Get medium difficulty challenges
        response = client.get('/api/challenges?difficulty=medium', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert len(data['challenges']) == 1
        assert data['challenges'][0]['difficulty'] == 'medium' 