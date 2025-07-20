import pytest
import os
import tempfile
from backend.app import create_app
from backend.models.user import db as user_db
from backend.models.module import db as module_db
from backend.models.challenge import db as challenge_db
from backend.models.progress import db as progress_db
from backend.models.leaderboard import db as leaderboard_db

@pytest.fixture(scope='session')
def app():
    """Create and configure a new app instance for each test session."""
    # Create a temporary file to isolate the database for each test session
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app('testing')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['TESTING'] = True
    
    # Create the database and load test data
    with app.app_context():
        # Initialize all database instances
        user_db.init_app(app)
        module_db.init_app(app)
        challenge_db.init_app(app)
        progress_db.init_app(app)
        leaderboard_db.init_app(app)
        
        # Create all tables
        user_db.create_all()
        module_db.create_all()
        challenge_db.create_all()
        progress_db.create_all()
        leaderboard_db.create_all()
    
    yield app
    
    # Clean up the temporary database
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture(scope='function')
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture(scope='function')
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

@pytest.fixture(scope='function')
def db_session(app):
    """Database session for testing."""
    with app.app_context():
        # Start a transaction
        user_db.session.begin_nested()
        module_db.session.begin_nested()
        challenge_db.session.begin_nested()
        progress_db.session.begin_nested()
        leaderboard_db.session.begin_nested()
        
        yield {
            'user_db': user_db,
            'module_db': module_db,
            'challenge_db': challenge_db,
            'progress_db': progress_db,
            'leaderboard_db': leaderboard_db
        }
        
        # Rollback the transaction
        user_db.session.rollback()
        module_db.session.rollback()
        challenge_db.session.rollback()
        progress_db.session.rollback()
        leaderboard_db.session.rollback()

@pytest.fixture(scope='function')
def auth_headers(client, db_session):
    """Create authenticated user and return headers."""
    # Register user
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'TestPass123!',
        'first_name': 'Test',
        'last_name': 'User'
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

@pytest.fixture(scope='function')
def admin_headers(client, db_session):
    """Create authenticated admin user and return headers."""
    # Register admin user
    user_data = {
        'username': 'admin',
        'email': 'admin@example.com',
        'password': 'AdminPass123!',
        'first_name': 'Admin',
        'last_name': 'User',
        'role': 'admin'
    }
    client.post('/api/auth/register', json=user_data)
    
    # Login to get token
    login_data = {
        'username': 'admin',
        'password': 'AdminPass123!'
    }
    response = client.post('/api/auth/login', json=login_data)
    token = response.get_json()['access_token']
    
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture(scope='function')
def sample_module_data():
    """Sample module data for testing."""
    return {
        'title': 'Test Module',
        'description': 'A test module for testing purposes',
        'content': 'This is the module content...',
        'difficulty': 'easy',
        'category': 'cryptography',
        'estimated_time': 30,
        'prerequisites': []
    }

@pytest.fixture(scope='function')
def sample_challenge_data():
    """Sample challenge data for testing."""
    return {
        'title': 'Test Challenge',
        'description': 'A test challenge for testing purposes',
        'difficulty': 'easy',
        'category': 'cryptography',
        'points': 100,
        'flag': 'flag{test_flag}',
        'hints': ['Hint 1', 'Hint 2'],
        'files': []
    }

@pytest.fixture(scope='function')
def sample_user_data():
    """Sample user data for testing."""
    return {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'TestPass123!',
        'first_name': 'Test',
        'last_name': 'User'
    }

@pytest.fixture(scope='function')
def mock_llm_response():
    """Mock LLM response for testing."""
    return {
        'response': 'This is a mock AI response for testing purposes.',
        'confidence': 0.95,
        'sources': ['source1', 'source2']
    }

@pytest.fixture(scope='function')
def mock_email_service():
    """Mock email service for testing."""
    class MockEmailService:
        def __init__(self):
            self.sent_emails = []
        
        def send_email(self, to, subject, body):
            self.sent_emails.append({
                'to': to,
                'subject': subject,
                'body': body
            })
            return True
    
    return MockEmailService()

@pytest.fixture(scope='function')
def mock_file_storage():
    """Mock file storage for testing."""
    class MockFileStorage:
        def __init__(self):
            self.files = {}
        
        def save_file(self, file_data, filename):
            self.files[filename] = file_data
            return f'/uploads/{filename}'
        
        def get_file(self, filename):
            return self.files.get(filename)
        
        def delete_file(self, filename):
            if filename in self.files:
                del self.files[filename]
                return True
            return False
    
    return MockFileStorage() 